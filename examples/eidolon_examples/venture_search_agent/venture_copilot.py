import asyncio

import yaml
from fastapi import Body
from pydantic import BaseModel, Field

from eidolon_ai_client.client import Agent, ProcessStatus
from eidolon_ai_client.events import (
    ObjectOutputEvent,
    AgentStateEvent,
)
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent.agent import register_program, Agent as AgentTemplate, register_action
from eidolon_ai_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage


class SummarizeWebsiteBody(BaseModel):
    venture_sites: str = Field(..., description="URL to scrape and summarize")
    investment_thesis: str = Field(..., description="Investment thesis to match against company summaries")


class VentureCopilot(AgentTemplate):
    @register_program()
    async def summarize_websites(self, process_id, input: SummarizeWebsiteBody):
        portfolio_agent = Agent.get("VenturePortfolioAgent")
        companies: ProcessStatus = await portfolio_agent.run_program("search_portfolio", dict(url=input.venture_sites))

        # Prepare coroutines for both researching the company and analyzing relevancy
        coroutines = [self.research_and_rank_company(company, input.investment_thesis) for company in companies.data['companies']]
        tasks = [asyncio.create_task(coro) for coro in coroutines]

        # Gather results from all tasks
        company_summaries = await asyncio.gather(*tasks, return_exceptions=True)

        # Process and yield results
        for summary_info in company_summaries:
            yield ObjectOutputEvent(content=summary_info)

        t = await self.cpu.main_thread(process_id)
        system_prompt = f"You are a helpful agent helping investors find companies to invest in. After research your team has identified the following companies other investors are looking at:\n\n{yaml.dump(company_summaries)}"
        await t.set_boot_messages(prompts=[SystemCPUMessage(prompt=system_prompt)])

        yield AgentStateEvent(state="idle")

    async def research_company(self, company: dict):
        rtn = dict(name=company["name"], category=company["category"])
        try:
            response = await Agent.get("CompanyResearcher").run_program("search_company", {"url": company["url"],
                                                                                           "company_name": company[
                                                                                               "name"]})
            rtn["description"] = response.data["company_description"]
        except Exception as e:
            logger.exception(f"Error researching company {company['name']}")
            rtn["error"] = str(e)
        return rtn

    async def research_and_rank_company(self, company: dict, investment_thesis: str):
        # Fetch company information
        company_info = await self.research_company(company)
        if 'error' not in company_info:
            # Send information to RelevancyRanker for analysis
            analysis_result = await Agent.get("RelevancyRanker").run_program("analyze", {
                "company_description": company_info["description"], "investment_thesis": investment_thesis})
            # Combine original company info with analysis results
            company_info['relevance'] = analysis_result.data['relevancy_score']
        return company_info

    @register_action("idle")
    async def converse(self, process_id, question: str = Body(..., media_type="text/plain")):
        text_message = UserTextCPUMessage(prompt=question)
        thread = await self.cpu.main_thread(process_id)
        async for event in thread.stream_request(prompts=[text_message]):
            yield event
        yield AgentStateEvent(state="idle")

