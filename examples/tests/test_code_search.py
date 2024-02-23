import pytest
from jsonref import requests


@pytest.fixture(scope="module", autouse=True)
def http_server(eidolon_server, eidolon_examples):
    with eidolon_server(eidolon_examples / "code_search" / "resources", log_file="code_search_log.txt") as server:
        yield server


def test_server_is_running(server_loc):
    response = requests.get(f"{server_loc}/openapi.json")
    assert response.status_code == 200
    assert "/agents/doc_producer/processes/{process_id}/actions/question" in response.json()["paths"]
