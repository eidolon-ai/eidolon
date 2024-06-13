from os import environ

import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.api_agent import APIAgent, APIAgentSpec, Operation
from eidolon_ai_sdk.agent.doc_manager.loaders.s3_loader import S3Loader
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture(scope="module")
def pet_store():
    spec = APIAgentSpec(
        title="Pet Store Agent",
        root_call_url="https://petstore31.swagger.io",
        open_api_location="https://petstore31.swagger.io/api/v31/openapi.json",
        operations_to_expose=[
            Operation(**{
                "name": "get_pets_by_status",
                "description": "Get a pet by Status",
                "path": "/pet/findByStatus",
                "method": "get",
                "result_filters": ["$.name", "$.status", "*.tags[*].name"],
            })
        ],
    )
    return AgentResource(
        apiVersion="eidolon/v1",
        metadata=Metadata(name="PetStoreAgent"),
        spec=Reference(
            implementation=fqn(APIAgent),
            **spec.model_dump()
        ),
    )


@pytest.fixture(scope="module")
async def agent(pet_store, run_app) -> Agent:
    async with run_app(pet_store):
        yield Agent.get("PetStoreAgent")


async def test_get_pets(agent):
    process = await agent.create_process()
    found = await process.action("get_pets_by_status", body={"status": ["available", "pending"]})
    print(found.data)
    assert found.data
