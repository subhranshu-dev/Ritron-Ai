"""FastAPI application factory and foundation middleware."""

import logging
import re
import uuid
from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRouter
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware

from ritron_api.config import Settings
from ritron_api.context import request_id_context
from ritron_api.contracts import (
    ErrorBody,
    ErrorResponse,
    LivenessResponse,
    ReadinessCheckResponse,
    ReadinessResponse,
)
from ritron_api.logging import configure_logging
from ritron_api.readiness import ReadinessCheck, ReadinessRegistry, application_bootstrap_check

REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9-]{1,128}$")
logger = logging.getLogger("ritron")


def create_app(
    settings: Settings | None = None,
    readiness_checks: Sequence[ReadinessCheck] = (),
) -> FastAPI:
    """Build the API without initializing future product subsystems."""
    resolved_settings = settings or Settings()
    readiness_registry = ReadinessRegistry((application_bootstrap_check, *readiness_checks))

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        configure_logging(str(resolved_settings.environment), resolved_settings.log_level)
        app.state.lifecycle_state = "started"
        logger.info(
            "application started", extra={"environment": str(resolved_settings.environment)}
        )
        try:
            yield
        finally:
            app.state.lifecycle_state = "stopped"
            logger.info(
                "application stopped", extra={"environment": str(resolved_settings.environment)}
            )

    app = FastAPI(
        title="RITRON AI API",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
    )
    app.state.settings = resolved_settings
    app.state.readiness_registry = readiness_registry
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(resolved_settings.cors_origins),
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["X-Request-ID"],
    )
    _register_middleware(app)
    _register_exception_handlers(app)
    _register_routes(app)
    return app


def _register_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_context(request: Request, call_next: RequestResponseEndpoint) -> Response:
        candidate = request.headers.get("X-Request-ID", "")
        request_id = candidate if REQUEST_ID_PATTERN.fullmatch(candidate) else str(uuid.uuid4())
        token = request_id_context.set(request_id)
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            request_id_context.reset(token)


def _register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = "not_found" if exc.status_code == 404 else "http_error"
        message = (
            "The requested resource was not found" if exc.status_code == 404 else "Request failed"
        )
        return _error_response(exc.status_code, code, message)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return _error_response(
            422, "validation_error", "Request validation failed", {"errors": exc.errors()}
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(request: Request, error: Exception) -> JSONResponse:
        logger.exception("unhandled request exception", extra={"event": "request.failed"})
        return _error_response(500, "internal_error", "An internal error occurred")


def _error_response(
    status_code: int,
    code: str,
    message: str,
    details: dict[str, object] | None = None,
) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorBody(code=code, message=message, details=details or {}),
        request_id=request_id_context.get() or "unknown",
        timestamp=datetime.now(UTC),
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump(mode="json"))


def _register_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/health")

    @router.get("/live", response_model=LivenessResponse, tags=["foundation"])
    async def live() -> LivenessResponse:
        return LivenessResponse(timestamp=datetime.now(UTC))

    @router.get("/ready", response_model=ReadinessResponse, tags=["foundation"])
    async def ready(request: Request) -> JSONResponse | ReadinessResponse:
        registry: ReadinessRegistry = request.app.state.readiness_registry
        checks = registry.evaluate()
        response = ReadinessResponse(
            status="ready" if all(check.ready for check in checks) else "not_ready",
            checks=[ReadinessCheckResponse(name=check.name, ready=check.ready) for check in checks],
            timestamp=datetime.now(UTC),
        )
        if response.status == "ready":
            return response
        return JSONResponse(status_code=503, content=response.model_dump(mode="json"))

    app.include_router(router)
