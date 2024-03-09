from typing import Annotated, Optional

from fastapi import Body
from pydantic import Field, BaseModel

from eidolon_ai_sdk.agent.agent import Agent, register_program, AgentSpec
from eidolon_ai_sdk.builtins.logic_units.web_search import WebSearch, WebSearchConfig
from eidolon_ai_sdk.system.reference_model import Specable


class SearchInput(BaseModel):
    query: str = Field(description="The keywords to search for. Include as many search terms that you want to use to find the desired results. The more search terms you include, the more specific the search will be.")
    num_results: int = Field(10, description="The number of search results to return. Limit is 10")


class WebSearchAgentSpec(AgentSpec):
    siteSearch: str = Field(default=None, description="The site to search. This can be a domain or a subdomain.")
    includeSiteSearchSites: Optional[bool] = Field(True, description="Controls whether to include or exclude results from the site specified in siteSearch.")


class WebSearchAgent(Agent, Specable[WebSearchAgentSpec]):
    @register_program()
    async def search(self, search_input: SearchInput):
        """
        This method is used to search for things on LinkedIn. It is useful for finding people, companies, jobs, etc.
        """
        searcher = WebSearch(spec=WebSearchConfig(siteSearch=self.spec.siteSearch), processing_unit_locator=None)
        return await searcher.search(search_input.query, num_results=search_input.num_results)

    @register_program()
    async def go_to_url(self, url: Annotated[str, Body(description="Your name", embed=True)]) -> str:
        """
        This method is used to navigate to a URL. It is useful for navigating to a LinkedIn page and retrieving information.
        """
        searcher = WebSearch(spec=WebSearchConfig(), processing_unit_locator=None)
        return await searcher.go_to_url(url)
