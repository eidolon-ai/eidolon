from typing import Optional

from pydantic import BaseModel, Field

from eidolon_ai_client.events import StringOutputEvent
from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_sdk.builtins.logic_units.web_search import SearchSpec, do_google_search
from eidolon_ai_sdk.system.processes import ProcessDoc
from eidolon_ai_sdk.system.reference_model import Specable


class SearchParams(BaseModel):
    term: str = Field(
        description="The query. Be very explicit and verbose in your question. This is going to a GOOGLE search engine."
    )
    num_results: int = Field(default=10, description="The number of results to return")
    lang: str = Field(default="en", description="The language to search in")
    dateRestrict: Optional[str] = Field(default=None, description="Restrict the search to a specific date range")


class WebSearchAgentSpec(SearchSpec):
    """
    The web search agent uses google to search for a term and return the results.
    """

    pass


class WebSearchAgent(Specable[WebSearchAgentSpec]):
    def __init__(self, **kwargs):
        Specable.__init__(self, **kwargs)

    @register_program()
    async def search(self, process_id, params: SearchParams):
        """
        Search google on the given term and get the results.
        :param process_id:
        :param params: the search params
        :return:
        """
        await ProcessDoc.set_delete_on_terminate(process_id, True)
        date_restrict = self.spec.defaultDateRestrict if self.spec.defaultDateRestrict else params.dateRestrict
        async for result in do_google_search(self.spec, params.term, params.num_results, params.lang, date_restrict):
            yield StringOutputEvent(content=result.model_dump_json() + "\n")
