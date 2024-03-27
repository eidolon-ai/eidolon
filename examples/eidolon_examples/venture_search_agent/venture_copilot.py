from typing import List
from fastapi import Body
from pydantic import BaseModel, Field
from eidolon_ai_sdk.agent.agent import register_program, AgentState, Agent as AgentTemplate
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
import asyncio
import requests
from bs4 import BeautifulSoup
from summarizer import Summarizer
from eidolon_ai_client.client import Agent
from eidolon_ai_client.events import (
    SuccessEvent,
    ObjectOutputEvent,
    ErrorEvent,
    BaseStreamEvent,
    StringOutputEvent,
    ToolCall,
    AgentStateEvent,
)
import json

class SummarizeWebsiteBody(BaseModel):
    venture_sites: str = Field(..., description="URL to scrape and summarize")
    investment_thesis: str = Field(..., description="Investment thesis to match against company summaries")

class VentureCopilot(AgentTemplate):
    @register_program()
    async def summarize_websites(self, process_id, input: SummarizeWebsiteBody):
        portfolio_agent = Agent.get("VenturePortfolioAgent")
        companies: List[dict] = await portfolio_agent.run_program("search_portfolio", dict(url=input.venture_sites))

        # Prepare coroutines for both researching the company and analyzing relevancy
        coroutines = [self.research_and_rank_company(company, input.investment_thesis) for company in companies.data["companies"]]
        tasks = [asyncio.create_task(coro) for coro in coroutines]

        # Gather results from all tasks
        company_summaries = await asyncio.gather(*tasks, return_exceptions=True)

        # Process and yield results
        for summary_info in company_summaries:
            # Assuming summary_info is a dictionary that contains a 'data' key among others
            if 'data' in summary_info:
                # Yield or process further only the 'data' part
                yield ObjectOutputEvent(content=summary_info['data'])
            else:
                # Handle the case where 'data' might not be present as expected
                continue

        yield AgentStateEvent(state="idle")

    async def research_company(self, company: dict):
        try:
            response = await Agent.get("CompanyResearcher").run_program("search_company", {"url": company["url"], "company_name": company["name"]})
            return {"name": company["name"], "description": response.data["company_description"]}
        except Exception as e:
            return {"error": str(e), "company": company["name"]}

    async def research_and_rank_company(self, company: dict, investment_thesis: str):
        # Fetch company information
        company_info = await self.research_company(company)
        if 'error' not in company_info:
            # Send information to RelevancyRanker for analysis
            analysis_result = await Agent.get("RelevancyRanker").run_program("analyze", {"company_description": company_info["description"], "investment_thesis": investment_thesis})
            # Combine original company info with analysis results
            company_info.update(analysis_result)
            return company_info
        return company_info