import json
import logging

from ritron_api.logging import JsonFormatter, redact


def test_redact_removes_sensitive_values_recursively() -> None:
    value = {
        "api_key": "secret-value",
        "nested": {"token": "also-secret", "safe": "value"},
    }

    assert redact(value) == {
        "api_key": "[REDACTED]",
        "nested": {"token": "[REDACTED]", "safe": "value"},
    }


def test_json_formatter_redacts_extra_fields() -> None:
    record = logging.makeLogRecord(
        {
            "name": "ritron",
            "levelno": logging.INFO,
            "levelname": "INFO",
            "msg": "configured",
            "args": (),
            "extra": {"password": "do-not-log"},
        }
    )

    payload = json.loads(JsonFormatter().format(record))

    assert payload["extra"]["password"] == "[REDACTED]"
    assert "do-not-log" not in JsonFormatter().format(record)
