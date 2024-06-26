import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.sql_agent import SqlAgent
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture(scope="module", autouse=True)
async def server(run_app, test_dir):
    async with run_app(Resource(
            apiVersion="eidolon/v1",
            kind="Agent",
            metadata=Metadata(name="SqlAgent"),
            spec=dict(
                implementation=fqn(SqlAgent),
                client=dict(
                    connection_string=f"sqlite+aiosqlite:///{str(test_dir / 'resources' / 'chinook.db')}",
                )
            )
    )) as ra:
        yield ra
    print("done...")


@pytest.fixture()
def agent(server):
    return Agent.get("SqlAgent")


@pytest.fixture()
async def process(agent):
    return await agent.create_process()


async def test_sql_agent(process):
    response = await process.action("query", "what tables are accessible?")
    assert response.data == [['albums'],
                             ['sqlite_sequence'],
                             ['artists'],
                             ['customers'],
                             ['employees'],
                             ['genres'],
                             ['invoices'],
                             ['invoice_items'],
                             ['media_types'],
                             ['playlists'],
                             ['playlist_track'],
                             ['tracks'],
                             ['sqlite_stat1']]
    assert response.state == "idle"
