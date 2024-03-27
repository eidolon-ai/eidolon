from typing import List
from fastapi import Body
from pydantic import BaseModel, Field
from eidolon_ai_sdk.agent.agent import register_program, AgentState, Agent as AgentTemplate
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

        coroutines = [self.research_company(company) for company in companies.data["companies"]]
        tasks = [asyncio.create_task(coro) for coro in coroutines]

        company_summaries = await asyncio.gather(*tasks, return_exceptions=True)

        for result in company_summaries:
            if isinstance(result, Exception):
                print(f"Error fetching company summary: {result}")
            else:
                response, name = result
                try:
                    yield ObjectOutputEvent(content={"company": name, "summary": response["company_description"]})
                except (KeyError, json.JSONDecodeError) as e:
                    print(f"Error processing company summary for {name}: {e}")

        yield AgentStateEvent(state="idle")

    async def research_company(self, company: dict):
        try:
            rtn = await Agent.get("CompanyResearcher").run_program("search_company", dict(url=company["url"], company_name=company["name"]))
            return (rtn.data, company["name"])
        except Exception as e:
            print(f"Error fetching company information for {company['name']}: {e}")
            return e