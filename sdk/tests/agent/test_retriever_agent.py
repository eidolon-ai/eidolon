from os import environ

import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.doc_manager.loaders.azure_loader import AzureLoader
from eidolon_ai_sdk.agent.doc_manager.loaders.s3_loader import S3Loader
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
    def retrieverS3(self, test_dir):
        return AgentResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name="RetrieverAgentS3"),
            spec=Reference(
                implementation=fqn(RetrieverAgent),
                name="s3retriever",
                description="A test retriever agent no store",
                document_manager=dict(
                    recheck_frequency=0,
                    loader=dict(
                        implementation=S3Loader.__name__,
                        bucket="rag-search-test",
                        region_name="us-east-2",
                        # these need to be set for cassette to match, but grab them from environ if present to make generating cassettes easier
                        aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID", "foo"),
                        aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY", "bar"),
                    ),
                ),
            ),
        )

    @pytest.fixture(scope="class")
    def retrieverAzure(self, test_dir):
        return AgentResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name="RetrieverAgentAzure"),
            spec=Reference(
                implementation=fqn(RetrieverAgent),
                name="azureretriever",
                description="A test retriever agent no store",
                document_manager=dict(
                    recheck_frequency=0,
                    loader=dict(
                        implementation=AzureLoader.__name__,
                        container="rag-search-test",
                        account_url="https://eidolon.blob.core.windows.net",
                        create_container_on_startup=False,
                    ),
                ),
            ),
        )

    @pytest.fixture(scope="class")
    async def agent(self, retriever, retrieverNoStore, retrieverS3, retrieverAzure, run_app) -> Agent:
        async with run_app(retriever, retrieverNoStore, retrieverS3, retrieverAzure):
            yield Agent.get("RetrieverAgentWithStore")

    async def test_list_files(self, agent):
        process = await agent.create_process()
        found = await process.action("list_files")
        assert set(found.data) == {
            "caz",
            "car",
            "doo",
            "dar",
            "daz",
            "coo",
            "ear",
            "eaz",
            "foo",
            "boo",
            "baz",
            "bar",
            "eoo",
        }

    async def test_search(self, agent):
        process = await agent.create_process()
        found = await process.action("search", body={"question": "foo"})
        assert found.data

    async def test_search_from_read_only_agent(self, agent):
        agentNoStore = Agent.get("RetrieverAgentNoStore")
        process = await agentNoStore.create_process()
        found = await process.action("search", body={"question": "foo"})
        assert found.data

    async def test_s3(self, agent):
        s3_agent = Agent.get("RetrieverAgentS3")
        process = await s3_agent.create_process()
        found = await process.action("search", body={"question": "how do I make a pdf?"})
        assert "Get_Started_With_Smallpdf" in str(found.data)

    async def test_s3_cached_results(self, agent):
        s3_agent = Agent.get("RetrieverAgentS3")
        process = await s3_agent.create_process()
        await process.action("search", body={"question": "how do I make a pdf?"})

        #  will error if there is an issue with syncing docs
        process = await s3_agent.create_process()
        await process.action("search", body={"question": "what about a .exe"})

    async def test_azure(self, agent):
        s3_agent = Agent.get("RetrieverAgentAzure")
        process = await s3_agent.create_process()
        found = await process.action("search", body={"question": "how do I make a pdf?"})
        assert "Get_Started_With_Smallpdf" in str(found.data)

    async def test_azure_cached_results(self, agent):
        s3_agent = Agent.get("RetrieverAgentAzure")
        process = await s3_agent.create_process()
        await process.action("search", body={"question": "how do I make a pdf?"})

        #  will error if there is an issue with syncing docs
        process = await s3_agent.create_process()
        await process.action("search", body={"question": "what about a .exe"})
