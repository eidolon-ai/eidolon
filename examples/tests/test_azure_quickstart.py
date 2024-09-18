import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.system.resources.resources_base import load_resources
from eidolon_ai_sdk.test_utils.machine import TestMachine
from eidolon_ai_sdk.test_utils.server import serve_thread


@pytest.fixture(scope="module")
def machine(tmp_path_factory):
    return TestMachine(tmp_path_factory.mktemp("test_utils_storage"))


@pytest.fixture(scope="module", autouse=True)
def server(eidolon_examples, machine):
    resources = load_resources(eidolon_examples / "azure_quickstart" / "resources")
    with serve_thread([machine, *resources]):
        yield


async def test_can_hit_generic_agent(server_loc):
    process = await Agent.get("hello-world").create_process()
    response = await process.action("converse", json="what is the capital of france?")
    assert "paris" in response.data.lower()
