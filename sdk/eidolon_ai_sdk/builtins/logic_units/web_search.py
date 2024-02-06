import os
from contextlib import asynccontextmanager
from typing import List, Optional

# from aiohttp import ClientSession
from bs4 import BeautifulSoup
from httpx import AsyncClient, Timeout
from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel, Field

from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.logger import logger


class SearchResult(BaseModel):
    url: str
    title: str
    description: str


# Requires custom search engine + token setup in google project. See more at https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
class WebSearchConfig(BaseModel):
    cse_id: str = Field(None, desctiption="Google Custom Search Engine Id.")
    cse_token: str = Field(None, desctiption="Google Project dev token, must have search permissions.")
    summarizer: Optional[str] = "BeautifulSoup"


class WebSearch(LogicUnit, Specable[WebSearchConfig]):
    def __init__(self, **kwargs):
        LogicUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)
        self.spec.cse_id = self.spec.cse_id or os.environ["CSE_ID"]
        self.spec.cse_token = self.spec.cse_token or os.environ["CSE_TOKEN"]
        self.jinja_env = Environment(undefined=StrictUndefined)
        if not self.spec.cse_id or not self.spec.cse_token:
            raise ValueError("missing required cse_id or cse_token")

    @asynccontextmanager
    async def _get(self, **kwargs):
        async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
            yield await client.get(**kwargs)

    @llm_function()
    async def go_to_url(self, url: str) -> str:
        """
        Retrieve the html document from a given webpage
        :param url: the url to retrieve.
        :return: the html document.
        """
        async with self._get(url=url) as resp:
            text = resp.text
            if not resp.is_success:
                logger.warning(f"Request to url '{url}' return {resp.status}, {resp.reason}")
                return text
            if self.spec.summarizer == "BeautifulSoup":
                soup = BeautifulSoup(text, "lxml")
                return soup.get_text(separator="\n", strip=True)
            else:
                raise ValueError(f"Summarizer {self.spec.summarizer} not supported")

    @llm_function()
    async def search(
        self,
        term: str,
        num_results: int = 10,
        lang: str = "en",
    ) -> List[SearchResult]:
        """
        Search google and get the results. Cannot return more than 100 results
        :param term: the search query
        :param num_results: the number of results to return (default 10, max 100)
        :param lang: the language to search in (default en)
        :return: A list of SearchResults including url, title, and description
        """
        return [r async for r in self._search_results(term, num_results, lang)]

    async def _search_results(self, term, num_results, lang):
        if num_results > 100:
            raise ValueError("Cannot return more than 100 results")
        escaped_term = term.replace(" ", "+")
        resp = await self._req(escaped_term, num_results, lang)
        if not resp["items"]:
            raise RuntimeError("Error retrieving results")
        for item in resp["items"]:
            yield SearchResult(url=item["link"], title=item["title"], description=item["snippet"])

    async def _req(self, term, results, lang):
        async with self._get(
            url="https://customsearch.googleapis.com/customsearch/v1",
            params={
                "q": term,
                "num": results,  # Prevents multiple requests
                "hl": lang,
                "cx": self.spec.cse_id,
                "key": self.spec.cse_token,
            },
        ) as resp:
            resp.raise_for_status()
            return resp.json()
