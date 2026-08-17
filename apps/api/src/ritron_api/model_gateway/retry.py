"""Bounded, cancellation-aware retry policy."""

import asyncio
import random
from dataclasses import dataclass

from ritron_api.core.context import ExecutionContext
from ritron_api.model_gateway.errors import ModelGatewayError


@dataclass(frozen=True)
class RetryPolicy:
    max_retries: int = 2
    initial_backoff_seconds: float = 0.25
    max_backoff_seconds: float = 4.0

    def delay_for(self, retry_number: int, random_value: float | None = None) -> float:
        capped = min(self.max_backoff_seconds, self.initial_backoff_seconds * 2**retry_number)
        return capped * (random.random() if random_value is None else random_value)

    async def wait(self, retry_number: int, context: ExecutionContext) -> None:
        context.ensure_active()
        delay = min(self.delay_for(retry_number), context.remaining_seconds())
        if delay <= 0:
            context.ensure_active()
        try:
            await asyncio.wait_for(context.cancel_event.wait(), timeout=delay)
        except TimeoutError:
            return
        context.ensure_active()

    def should_retry(self, error: ModelGatewayError, attempt: int, context: ExecutionContext) -> bool:
        return error.retryable and attempt < self.max_retries and context.remaining_seconds() > 0
