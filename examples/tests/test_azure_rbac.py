import os

import pytest
import requests
from jose import jwt

from eidolon_ai_client.client import Agent
from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_client.util.request_context import RequestContext


@pytest.fixture()
def azure_jwt():
    # todo, I need to add some permissions to the application jwt in azure so I can use it for test. Might create different applicaiton token for this vs ui
    url = f"https://login.microsoftonline.com/{os.environ['AZURE_AD_TENANT_ID']}/oauth2/v2.0/token"
    client_id = os.environ["AZURE_AD_CLIENT_ID"]
    client_secret = os.environ["AZURE_AD_CLIENT_SECRET"]
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": f"openid profile email {client_id}/.default"
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
async def test_get_azure_jwt(agent):
    process = await agent.create_process()
    with pytest.raises(AgentError) as e:
        await process.delete()
    assert e.value.status_code == 403
