"""Public response contracts for the Step 01 API."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)
    reference: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody
    request_id: str
    timestamp: datetime


class LivenessResponse(BaseModel):
    status: str = "alive"
    timestamp: datetime


class ReadinessCheckResponse(BaseModel):
    name: str
    ready: bool


class ReadinessResponse(BaseModel):
    status: str
    checks: list[ReadinessCheckResponse]
    timestamp: datetime
