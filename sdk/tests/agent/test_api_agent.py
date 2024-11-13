import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.api_agent import APIAgent, APIAgentSpec, Operation
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture(scope="module")
def processes_resource():
    spec = APIAgentSpec(
        title="Local Agent",
        root_call_url="https://fakerestapi.azurewebsites.net",
        open_api_location="https://fakerestapi.azurewebsites.net/swagger/v1/swagger.json",
        max_response_size=75 * 1024,
        operations_to_expose=[
            Operation(
                **{
                    "name": "get_authors",
                    "path": "/api/v1/Authors",
                    "method": "get",
                }
            )
        ],
    )
    return AgentResource(
        apiVersion="eidolon/v1",
        metadata=Metadata(name="LocalAgent"),
        spec=Reference(implementation=fqn(APIAgent), **spec.model_dump()),
    )


@pytest.fixture(scope="module")
async def agent(processes_resource, run_app) -> Agent:
    async with run_app(processes_resource):
        yield Agent.get("LocalAgent")


async def test_get_authors(agent):
    process = await agent.create_process()
    found = await process.action("get_authors", dict(body={}))
    assert found.data[0] == {"id": 1, "idBook": 1, "firstName": "First Name 1", "lastName": "Last Name 1"}
