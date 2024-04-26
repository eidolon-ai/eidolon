from typing import Optional, List, cast, Annotated

from fastapi import Body
from pydantic import BaseModel, Field

from eidolon_ai_client.client import Agent, ProcessStatus
from eidolon_ai_client.events import (
    ObjectOutputEvent,
    AgentStateEvent,
)
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.stream_collector import merge_streams
from eidolon_ai_sdk.agent.agent import register_program, Agent as AgentTemplate, register_action
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.agent_io import UserTextAPUMessage


class SummarizeWebsiteBody(BaseModel):
    venture_sites: str = Field(..., description="URL to scrape and summarize")


class CompanyDetails(BaseModel):
    description: str
    stage: str
    market_size: str
    business_model: str
    logo_url: str
    relevance: Optional[float] = None
    other_information: Optional[str] = None


class Company(BaseModel):
    name: str
    url: str
    should_research: bool = Field(default=False, description="Whether the company should be researched")
    category: Optional[str]
    researched_details: Optional[CompanyDetails] = None
    error: Optional[str] = None


# todo: Add parent process id so calls are nested

class VentureCopilot(AgentTemplate):
    @register_program()
    async def find_companies(self, process_id, venture_site: Annotated[str, Body(description="The URL of the venture site to scrub", embed=True)]):
        portfolio_agent = Agent.get("VenturePortfolioAgent")
        companies_process: ProcessStatus = await portfolio_agent.run_program("search_portfolio", dict(url=venture_site))
        companies = cast(List[dict], companies_process.data['companies'])
        for company in companies:
            company['process_id'] = process_id

        await AgentOS.symbolic_memory.insert("venture_agent_companies", companies)

        yield ObjectOutputEvent(content=await self._loadCompanies(process_id))
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def get_companies(self, process_id):
        yield ObjectOutputEvent(content=await self._loadCompanies(process_id))
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def research_company(self, process_id, companyName: Annotated[str, Body(description="Your name", embed=True)]):
        company = await self._loadCompany(process_id, companyName)
        company.error = None

        company = await self.research_and_rank_company(company)
        await AgentOS.symbolic_memory.upsert_one("venture_agent_companies", company.model_dump(), {"process_id": process_id, "name": companyName})
        yield ObjectOutputEvent(content=company)
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def research_more_companies(self, process_id, companyNames: Annotated[List[str], Body(description="List of company names", embed=True)]):

        companies = await self._loadCompanies(process_id)
        companies = [company for company in companies if company.name in companyNames]

        async def research(company):
            company = await self.research_and_rank_company(company)
            await AgentOS.symbolic_memory.upsert_one("venture_agent_companies", company.model_dump(), {"process_id": process_id, "name": company.name})
            yield ObjectOutputEvent(content=company)

        tasks = []
        for company in companies:
            tasks.append(research(company))

        group_size = 5
        task_groups = [tasks[i:i + group_size] for i in range(0, len(tasks), group_size)]
        for tasks in task_groups:
            combined_calls = merge_streams(tasks)
            async for event in combined_calls:
                yield event

        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def mark_companies_for_research(self, process_id, companies: Annotated[List[str], Body(description="Your name", embed=True)]):
        loaded_companies = await self._loadCompanies(process_id)
        for company in loaded_companies:
            company.should_research = False

        companies = [company for company in loaded_companies if company.name in companies]
        for company in companies:
            company.should_research = True

        for company in loaded_companies:
            await AgentOS.symbolic_memory.upsert_one("venture_agent_companies", company.model_dump(), {"process_id": process_id, "name": company.name})

        yield ObjectOutputEvent(content=loaded_companies)
        yield AgentStateEvent(state="idle")

    async def _loadCompanies(self, process_id):
        companies = []
        async for company in AgentOS.symbolic_memory.find("venture_agent_companies", {"process_id": process_id}):
            company.pop("_id")
            companies.append(Company.model_validate(company))
        return companies

    async def _loadCompany(self, process_id, name: str):
        company = await AgentOS.symbolic_memory.find_one("venture_agent_companies", {"process_id": process_id, "name": name})
        if company:
            company.pop("_id")
            return Company.model_validate(company)
        return None

    async def _research_company(self, company: Company):
        try:
            response = await Agent.get("CompanyResearcher").run_program(
                "search_company",
                {"url": company.url, "company_name": company.name},
            )
            if response and response.data:
                details = CompanyDetails.model_validate(response.data)
                return details
            return None
        except Exception as e:
            logger.exception(f"Error researching company {company.name}")
            return str(e)

    async def research_and_rank_company(self, company: Company, ):
        # Fetch company information
        company_info = await self._research_company(company)
        if isinstance(company_info, str):
            # Send information to RelevancyRanker for analysis
            company.researched_details = company_info
        else:
            company.error = company_info

        return company

    @register_action("idle")
    async def converse(self, process_id, question: str = Body(..., media_type="text/plain")):
        text_message = UserTextAPUMessage(prompt=question)
        thread = await self.cpu.main_thread(process_id)
        async for event in thread.stream_request(prompts=[text_message]):
            yield event
        yield AgentStateEvent(state="idle")
