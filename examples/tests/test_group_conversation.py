from jsonref import requests
from pytest_asyncio import fixture

from eidolon_ai_client.client import Machine


@fixture(scope="module", autouse=True)
def http_server(eidolon_server, eidolon_examples):
    with eidolon_server(eidolon_examples / "group_conversation" / "resources", log_file="group_conversation.txt") as server:
        yield server


async def test_can_cycle(server_loc, http_server):
    process = await Machine(machine=server_loc).agent("Coordinator").create_process()
    response = await process.action("start_conversation", json=dict(topic="How about them bengals?"))
    assert "Agent: Bob" in response.data
