from pytest_asyncio import fixture

from eidolon_ai_client.client import Machine
from eidolon_ai_sdk.test_utils.server import serve_thread


@fixture(scope="module", autouse=True)
def server(machine, eidolon_examples):
    with serve_thread([machine, eidolon_examples / "group_conversation" / "resources"]):
        yield


async def test_can_cycle(server_loc):
    process = await Machine(machine=server_loc).agent("Coordinator").create_process()
    response = await process.action("start_conversation", json=dict(topic="How about them bengals?"))
    assert "Agent: Bob" in response.data
