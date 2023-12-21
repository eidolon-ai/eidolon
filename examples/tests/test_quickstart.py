import pytest
from jsonref import requests


@pytest.fixture(scope="module", autouse=True)
def http_server(eidolon_server, eidolon_examples):
    with eidolon_server(eidolon_examples / "quickstart", "-m", "local_dev") as server:
        yield server


def test_can_hit_generic_agent(server_loc):
    response = requests.post(
        f"{server_loc}/agents/hello_world/programs/question",
        json=dict(name="World"),
    )
    assert response.status_code == 200
