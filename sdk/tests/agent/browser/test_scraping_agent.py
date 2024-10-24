import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.browser.scraping_agent import WebScrapingAgent, WebScrapeResponse
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture(scope="module")
def scraper_agent(test_dir):
    return AgentResource(
        apiVersion="eidolon/v1",
        metadata=Metadata(name="ScrapingAgent"),
        spec=Reference(
            implementation=fqn(WebScrapingAgent),
            name="sa",
            description="A test retriever agent",
        ),
    )


@pytest.fixture(scope="module")
async def agent(scraper_agent, run_app) -> Agent:
    async with run_app(scraper_agent):
        yield Agent.get("ScrapingAgent")


async def test_get_page_content(agent):
    process = await agent.create_process()
    found = await process.action("getPageContent", body={"url": "https://www.eidolonai.com"})
    # noinspection Pydantic
    found = WebScrapeResponse.model_validate(found.data)
    assert "Eidolon AI" in found.text
    assert "https://www.eidolonai.com/blog" in found.links
