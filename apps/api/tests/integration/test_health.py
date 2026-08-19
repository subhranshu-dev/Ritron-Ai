import pytest

from conftest import api_client
from ritron_api.app import create_app
from ritron_api.readiness import ReadinessResult


@pytest.mark.integration
@pytest.mark.anyio
async def test_liveness_reports_an_alive_process() -> None:
    async with api_client(create_app()) as client:
        response = await client.get(
            "/health/live", headers={"X-Request-ID": "test-request-1"}
        )

    assert response.status_code == 200
    assert response.json()["status"] == "alive"
    assert response.headers["X-Request-ID"] == "test-request-1"


@pytest.mark.integration
@pytest.mark.anyio
async def test_readiness_reports_started_application() -> None:
    async with api_client(create_app()) as client:
        response = await client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["checks"] == [{"name": "application", "ready": True}]


@pytest.mark.integration
@pytest.mark.anyio
async def test_readiness_fails_when_a_registered_check_is_unready() -> None:
    app = create_app(
        readiness_checks=[lambda: ReadinessResult(name="future-service", ready=False)]
    )

    async with api_client(app) as client:
        response = await client.get("/health/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"


@pytest.mark.integration
@pytest.mark.anyio
async def test_lifespan_tracks_clean_shutdown() -> None:
    app = create_app()

    async with app.router.lifespan_context(app):
        assert app.state.lifecycle_state == "started"

    assert app.state.lifecycle_state == "stopped"
