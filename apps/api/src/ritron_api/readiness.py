"""Extensible readiness checks without coupling to future dependencies."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class ReadinessResult:
    name: str
    ready: bool


ReadinessCheck = Callable[[], ReadinessResult]


class ReadinessRegistry:
    def __init__(self, checks: Sequence[ReadinessCheck] = ()) -> None:
        self._checks = tuple(checks)

    def evaluate(self) -> tuple[ReadinessResult, ...]:
        return tuple(check() for check in self._checks)


def application_bootstrap_check() -> ReadinessResult:
    return ReadinessResult(name="application", ready=True)
