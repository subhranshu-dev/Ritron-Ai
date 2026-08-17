"""Safe structured logging for the API foundation."""

import json
import logging
from datetime import UTC, datetime
from typing import Any

from ritron_api.context import request_id_context

SENSITIVE_FIELD_MARKERS = ("api_key", "authorization", "password", "secret", "token")


def redact(value: Any) -> Any:
    """Return a recursively redacted logging value without mutating the input."""
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if _is_sensitive(key) else redact(nested)
            for key, nested in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact(item) for item in value)
    return value


def _is_sensitive(key: str) -> bool:
    lowered = key.lower()
    return any(marker in lowered for marker in SENSITIVE_FIELD_MARKERS)


class JsonFormatter(logging.Formatter):
    """Format log records as a stable, safe JSON object."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "service": "ritron-api",
            "environment": getattr(record, "environment", "unknown"),
            "request_id": request_id_context.get(),
            "event": getattr(record, "event", record.name),
            "message": record.getMessage(),
        }
        extra = getattr(record, "extra", None)
        if isinstance(extra, dict):
            payload["extra"] = redact(extra)
        return json.dumps(payload, default=str, separators=(",", ":"))


def configure_logging(environment: str, level: str) -> None:
    """Configure the RITRON logger without changing global root logging."""
    logger = logging.getLogger("ritron")
    logger.handlers.clear()
    logger.setLevel(level)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.info(
        "logging configured",
        extra={"environment": environment, "event": "logging.configured"},
    )
