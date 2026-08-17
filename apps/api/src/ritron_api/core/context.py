"""Provider-independent execution context and cooperative cancellation."""

import asyncio
from dataclasses import dataclass, field
from time import monotonic
from uuid import uuid4

from ritron_api.model_gateway.errors import ModelCancelledError, ProviderTimeoutError


@dataclass
class ExecutionContext:
    request_id: str | None
    timeout_seconds: float
    operation_id: str = field(default_factory=lambda: str(uuid4()))
    cancel_event: asyncio.Event = field(default_factory=asyncio.Event)
    _started_at: float = field(default_factory=monotonic)

    def remaining_seconds(self) -> float:
        return max(0.0, self.timeout_seconds - (monotonic() - self._started_at))

    def ensure_active(self) -> None:
        if self.cancel_event.is_set():
            raise ModelCancelledError("Model operation was cancelled")
        if self.remaining_seconds() <= 0:
            raise ProviderTimeoutError("Model operation exceeded its total timeout")

    def cancel(self) -> None:
        self.cancel_event.set()
