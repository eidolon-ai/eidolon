import httpx
import pytest
from httpx import Client
from jsonref import requests


class TestAgentCommunication:
    @pytest.fixture(scope="module", autouse=True)
    def http_server(self, eidolon_server, eidolon_examples):
        with eidolon_server(eidolon_examples / "getting_started/1_agent_communication", "-m", "local_dev", log_file="1_agent_communication.txt") as server:
            yield server

    def test_can_hit_generic_agent(self, server_loc):
        response = requests.post(
            f"{server_loc}/agents/hello_world/programs/question",
            json=dict(name="Joe Dirt"),
        )
        assert response.status_code == 200
        assert "Joe Dirt" in response.json()["data"]

    def test_can_hit_qa_agent(self, server_loc):
        response = requests.post(
            f"{server_loc}/agents/qa/programs/question"
        )
        assert response.status_code == 200
        assert "Success" in response.json()["data"]


class TestCustomAgents:
    @pytest.fixture(scope="module", autouse=True)
    def http_server(self, eidolon_server, eidolon_examples):
        with eidolon_server(eidolon_examples / "getting_started/2_custom_agents/resources", "-m", "local_dev", log_file="2_custom_agents.txt") as server:
            yield server

    def test_can_hit_generic_agent(self, server_loc):
        response = requests.post(
            f"{server_loc}/agents/hello_world/programs/enter",
            json=dict(name="Joe Dirt"),
        )
        assert response.status_code == 200
        assert "Joe Dirt" in response.json()["data"]

    def test_can_hit_qa_agent(self, server_loc):
        with Client(timeout=httpx.Timeout(120)) as client:
            response = client.post(
                f"{server_loc}/agents/qa/programs/test",
                json="hello_world",
            )
            assert response.status_code == 200
            assert response.json()["data"]["outcome"] == "success"
