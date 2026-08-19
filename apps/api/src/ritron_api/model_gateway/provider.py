"""Provider adapter protocol; provider SDK types cannot cross this boundary."""

from collections.abc import AsyncIterator
from typing import Protocol

from ritron_api.core.context import ExecutionContext
from ritron_api.model_gateway.contracts import (
    ModelDescriptor,
    ModelRequest,
    ModelResponse,
    ModelStreamEvent,
)


class ModelProvider(Protocol):
    id: str

    async def generate(self, request: ModelRequest, context: ExecutionContext) -> ModelResponse: ...

    async def stream(
        self, request: ModelRequest, context: ExecutionContext
    ) -> AsyncIterator[ModelStreamEvent]: ...

    def get_model(self, model_id: str) -> ModelDescriptor | None: ...

    def list_models(self) -> tuple[ModelDescriptor, ...]: ...
