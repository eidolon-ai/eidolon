import os

import pytest
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from eidolon_sdk.impl.mongo_symbolic_memory import MongoSymbolicMemory, MongoSymbolicMemoryConfig


@pytest.fixture()
async def symbolic_memory():
    # Setup unique database for test suite
    print("In fixture")
    database_name = f"test_db_{ObjectId()}"  # Unique name for test database
    memory = MongoSymbolicMemory(MongoSymbolicMemoryConfig(mongo_database_name=database_name))
    memory.start()
    yield memory
    memory.stop()
    # Teardown: drop the test database
    connection_string = os.getenv('MONGO_CONNECTION_STRING')
    client = AsyncIOMotorClient(connection_string)
    await client.drop_database(database_name)
    client.close()
