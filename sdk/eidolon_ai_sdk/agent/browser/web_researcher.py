from textwrap import dedent
from typing import Annotated

from fastapi import Body
from pydantic import BaseModel, Field

from eidolon_ai_client.events import AgentStateEvent
from eidolon_ai_sdk.agent.agent import register_program, register_action
from eidolon_ai_sdk.apu.agent_io import UserTextAPUMessage, SystemAPUMessage
from eidolon_ai_sdk.apu.agents_logic_unit import AgentsLogicUnit, AgentsLogicUnitSpec
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Specable


class WebResearcherSpec(BaseModel):
    apu: AnnotatedReference[APU]

    search_agent: str = Field(description="The agent to use for searching")
    scraping_agent: str = Field(description="The agent to use for scraping")

    system_prompt: str = Field(
        dedent("""You have many tools available to you to help you find the information you need. Only use the relevant tools for the task at hand.
        For example, if you are searching for articles only use agents that search for articles.
      
        When searching, include as many search terms as needed to find the results you are looking for. Be very terse in the query parameters to get the best results.
        The search engine is google so you can use the same search operators you would use on google.
        Don't limit the results from the search as the first answer might not be the best answer.
        
        Let's start by thinking through the problem. For example:
          USER: "What is the capital of France?"
          PLAN:
            - Determine what the user is asking for. In this case, the capital of France.
            - ADD information to the user query if needed.
            - SEARCH: Use the search tool to find the answer. Include EVERYTHING from the user query plus any additional information.
            - SCRAPE: Use the scraping tool to get the full content of the page. Make sure you get the full contents.
            - FOLLOW: Follow links if needed.
            - RETURN: Return the answer and the source of the information.
          
        Let's think through step by step. Explain what you are going to do then call the tools to get it done all in the same cycle.
        """),
        description="The prompt to use for the system to ask the user for input"
    )
    system_prompt_postamble: str = Field("", description="A prompt to include after the system prompt. This is suitable for things like limiting the results to a topic")


class WebResearcher(Specable[WebResearcherSpec]):
    apu: APU

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apu = self.spec.apu.instantiate()
        self.apu.logic_units.append(
            AgentsLogicUnit(
                processing_unit_locator=self.apu,
                spec=AgentsLogicUnitSpec(agents=[self.spec.search_agent, self.spec.scraping_agent]),
            )
        )

    @register_program()
    async def search(self, process_id,
                     question: Annotated[str, Body(description="The query. This can include instructions on date ranges, topics, sites to limit to, etc...", embed=True)]):
        """
        This program will search for the given query. The question can include instructions on date ranges, topics, sites to limit to, etc...
        This method should be used to create a new search. Use it if this is a new topic or a different topic than a previous search.
        :param process_id:
        :param question:
        :return:
        """
        text_message = UserTextAPUMessage(prompt=question)
        thread = await self.apu.main_thread(process_id)
        system_messages = [SystemAPUMessage(prompt=self.spec.system_prompt)]
        if self.spec.system_prompt_postamble:
            system_messages.append(SystemAPUMessage(prompt=self.spec.system_prompt_postamble))

        await thread.set_boot_messages(system_messages)
        async for event in thread.stream_request(prompts=[text_message]):
            yield event
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def followup_question(self, process_id,
                                question: Annotated[
                                    str, Body(description="The query. This can include instructions on date ranges, topics, sites to limit to, etc...", embed=True)]):
        """
        This action will ask a followup question. This is used to ask for more information about a prior search.
        :param process_id:
        :param question:
        :return:
        """
        text_message = UserTextAPUMessage(prompt=question)
        thread = await self.apu.main_thread(process_id)

        async for event in thread.stream_request(prompts=[text_message]):
            yield event
        yield AgentStateEvent(state="idle")
