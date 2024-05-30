import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


class TestRetrieverAgent:
    @pytest.fixture(scope="class")
    def retriever(self, test_dir):
        docs_loc = test_dir / "agent" / "retriever_docs"
        return AgentResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name="RetrieverAgentWithStore"),
            spec=Reference(
                implementation=fqn(RetrieverAgent),
                name="test_retriever_name",
                description="A test retriever agent",
                loader_root_location=f"file:///{docs_loc}",
            ),
        )

    @pytest.fixture(scope="class")
    def retrieverNoStore(self, test_dir):
        return AgentResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name="RetrieverAgentNoStore"),
            spec=Reference(
                implementation=fqn(RetrieverAgent),
                name="test_retriever_name",
                description="A test retriever agent no store",
            ),
        )

    @pytest.fixture(scope="class")
    async def agent(self, retriever, retrieverNoStore, run_app) -> Agent:
        async with run_app(retriever, retrieverNoStore):
            yield Agent.get("RetrieverAgentWithStore")

    async def test_list_files(self, agent):
        process = await agent.create_process()
        found = await process.action("list_files")
        assert set(found.data) == {"caz", "car", "doo", "dar", "daz", "coo", "ear", "eaz", "foo", "boo", "baz", "bar", "eoo"}

    async def test_search(self, agent):
        process = await agent.create_process()
        found = await process.action("search", body={"question": "foo"})
        assert found.data

    async def test_search_from_read_only_agent(self, agent):
        agentNoStore = Agent.get("RetrieverAgentNoStore")
        process = await agentNoStore.create_process()
        found = await process.action("search", body={"question": "foo"})
        assert found.data
