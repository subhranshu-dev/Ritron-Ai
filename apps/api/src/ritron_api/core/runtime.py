"""Reusable model execution runtime; HTTP is deliberately absent here."""

from collections.abc import AsyncIterator
from time import monotonic
from typing import Protocol

from ritron_api.core.context import ExecutionContext
from ritron_api.core.events import ExecutionStatus, ModelExecutionEvent
from ritron_api.core.telemetry import ModelTelemetryHook, NullTelemetry
from ritron_api.model_gateway.contracts import (
    ModelRequest,
    ModelResponse,
    ModelStreamEvent,
)
from ritron_api.model_gateway.errors import ModelCancelledError, ModelGatewayError


class ModelGateway(Protocol):
    async def generate(
        self, request: ModelRequest, context: ExecutionContext
    ) -> ModelResponse: ...

    async def stream(
        self, request: ModelRequest, context: ExecutionContext
    ) -> AsyncIterator[ModelStreamEvent]: ...


class ModelExecutionRuntime:
    def __init__(
        self, gateway: ModelGateway, telemetry: ModelTelemetryHook | None = None
    ) -> None:
        self._gateway = gateway
        self._telemetry = telemetry or NullTelemetry()

    async def generate(self, request: ModelRequest) -> ModelResponse:
        context = self._context_for(request)
        started = monotonic()
        self._telemetry.emit(
            ModelExecutionEvent(
                context.operation_id, request.request_id, ExecutionStatus.STARTED
            )
        )
        try:
            response = await self._gateway.generate(request, context)
        except ModelCancelledError:
            self._telemetry.emit(
                ModelExecutionEvent(
                    context.operation_id, request.request_id, ExecutionStatus.CANCELLED
                )
            )
            raise
        except ModelGatewayError as error:
            self._telemetry.emit(
                ModelExecutionEvent(
                    context.operation_id,
                    request.request_id,
                    ExecutionStatus.FAILED,
                    error_code=error.code.value,
                )
            )
            raise
        self._telemetry.emit(
            ModelExecutionEvent(
                context.operation_id,
                request.request_id,
                ExecutionStatus.COMPLETED,
                provider_id=response.provider_id,
                model_id=response.model_id,
                latency_ms=int((monotonic() - started) * 1000),
                usage=response.usage,
            )
        )
        return response

    async def stream(self, request: ModelRequest) -> AsyncIterator[ModelStreamEvent]:
        context = self._context_for(request)
        self._telemetry.emit(
            ModelExecutionEvent(
                context.operation_id, request.request_id, ExecutionStatus.STARTED
            )
        )
        try:
            async for event in self._gateway.stream(request, context):
                yield event
                if event.type == "completed":
                    self._telemetry.emit(
                        ModelExecutionEvent(
                            context.operation_id,
                            request.request_id,
                            ExecutionStatus.COMPLETED,
                            usage=event.usage,
                        )
                    )
                elif event.type == "failed":
                    self._telemetry.emit(
                        ModelExecutionEvent(
                            context.operation_id,
                            request.request_id,
                            ExecutionStatus.FAILED,
                            error_code=event.code,
                        )
                    )
        except ModelCancelledError:
            self._telemetry.emit(
                ModelExecutionEvent(
                    context.operation_id, request.request_id, ExecutionStatus.CANCELLED
                )
            )
            raise
        finally:
            context.cancel()

    @staticmethod
    def _context_for(request: ModelRequest) -> ExecutionContext:
        return ExecutionContext(
            request_id=request.request_id,
            timeout_seconds=request.timeout_seconds or 60.0,
        )
