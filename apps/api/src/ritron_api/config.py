"""Typed, environment-backed API configuration."""

from collections.abc import Sequence
from enum import StrEnum
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Configuration available to the Step 01 core process only."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="RITRON_API_",
        extra="ignore",
    )

    environment: Environment = Environment.DEVELOPMENT
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = "INFO"
    cors_origins: Annotated[tuple[str, ...], NoDecode] = ("http://localhost:1420",)

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            message = "RITRON_API_LOG_LEVEL must be a standard Python log level"
            raise ValueError(message)
        return normalized

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | Sequence[str]) -> tuple[str, ...]:
        if isinstance(value, str):
            origins = tuple(origin.strip() for origin in value.split(",") if origin.strip())
        else:
            origins = tuple(value)
        if not origins:
            message = "RITRON_API_CORS_ORIGINS must contain at least one origin"
            raise ValueError(message)
        return origins
