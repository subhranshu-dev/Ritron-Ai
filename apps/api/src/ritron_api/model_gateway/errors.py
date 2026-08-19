"""Safe, normalized errors at the model execution boundary."""

from enum import StrEnum


class ModelErrorCode(StrEnum):
    AUTHENTICATION = "provider_authentication"
    RATE_LIMIT = "provider_rate_limited"
    TIMEOUT = "provider_timeout"
    UNAVAILABLE = "provider_unavailable"
    MODEL_NOT_FOUND = "model_not_found"
    CAPABILITY = "model_capability_unsupported"
    INVALID_REQUEST = "invalid_model_request"
    EXECUTION = "model_execution_failed"
    CANCELLED = "model_cancelled"


class ModelGatewayError(Exception):
    code = ModelErrorCode.EXECUTION
    retryable = False
    status_code = 502

    def __init__(
        self, message: str, *, safe_details: dict[str, object] | None = None
    ) -> None:
        super().__init__(message)
        self.safe_details = safe_details or {}


class ProviderAuthenticationError(ModelGatewayError):
    code = ModelErrorCode.AUTHENTICATION
    status_code = 502


class ProviderRateLimitError(ModelGatewayError):
    code = ModelErrorCode.RATE_LIMIT
    retryable = True
    status_code = 429


class ProviderTimeoutError(ModelGatewayError):
    code = ModelErrorCode.TIMEOUT
    retryable = True
    status_code = 504


class ProviderUnavailableError(ModelGatewayError):
    code = ModelErrorCode.UNAVAILABLE
    retryable = True
    status_code = 503


class ModelNotFoundError(ModelGatewayError):
    code = ModelErrorCode.MODEL_NOT_FOUND
    status_code = 404


class ModelCapabilityError(ModelGatewayError):
    code = ModelErrorCode.CAPABILITY
    status_code = 422


class InvalidModelRequestError(ModelGatewayError):
    code = ModelErrorCode.INVALID_REQUEST
    status_code = 422


class ModelExecutionError(ModelGatewayError):
    code = ModelErrorCode.EXECUTION
    retryable = True
    status_code = 502


class ModelCancelledError(ModelGatewayError):
    code = ModelErrorCode.CANCELLED
    status_code = 499
