import os
from contextlib import asynccontextmanager
from typing import List, Optional, Literal

# from aiohttp import ClientSession
from bs4 import BeautifulSoup
from httpx import AsyncClient, Timeout
from pydantic import BaseModel, Field, model_validator

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable


class SearchResult(BaseModel):
    url: str
    title: str
    description: Optional[str]


class BrowseSpec(BaseModel):
    summarizer: Literal["BeautifulSoup", "noop"] = "BeautifulSoup"


class Browser(LogicUnit, Specable[BrowseSpec]):
    def __init__(self, **kwargs):
        LogicUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)

    @llm_function()
    async def go_to_url(self, url: str) -> str:
        """
        Retrieve the html document from a given webpage
        :param url: the url to retrieve.
        :return: the html document.
        """
        async with _get(url=url) as resp:
            text = resp.text
            if not resp.is_success:
                logger.warning(f"Request to url '{url}' return {resp.status_code}")
                return text
            if self.spec.summarizer == "BeautifulSoup":
                soup = BeautifulSoup(text, "lxml")
                for a in soup.findAll("a"):
                    a.replace_with(a.text + f" {a.get('href')}")
                return soup.get_text(separator="\n", strip=True)
            elif self.spec.summarizer == "noop":
                return text
            else:
                raise ValueError(f"Summarizer {self.spec.summarizer} not supported")


# Requires custom search engine + token setup in google project. See more at https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
class SearchSpec(BaseModel):
    cse_id: str = Field(
        default_factory=lambda: os.environ["CSE_ID"],
        validate_default=True,
        desctiption="Google Custom Search Engine Id.",
    )
    cse_token: str = Field(
        default_factory=lambda: os.environ["CSE_TOKEN"],
        validate_default=True,
        desctiption="Google Project dev token, must have search permissions.",
    )
    name: str = "search"
    description: str = None
    defaultDateRestrict: Optional[str] = None
    params: Optional[dict] = {}

    @model_validator(mode="after")
    def _validate(self):
        if not self.description:
            self.description = (
                f"Search google on {self.params['siteSearch']} and get the results."
                if "siteSearch" in self.params
                else "Search google and get the results."
            )
        return self


class Search(LogicUnit, Specable[SearchSpec]):
    def __init__(self, **kwargs):
        LogicUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)
        setattr(self, "search", llm_function(name=self.spec.name, description=self.spec.description)(self._search()))

    def _search(self):
        if "dateRestrict" in self.spec.params:

            async def fn(self_, term: str, num_results: int = 10, lang: str = "en") -> List[SearchResult]:
                return [
                    r async for r in self_._search_results(term, num_results, lang, self.spec.params["dateRestrict"])
                ]
        else:

            async def fn(
                self_,
                term: str,
                num_results: int = 10,
                lang: str = "en",
                dateRestrict: Optional[str] = self.spec.defaultDateRestrict,
            ) -> List[SearchResult]:
                return [r async for r in self_._search_results(term, num_results, lang, dateRestrict)]

        return fn

    async def _search_results(self, term, num_results, lang, date_restrict):
        if num_results > 100:
            raise ValueError("Cannot return more than 100 results")
        escaped_term = term.replace(" ", "+")
        resp = await self._req(escaped_term, num_results, lang, date_restrict)
        items = []
        if "items" in resp:
            items = resp["items"]
        for item in items:
            yield SearchResult(url=item["link"], title=item["title"], description=item.get("snippet"))

    async def _req(self, term, results, lang, date_restrict):
        params = {
            "q": term,
            "num": results,  # Prevents multiple requests
            "hl": lang,
            "cx": self.spec.cse_id,
            "key": self.spec.cse_token,
        }
        if date_restrict:
            params["dateRestrict"] = date_restrict
        params.update(self.spec.params)

        async with _get(url="https://customsearch.googleapis.com/customsearch/v1", params=params) as resp:
            resp.raise_for_status()
            return resp.json()


class WebSearchConfig(SearchSpec, BrowseSpec):
    pass


class WebSearch(Specable[WebSearchConfig], LogicUnit):
    parts: List[LogicUnit]

    def __init__(self, **kwargs):
        LogicUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)
        self.parts = [Browser(**kwargs), Search(**kwargs)]

    async def build_tools(self, call_context: CallContext) -> List[FnHandler]:
        acc = []
        for part in self.parts:
            acc.extend(await part.build_tools(call_context))
        return acc


@asynccontextmanager
async def _get(**kwargs):
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        yield await client.get(**kwargs, follow_redirects=True)
