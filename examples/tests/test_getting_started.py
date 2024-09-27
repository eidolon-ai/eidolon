import pytest

from eidolon_ai_client.client import Machine


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
    def http_server(self, eidolon_server, eidolon_examples):
        with eidolon_server(
            eidolon_examples / "getting_started/2_custom_agents/resources",
            "-m",
            "local_dev",
            log_file="2_custom_agents.txt",
        ) as server:
            yield server

    async def test_can_hit_simple_agent(self, server_loc):
        process = await Machine(machine=server_loc).agent("hello_world").create_process()
        response = await process.action("enter", body=dict(name="Joe Dirt"))
        assert "Joe Dirt" in response.data

    async def test_can_hit_qa_agent(self, server_loc):
        process = await Machine(machine=server_loc).agent("qa").create_process()
        response = await process.action("test", json="hello_world")
        assert response.data["outcome"].lower() == "success"
