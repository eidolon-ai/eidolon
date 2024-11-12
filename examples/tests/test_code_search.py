from jsonref import requests
from pytest_asyncio import fixture

from eidolon_ai_sdk.system.resources.resources_base import load_resources
from eidolon_ai_sdk.test_utils.server import serve_thread


@fixture(scope="module", autouse=True)
def server(machine, eidolon_examples):
    resources = load_resources([eidolon_examples / "code_search" / "resources"])
    with serve_thread([machine, *resources]):
        yield


def test_server_is_running(server_loc):
    response = requests.get(f"{server_loc}/openapi.json")
    assert response.status_code == 200
    assert "/processes/{process_id}/agent/doc_producer/actions/converse" in response.json()["paths"]
