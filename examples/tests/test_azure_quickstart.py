import pytest

from eidolon_ai_client.client import Agent


@pytest.fixture(scope="module", autouse=True)
def http_server(eidolon_server, eidolon_examples):
    with eidolon_server(eidolon_examples / "azure_quickstart" / "resources", log_file="azure_quickstart.txt") as server:
        yield server


@pytest.fixture
def agent(server_loc):
    return Agent(machine=server_loc, agent="hello-world")


async def test_can_hit_generic_agent(agent: Agent):
    process = await agent.create_process()
    response = await process.action("converse", json="what is the capital of france?")
    assert "paris" in response.data.lower()
