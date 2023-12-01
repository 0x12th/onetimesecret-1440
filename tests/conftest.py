import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
from httpx import AsyncClient

from src.main import app as fastapi_app


@pytest.fixture(autouse=True, scope="session")
def run_migrations() -> Generator[Any, None, None]:
    import os

    os.system("alembic upgrade head")  # noqa: S605, S607
    yield
    os.system("alembic downgrade base")  # noqa: S605, S607


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client
