from typing import Annotated

from fastapi import Body
from pydantic import Field, BaseModel

from eidolon_ai_sdk.agent.agent import Agent, register_program
from eidolon_ai_sdk.builtins.logic_units.web_search import WebSearch, WebSearchConfig


class SearchInput(BaseModel):
    query: str = Field(description="The keywords to search for. Include as many search terms that you want to use to find the desired results. The more search terms you include, the more specific the search will be.")
    typeFilter: str = Field(description="The type of search to perform. This can be 'people', 'jobs', 'company', 'pulse', 'posts', or 'events'.")
    num_results: int = Field(25, description="The number of search results to return.")


class LinkedInSearcher(Agent):
    """
    This agent is used to search for people, companies, jobs, etc. on LinkedIn.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @register_program()
    async def search(self, search_input: SearchInput):
        """
        This method is used to search for things on LinkedIn. It is useful for finding people, companies, jobs, etc.
        """
        searcher = WebSearch(spec=WebSearchConfig(siteSearch=f"linkedin.com/{search_input.typeFilter}"), processing_unit_locator=None)
        return await searcher.search(search_input.query, num_results=search_input.num_results)

    @register_program()
    async def go_to_url(self, url: Annotated[str, Body(description="Your name", embed=True)]) -> str:
        """
        This method is used to navigate to a URL. It is useful for navigating to a LinkedIn page and retrieving information.
        """
        searcher = WebSearch(spec=WebSearchConfig(), processing_unit_locator=None)
        print(""" going to URL """, url)
        return await searcher.go_to_url(url)
