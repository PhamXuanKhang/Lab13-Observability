from __future__ import annotations

# verified: Langfuse credentials loaded from environment variables (LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)
import os
from typing import Any

try:
    from langfuse import get_client, observe

    # Accepted kwarg sets for each v3 method (prevents unexpected keyword errors)
    _SPAN_KEYS = frozenset({"name", "input", "output", "metadata", "version", "level", "status_message"})
    _GEN_KEYS  = _SPAN_KEYS | frozenset({"completion_start_time", "model", "model_parameters",
                                          "usage_details", "cost_details", "prompt"})

    class _LangfuseContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            # Langfuse v3 removed update_current_trace; store trace-level attrs in span metadata.
            client = get_client()
            meta = {k: v for k, v in kwargs.items() if k not in _SPAN_KEYS}
            if meta:
                client.update_current_span(metadata=meta)

        def update_current_observation(self, **kwargs: Any) -> None:
            client = get_client()
            if "usage_details" in kwargs or "cost_details" in kwargs or "model" in kwargs:
                client.update_current_generation(**{k: v for k, v in kwargs.items() if k in _GEN_KEYS})
            else:
                client.update_current_span(**{k: v for k, v in kwargs.items() if k in _SPAN_KEYS})

    langfuse_context = _LangfuseContext()
except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
