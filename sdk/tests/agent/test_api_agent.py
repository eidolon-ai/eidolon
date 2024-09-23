import os

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
        root_call_url="https://openlibrary.org",
        open_api_location="https://openlibrary.org/static/openapi.json",
        operations_to_expose=[
            Operation(
                **{
                    "name": "get_books",
                    "path": "/api/books",
                    "method": "get",
                    "extra_query_params": {"format": "{{ENV_FORMAT}}"},
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


async def test_get_processes(agent):
    process = await agent.create_process()
    os.environ["ENV_FORMAT"] = "json"
    found = await process.action("get_books", {"bibkeys": "OCLC:263296519"})
    assert found.data.get("OCLC:263296519") is not None
