"""Pytest fixtures."""

from collections.abc import AsyncIterator

import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from imagen.config import cfg

# Override config settings before loading the app
cfg.testing = True
cfg.lance_table_image += "_test"

from imagen.server.main import app  # noqa: E402


async def clear_database() -> None:
    """Empty the test database."""
    # delete temp database here


@pytest_asyncio.fixture()
async def client() -> AsyncIterator[AsyncClient]:
    """Async server client that handles lifespan and teardown."""
    async with LifespanManager(app):  # noqa SIM117
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as _client:  # type: ignore
            try:
                yield _client
            finally:
                await clear_database(app)
