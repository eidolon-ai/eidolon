from pytest_asyncio import fixture

from eidolon_ai_client.client import Machine

@fixture(scope="module", autouse=True)
def http_server(eidolon_server, eidolon_examples):
    with eidolon_server(eidolon_examples / "quickstart", "-m", "local_dev", log_file="quickstart_log.txt") as server:
        yield server


async def test_can_hit_generic_agent(server_loc):
    process = await Machine(machine=server_loc).agent("hello_world").create_process()
    response = await process.action("converse", json=dict(name="World"))
    assert "World" in response.data
