import os

import pytest
import requests

from eidolon_ai_client.client import Agent
from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_client.util.request_context import RequestContext


@pytest.fixture()
def azure_jwt():
    tenant_id = os.environ["AZURE_AD_TENANT_ID"]
    eidolon_application_id = os.environ["AZURE_AD_CLIENT_ID"]
    test_application_id = os.environ["AZURE_AD_TEST_CLIENT_ID"]
    test_application_secret = os.environ["AZURE_AD_TEST_CLIENT_SECRET"]

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": test_application_id,
        "client_secret": test_application_secret,
        "scope": f"openid profile email {eidolon_application_id}/.default",
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    RequestContext.set("Authorization", f"Bearer {response.json()['access_token']}", propagate=True)
    return response.json()


@pytest.fixture(scope="module", autouse=True)
def http_server(eidolon_server, eidolon_examples):
    with eidolon_server(eidolon_examples / "azure_auth_rbac", log_file="azure_auth_rbac.txt") as server:
        yield server


@pytest.fixture
def agent(server_loc, azure_jwt):
    return Agent(machine=server_loc, agent="assistant")


@pytest.mark.asyncio
async def test_azure_functional_permissions(agent):
    """
    This test expects an application with create but not delete functional permissions
    """
    process = await agent.create_process()
    with pytest.raises(AgentError) as e:
        await process.delete()
    assert e.value.status_code == 403
