import pytest

from eidolon_ai_sdk.agent.client import Agent
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture(scope="module")
def retriever(test_dir):
    docs_loc = test_dir / "agent" / "retriever_docs"
    return AgentResource(
        apiVersion="eidolon/v1",
        metadata=Metadata(name="RetrieverAgent"),
        spec=Reference(
            implementation=fqn(RetrieverAgent),
            name="test_retriever_name",
            description="A test retriever agent",
            loader_root_location=f"file:///{docs_loc}",
        ),
    )


@pytest.fixture(scope="module")
async def agent(retriever, run_app):
    async with run_app(retriever):
        yield Agent.get("RetrieverAgent")


async def test_list_files(agent):
    found = await agent.program("list_files")
    assert set(found.data) == {"caz", "car", "doo", "dar", "daz", "coo", "ear", "eaz", "foo", "boo", "baz", "bar", "eoo"}


async def test_search(agent):
    found = await agent.program("search", body={"question": "foo"})
    assert found.data
