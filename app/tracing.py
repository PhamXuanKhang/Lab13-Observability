from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
import logging
from typing import Any
from functools import wraps

logger = logging.getLogger(__name__)

try:
    from langfuse import observe, get_client
    _langfuse_client = get_client()
    logger.info("Langfuse v4 loaded successfully")
    LANGFUSE_AVAILABLE = True
except Exception as e:
    logger.warning(f"Langfuse not available: {e}")
    LANGFUSE_AVAILABLE = False

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    def get_client():
        return None


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))