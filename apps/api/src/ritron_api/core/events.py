"""Safe execution events for logging and future telemetry integrations."""

from dataclasses import dataclass
from enum import StrEnum

from ritron_api.model_gateway.contracts import Usage


class ExecutionStatus(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class ModelExecutionEvent:
    operation_id: str
    request_id: str | None
    status: ExecutionStatus
    provider_id: str | None = None
    model_id: str | None = None
    latency_ms: int | None = None
    retry_count: int = 0
    fallback_count: int = 0
    usage: Usage | None = None
    error_code: str | None = None
