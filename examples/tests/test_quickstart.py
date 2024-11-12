from pytest_asyncio import fixture

from eidolon_ai_client.client import Machine
from eidolon_ai_sdk.test_utils.server import serve_thread


@fixture(scope="module", autouse=True)
def server(machine, eidolon_examples):
    with serve_thread([machine, eidolon_examples / "quickstart"]):
        yield


async def test_can_hit_simple_agent(server_loc):
    process = await Machine(machine=server_loc).agent("hello_world").create_process()
    response = await process.action("converse", json=dict(name="World"))
    assert "World" in response.data
