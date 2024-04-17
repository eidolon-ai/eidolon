import asyncio
import pytest
import pytest_asyncio

from eidolon_ai_usage_client.client import UsageClient
from usage_server.server import app
from usage_server.usage import UsageService


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client():
    s = await UsageService.singleton()
    await s.collection.delete_many({})
    return UsageClient("http://test", app=app)
