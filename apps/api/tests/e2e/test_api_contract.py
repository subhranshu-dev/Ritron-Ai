import pytest

from conftest import api_client
from ritron_api.app import create_app


@pytest.mark.e2e
@pytest.mark.anyio
async def test_unknown_route_uses_the_public_error_contract() -> None:
    async with api_client(create_app()) as client:
        response = await client.get("/api/v1/not-implemented")

    body = response.json()
    assert response.status_code == 404
    assert body["error"] == {
        "code": "not_found",
        "message": "The requested resource was not found",
        "details": {},
        "reference": None,
    }
    assert response.headers["X-Request-ID"] == body["request_id"]
    assert "traceback" not in response.text.lower()
