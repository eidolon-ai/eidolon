import pytest

from eidolon_ai_client.client import Machine
from eidolon_ai_sdk.system.resources.resources_base import load_resources
from eidolon_ai_sdk.test_utils.server import serve_thread


class TestAgentCommunication:
    @pytest.fixture(scope="class", autouse=True)
    def http_server(self, eidolon_server, eidolon_examples):
        with eidolon_server(
            eidolon_examples / "getting_started/1_agent_communication",
            "-m",
            "local_dev",
            log_file="1_agent_communication.txt",
        ) as server:
            yield server

    @pytest.fixture(scope="class", autouse=True)
    def server(self, machine, eidolon_examples):
        resources = load_resources([eidolon_examples / "getting_started" / "1_agent_communication"])
        with serve_thread([machine, *resources]):
            yield

    async def test_can_hit_simple_agent(self, server_loc):
        process = await Machine(machine=server_loc).agent("hello_world").create_process()
        response = await process.action("question", body=dict(name="Joe Dirt"))
        assert "Joe Dirt" in response.data

    async def test_can_hit_qa_agent(self, server_loc):
        process = await Machine(machine=server_loc).agent("qa").create_process()
        response = await process.action("question", body=dict(name="Joe Dirt"))
        assert "Success" in response.data


class TestCustomAgents:
    @pytest.fixture(scope="class", autouse=True)
    def server(self, machine, eidolon_examples):
        resources = load_resources([eidolon_examples / "getting_started" / "2_custom_agents" / "resources"])
        with serve_thread([machine, *resources]):
            yield

    async def test_can_hit_simple_agent(self, server_loc):
        process = await Machine(machine=server_loc).agent("hello_world").create_process()
        response = await process.action("enter", body=dict(name="Joe Dirt"))
        assert "Joe Dirt" in response.data

    async def test_can_hit_qa_agent(self, server_loc):
        process = await Machine(machine=server_loc).agent("qa").create_process()
        response = await process.action("test", json="hello_world")
        assert response.data["outcome"].lower() == "success"
