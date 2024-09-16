import pytest

from eidolon_ai_client.client import Agent, ProcessStatus
from eidolon_ai_sdk.agent.vectara_agent import VectaraAgent
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture(scope="module")
async def server(run_app):
    async with run_app(AgentResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name="VectaraAgent"),
            spec=Reference(
                implementation=fqn(VectaraAgent),
                corpus_key="black-holes-sample-data"
            ),
    )) as ra:
        yield ra


@pytest.fixture()
def agent(server):
    return Agent.get("VectaraAgent")


async def test_can_create_conversation(agent: Agent):
    process = await agent.create_process()
    response: ProcessStatus = await process.action("converse", body="what is a black hole?")
    assert response.state == "idle"
    assert "A black hole is" in response.data


async def test_can_continue_conversation(agent: Agent):
    process = await agent.create_process()
    process= await process.action("converse", body="what is a black hole?")
    response: ProcessStatus = await process.action("converse", body="Who first proposed the concept?")
    assert response.state == "idle"
    assert "Karl Schwarzschild" in response.data

