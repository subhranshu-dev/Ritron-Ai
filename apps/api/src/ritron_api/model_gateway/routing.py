"""Deterministic, capability-aware model selection."""

from dataclasses import dataclass

from ritron_api.model_gateway.contracts import ModelDescriptor, ModelRequest
from ritron_api.model_gateway.errors import ModelCapabilityError, ModelNotFoundError
from ritron_api.model_gateway.registry import ProviderRegistry


@dataclass(frozen=True)
class RoutingPolicy:
    default_model_id: str | None = None
    fallback_model_ids: tuple[str, ...] = ()


class ModelRouter:
    def __init__(self, registry: ProviderRegistry, policy: RoutingPolicy) -> None:
        self._registry = registry
        self._policy = policy

    def select(self, request: ModelRequest) -> tuple[ModelDescriptor, ...]:
        selected_id = request.model_id or self._policy.default_model_id
        if selected_id is None:
            raise ModelNotFoundError(
                "No model was requested and no default model is configured"
            )
        candidates = (selected_id, *self._policy.fallback_model_ids)
        descriptors = tuple(
            self._registry.get_model(model_id) for model_id in dict.fromkeys(candidates)
        )
        required = request.required_capabilities()
        compatible = tuple(
            model for model in descriptors if required <= model.capabilities
        )
        if not compatible:
            raise ModelCapabilityError(
                "No configured candidate supports the requested capabilities",
                safe_details={
                    "required_capabilities": sorted(
                        capability.value for capability in required
                    )
                },
            )
        return compatible
