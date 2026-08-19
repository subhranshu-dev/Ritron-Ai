from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@asynccontextmanager
async def api_client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    """Exercise the ASGI contract without a deprecated synchronous test client."""
    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client
