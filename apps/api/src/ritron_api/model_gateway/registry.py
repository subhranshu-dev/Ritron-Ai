"""Configuration-backed provider and model registry."""

from ritron_api.model_gateway.contracts import ModelDescriptor
from ritron_api.model_gateway.errors import ModelNotFoundError
from ritron_api.model_gateway.provider import ModelProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ModelProvider] = {}
        self._models: dict[str, ModelDescriptor] = {}

    def register(self, provider: ModelProvider) -> None:
        if provider.id in self._providers:
            raise ValueError(f"Provider already registered: {provider.id}")
        self._providers[provider.id] = provider
        for model in provider.list_models():
            if model.id in self._models:
                raise ValueError(f"Model already registered: {model.id}")
            self._models[model.id] = model

    def get_provider(self, provider_id: str) -> ModelProvider:
        try:
            return self._providers[provider_id]
        except KeyError as error:
            raise ModelNotFoundError("Configured provider was not found") from error

    def get_model(self, model_id: str) -> ModelDescriptor:
        try:
            return self._models[model_id]
        except KeyError as error:
            raise ModelNotFoundError("Requested model was not found") from error

    def list_models(self) -> tuple[ModelDescriptor, ...]:
        return tuple(self._models.values())
