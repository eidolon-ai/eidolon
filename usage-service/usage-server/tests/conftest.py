import asyncio

import os

import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from usage_server.endpoints import service
from usage_server.main import app
from usage_client.client import UsageClient

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
    await service.db.delete_many({})
    return UsageClient("http://test", app=app)
