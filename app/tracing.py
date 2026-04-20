from __future__ import annotations

# verified: Langfuse credentials loaded from environment variables (LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)
import os
from typing import Any

try:
    from langfuse import get_client, observe

    class _LangfuseContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            get_client().update_current_trace(**kwargs)

        # Backwards-compatible alias for older examples/templates.
        # In langfuse>=3, "observation" is represented as spans/generations.
        def update_current_observation(self, **kwargs: Any) -> None:
            client = get_client()
            if "usage_details" in kwargs or "cost_details" in kwargs or "model" in kwargs:
                client.update_current_generation(**kwargs)
            else:
                client.update_current_span(**kwargs)

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
