from typing import List

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pydantic import Field, BaseModel

from eidos_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidos_sdk.system.reference_model import Specable
from eidos_sdk.util.logger import logger


class SearchResult(BaseModel):
    url: str
    title: str
    description: str


class WebSearchConfig(BaseModel):
    include_images: bool = False
    max_chunk_size: int = 20


class WebSearch(LogicUnit, Specable[WebSearchConfig]):
    @llm_function()
    async def go_to_url(self, url: Field(description="The webpage to retrieve")):
        """
        Retrieve the html document from a given webpage.
        """
        async with ClientSession() as session, session.get(url) as resp:
            if not resp.ok:
                logger.warning(f"Request to url '{url}' return {resp.status}, {resp.reason}")
            # todo, we should see if text or parsed text performs better. Raw html might be more useful for llm
            #  We should also add a summarization option to save context. Settable from config and/or llm tool call
            return await resp.text()

    @llm_function()
    async def search(
            self,
            term: str = Field(description="The search query"),
            num_results: int = Field(10, description="The number of results to return"),
            lang: str = Field("en", description="Language of search"),
    ) -> List[SearchResult]:
        """
        Search google and get the results.
        :return: A list of SearchResults, each including url, title, and description
        """
        return [r async for r in self._search_results(term, num_results, lang)]

    async def _search_results(self, term, num_results, lang):
        escaped_term = term.replace(" ", "+")
        # Fetch
        start = 0
        while start < num_results:
            # Send request
            resp = await self._req(escaped_term, num_results - start, lang, start)

            # Parse
            soup = BeautifulSoup(resp, "html.parser")
            result_block = soup.find_all("div", attrs={"class": "g"})
            for result in result_block:
                # Find link, title, description
                link = result.find("a", href=True)
                title = result.find("h3")
                description_box = result.find(
                    "div", {"style": "-webkit-line-clamp:2"})
                if description_box:
                    description = description_box.text
                    if link and title and description:
                        start += 1
                        yield SearchResult(url=link["href"], title=title.text, description=description)

    async def _req(self, term, results, lang, start):
        async with ClientSession() as session:
            async with session.get("https://www.google.com/search", params={
                "q": term,
                "num": min(results + 2, self.spec.max_chunk_size),  # Prevents multiple requests
                "hl": lang,
                "start": start,
            }) as resp:
                resp.raise_for_status()
                return await resp.text()
