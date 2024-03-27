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
        print(f"Coroutines: {coroutines}")  # Debug log
        print(f"Companies: {companies.data['companies']}")  # Debug log
        tasks = [asyncio.create_task(coro) for coro in coroutines]

        # Gather results from all tasks
        company_summaries = await asyncio.gather(*tasks, return_exceptions=True)
        print(f"Company summaries: {company_summaries}")  # Debug log
        # Process and yield results
        for summary_info in company_summaries:
            print(f"Summary info: {summary_info}")  # Debug log

            # Check if 'data' is present in summary_info
            if 'data' in summary_info:
                print(f"Summary info data: {summary_info['data']}")  # Debug log

                # Separate the URL from the 'data' part if it exists
                data_section = summary_info['data'].copy()  # Copy to safely modify
                url_in_data = data_section.pop('url', None)  # Remove 'url' from 'data' if present

                # Construct a new object to yield
                yield_object = {}

                # Add top-level URL if it's separate and exists, or use the URL from 'data' if present
                if 'url' in summary_info:
                    yield_object['url'] = summary_info['url']
                elif url_in_data:
                    yield_object['url'] = url_in_data

                # Add the modified 'data' section without the URL
                if data_section:
                    yield_object['data'] = data_section

                # Yield the constructed object
                if yield_object:
                    yield ObjectOutputEvent(content=yield_object)
            else:
                # Handle the case where 'data' might not be present as expected
                continue


        yield AgentStateEvent(state="idle")

    async def research_company(self, company: dict):
        try:
            response = await Agent.get("CompanyResearcher").run_program("search_company", {"url": company["url"], "company_name": company["name"]})
            print(f"Fetched company data: {response.data}")  # Debug log
            a = {"url": company["url"], "name": company["name"], "description": response.data["company_description"]}
            print(f"Company info: {a}")  # Debug log
            return {"url": company["url"], "name": company["name"], "description": response.data["company_description"]}
        except Exception as e:
            print(f"Error fetching company data for {company['name']}: {e}")  # Error log
            return {"error": str(e), "company": company["name"]}


    async def research_and_rank_company(self, company: dict, investment_thesis: str):
        # Fetch company information
        company_info = await self.research_company(company)
        print(f"Company info: {company_info}")  # Debug log
        if 'error' not in company_info:
            # Send information to RelevancyRanker for analysis
            analysis_result = await Agent.get("RelevancyRanker").run_program("analyze", {"company_description": company_info["description"], "investment_thesis": investment_thesis})
            # Combine original company info with analysis results
            company_info.update(analysis_result)
            return company_info
        return company_info