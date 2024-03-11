import pytest
from jsonref import requests

from conftest import get_process_id


@pytest.fixture(scope="module", autouse=True)
def http_server(eidolon_server, eidolon_examples):
    with eidolon_server(eidolon_examples / "hello_world" / "resources", log_file="hello_world_log.txt") as server:
        yield server


def test_server_is_running(server_loc):
    response = requests.get(f"{server_loc}/openapi.json")
    assert response.status_code == 200
    assert "/agents/ExampleGeneric/processes/{process_id}/actions/question" in response.json()["paths"]


def test_can_hit_generic_agent(server_loc):
    process_id = get_process_id(server_loc, "ExampleGeneric")
    response = requests.post(
        f"{server_loc}/agents/ExampleGeneric/processes/{process_id}/actions/question",
        json=dict(instruction="Hi! What is the capital of France?"),
    )
    assert response.status_code == 200
    assert "paris" in response.json()["data"].lower()


def test_tool_calls(server_loc):
    process_id = get_process_id(server_loc, "ExampleGeneric")
    # prep with some information to use on the subsequent response to demonstrate is handled well
    response = requests.post(
        f"{server_loc}/agents/ExampleGeneric/processes/{process_id}/actions/question",
        json=dict(instruction="Hi! My name is Luke."),
    )
    response.raise_for_status()
    response2 = requests.post(
        f"{server_loc}/agents/ExampleGeneric/processes/{process_id}/actions/respond",
        json=dict(statement="Please use the HelloWorld tool with my name."),
    )
    response2.raise_for_status()
    assert "Luke" in response2.json()["data"]
