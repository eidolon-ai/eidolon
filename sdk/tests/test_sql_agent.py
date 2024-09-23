import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.sql_agent.agent import SqlAgent
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture(scope="module", autouse=True)
async def server(run_app, test_dir):
    async with run_app(
        sqlagent(
            "SqlAgent",
            client=dict(connection_string=f"sqlite+aiosqlite:///{str(test_dir / 'resources' / 'chinook.db')}"),
        ),
        sqlagent(
            "BrokenSqlAgent", client=dict(connection_string=f"sqlite:///{str(test_dir / 'resources' / 'chinook.db')}")
        ),
    ) as ra:
        yield ra


def sqlagent(name: str, **kwargs):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=name),
        spec=dict(implementation=fqn(SqlAgent), **kwargs),
    )


@pytest.fixture()
def agent(server):
    return Agent.get("SqlAgent")


@pytest.fixture()
async def process(agent):
    return await agent.create_process()


async def test_sql_agent(process):
    response = await process.action("query", dict(message="what tables are accessible?"))
    assert "albums" in response.data
    assert "artists" in response.data
    assert "customers" in response.data
    assert "employees" in response.data
    assert "genres" in response.data
    assert "invoice_items" in response.data
    assert "invoices" in response.data
    assert "media_types" in response.data
    assert "tracks" in response.data
    assert "playlist_track" in response.data
    assert "playlists" in response.data
    assert response.state == "idle"


async def test_sql_agent_data_query(process):
    response = await process.action(
        "query", dict(message="how may albums are in the database?", allow_conversation=False)
    )
    assert response.data == [347]


async def test_sync_connection_error():
    agent = Agent.get("BrokenSqlAgent")
    process = await agent.create_process()
    with pytest.raises(Exception) as e:
        await process.action("query", dict(message="how may albums are in the database?"))
    assert "invalid connection_string" in e.value.message
