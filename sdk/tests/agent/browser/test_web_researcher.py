import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.browser.scraping_agent import WebScrapingAgent
from eidolon_ai_sdk.agent.browser.search_agent import WebSearchAgent
from eidolon_ai_sdk.agent.browser.web_researcher import WebResearcher
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


class TestWebResearcher:
    @pytest.fixture(scope="class")
    def scraper_agent(self, test_dir):
        return AgentResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name="ScrapingAgent"),
            spec=Reference(
                implementation=fqn(WebScrapingAgent),
            ),
        )

    @pytest.fixture(scope="class")
    def search_agent(self, test_dir):
        return AgentResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name="WebSearchAgent"),
            spec=Reference(
                implementation=fqn(WebSearchAgent),
            ),
        )

    @pytest.fixture(scope="class")
    def researcher_agent(self, test_dir):
        return AgentResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name="WebResearcher"),
            spec=Reference(
                implementation=fqn(WebResearcher),
                search_agent="WebSearchAgent",
                scraping_agent="ScrapingAgent",
            ),
        )

    @pytest.fixture(scope="class")
    async def agent(self, scraper_agent, search_agent, researcher_agent, run_app) -> Agent:
        async with run_app(scraper_agent, search_agent, researcher_agent):
            yield Agent.get("WebResearcher")

    async def test_research(self, agent):
        process = await agent.create_process()
        found = await process.action("search", body={"question": "In what county is Morrow Ohio located?"})
        # noinspection Pydantic
        assert "Warren" in found.data

    async def test_research_followup(self, agent):
        process = await agent.create_process()
        found = await process.action("search", body={"question": "In what county is Morrow Ohio located?"})
        # noinspection Pydantic
        assert "Warren" in found.data
        followup = await process.action("followup_question", body={"question": "When was it founded?"})
        assert "1844" in followup.data
