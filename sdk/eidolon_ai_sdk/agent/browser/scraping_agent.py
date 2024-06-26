from typing import Literal, Annotated, Any, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from fastapi import Body
from playwright.async_api import async_playwright
from pydantic import BaseModel

from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.system.processes import ProcessDoc
from eidolon_ai_sdk.system.reference_model import Specable


class WebScrapeResponse(BaseModel):
    text: str
    links: List[str]
    images: List[str]


class WebScrapingAgentSpec(BaseModel):
    """
    The web scraping agent uses playwright to scrape a webpage and return the text, links and images.
    """
    summarizer: Literal["BeautifulSoup", "noop"] = "BeautifulSoup"


class WebScrapingAgent(Specable[WebScrapingAgentSpec]):
    def __init__(self, **kwargs):
        Specable.__init__(self, **kwargs)

    def scrape_page(self, page: Any, text: str):
        if self.spec.summarizer == "BeautifulSoup":
            soup = BeautifulSoup(text, "lxml")
            base_url = page.url
            anchors = soup.find_all("a")
            links = [urljoin(base_url, anchor.get("href", "")) for anchor in anchors]
            images = [urljoin(base_url, img.get("src", "")) for img in soup.find_all("img") if img.get("src", "")]
            return WebScrapeResponse(text=soup.get_text(separator="\n", strip=True), links=links, images=images)
        elif self.spec.summarizer == "noop":
            return text
        else:
            raise ValueError(f"Summarizer {self.spec.summarizer} not supported")

    @register_program()
    async def getPageContent(self, process_id, url: Annotated[str, Body(description="The URL to get the context of", embed=True)]):
        """
        Get the content of the page at the given URL
        :param process_id:
        :param url:
        :return:
        """
        await ProcessDoc.set_delete_on_terminate(process_id, True)
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            try:
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(url)
                html_content = await page.content()
                return self.scrape_page(page, html_content)
            finally:
                await browser.close()
