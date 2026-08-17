"""Lightweight extension point for model execution observability."""

from typing import Protocol

from ritron_api.core.events import ModelExecutionEvent


class ModelTelemetryHook(Protocol):
    def emit(self, event: ModelExecutionEvent) -> None: ...


class NullTelemetry:
    def emit(self, event: ModelExecutionEvent) -> None:
        del event
