import pytest
from pydantic import ValidationError

from ritron_api.config import Environment, Settings


def test_settings_have_safe_local_defaults() -> None:
    settings = Settings()

    assert settings.environment is Environment.DEVELOPMENT
    assert settings.host == "127.0.0.1"
    assert settings.port == 8000


def test_settings_load_namespaced_environment_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("RITRON_API_PORT", "9001")
    monkeypatch.setenv(
        "RITRON_API_CORS_ORIGINS", "http://localhost:1420,http://localhost:3000"
    )

    settings = Settings()

    assert settings.port == 9001
    assert settings.cors_origins == ("http://localhost:1420", "http://localhost:3000")


@pytest.mark.parametrize(
    ("environment_variable", "value"),
    [
        ("RITRON_API_PORT", "70000"),
        ("RITRON_API_ENVIRONMENT", "invalid"),
        ("RITRON_API_LOG_LEVEL", "verbose"),
        ("RITRON_API_CORS_ORIGINS", ""),
    ],
)
def test_invalid_environment_configuration_is_rejected(
    monkeypatch: pytest.MonkeyPatch, environment_variable: str, value: str
) -> None:
    monkeypatch.setenv(environment_variable, value)

    with pytest.raises(ValidationError):
        Settings()
