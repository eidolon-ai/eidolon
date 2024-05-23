import os
from typing import Optional, List, Annotated, Dict

from fastapi import Body
from pydantic import BaseModel, Field

from eidolon_ai_client.client import Agent
from eidolon_ai_client.events import (
    ObjectOutputEvent,
    AgentStateEvent,
)
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.stream_collector import merge_streams
from eidolon_ai_sdk.agent.agent import register_program, Agent as AgentTemplate, register_action
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.agent_io import UserTextAPUMessage
from eidolon_ai_sdk.system.processes import ProcessDoc


class SummarizeWebsiteBody(BaseModel):
    venture_sites: str = Field(..., description="URL to scrape and summarize")


class CompanyDetails(BaseModel):
    url: str
    process_id: str
    description: str
    stage: str
    market_size: str
    funding_information: str
    investors: str
    founders: str
    business_model: str
    logo_url: str
    other_information: Optional[str] = None
    references: List[Dict[str, str]]
    enriched_with_harmonic: Optional[bool] = False


class Company(BaseModel):
    name: str
    should_research: bool = Field(default=False, description="Whether the company should be researched")
    category: Optional[str]
    researched_details: Optional[CompanyDetails] = None
    error: Optional[str] = None


class Thesis(BaseModel):
    parent_process_id: str
    companyFinderPID: str


class VentureCopilot(AgentTemplate):
    @register_program()
    async def start_thesis(self, process_id):
        agent = Agent.get("CompanyFinder")
        process = await agent.create_process(process_id)
        thesis = Thesis(parent_process_id=process_id, companyFinderPID=process.process_id)
        await AgentOS.symbolic_memory.insert_one("venture_agent_thesis", thesis.model_dump())
        yield ObjectOutputEvent(content=thesis)
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def generate_title(self, process_id, body: Annotated[str, Body(description="Your name", embed=True)]):
        thesis = await self._loadThesis(process_id)
        agent = Agent.get("CompanyFinder")
        # noinspection Pydantic
        title = (await agent.process(thesis.companyFinderPID).action("generate_title", body)).data
        process_obj = await ProcessDoc.find_one(query={"_id": process_id})
        await process_obj.update(title=title)
        yield ObjectOutputEvent(content=title)
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def get_thesis(self, process_id):
        thesis = await self._loadThesis(process_id)
        print(thesis)
        yield ObjectOutputEvent(content=thesis)
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def get_companies(self, process_id):
        yield ObjectOutputEvent(content=await self._loadCompanies(process_id))
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def research_company(self, process_id, companyName: Annotated[str, Body(description="Your name", embed=True)]):
        thesis = await self._loadThesis(process_id)
        company = await self._loadCompany(process_id, companyName)
        company.error = None

        company = await self.research_and_assign_company(process_id, company)
        await AgentOS.symbolic_memory.upsert_one("venture_agent_companies", company.model_dump(), {"process_id": thesis.companyFinderPID, "name": companyName})
        yield ObjectOutputEvent(content=company)
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def research_more_companies(self, process_id, companyNames: Annotated[List[str], Body(description="List of company names", embed=True)]):
        thesis = await self._loadThesis(process_id)

        companies = await self._loadCompanies(process_id)
        companies = [company for company in companies if company.name in companyNames]

        async def research(company):
            company = await self.research_and_assign_company(process_id, company)
            await AgentOS.symbolic_memory.upsert_one("venture_agent_companies", company.model_dump(), {"process_id": thesis.companyFinderPID, "name": company.name})
            yield ObjectOutputEvent(content=company)

        async for event in self._run_tasks(research, companies):
            yield event

        yield AgentStateEvent(state="idle")

    async def _run_tasks(self, fn, args):
        tasks = []
        for arg in args:
            tasks.append(fn(arg))
        group_size = 5
        task_groups = [tasks[i:i + group_size] for i in range(0, len(tasks), group_size)]
        for tasks in task_groups:
            combined_calls = merge_streams(tasks)
            async for event in combined_calls:
                yield event

    @register_action("idle")
    async def mark_companies_for_research(self, process_id, companies: Annotated[List[str], Body(description="Your name", embed=True)]):
        thesis = await self._loadThesis(process_id)
        loaded_companies = await self._loadCompanies(process_id)
        for company in loaded_companies:
            company.should_research = False

        companies = [company for company in loaded_companies if company.name in companies]
        for company in companies:
            company.should_research = True

        for company in loaded_companies:
            await AgentOS.symbolic_memory.upsert_one("venture_agent_companies", company.model_dump(), {"process_id": thesis.companyFinderPID, "name": company.name})

        yield ObjectOutputEvent(content=loaded_companies)
        yield AgentStateEvent(state="idle")

    async def _loadCompanies(self, process_id):
        thesis = await self._loadThesis(process_id)
        companies = []
        async for company in AgentOS.symbolic_memory.find("venture_agent_companies", {"process_id": thesis.companyFinderPID}):
            company.pop("_id")
            companies.append(Company.model_validate(company))
        return companies

    async def _loadThesis(self, process_id):
        thesis = await AgentOS.symbolic_memory.find_one("venture_agent_thesis", {"parent_process_id": process_id})
        thesis.pop("_id")
        return Thesis.model_validate(thesis)

    async def _loadCompany(self, process_id, name: str):
        thesis = await self._loadThesis(process_id)
        company = await AgentOS.symbolic_memory.find_one("venture_agent_companies", {"process_id": thesis.companyFinderPID, "name": name})
        if company:
            company.pop("_id")
            return Company.model_validate(company)
        return None

    # noinspection Pydantic
    async def _research_company(self, process_id: str, company: Company):
        try:
            agent = Agent.get("CompanyResearcher")
            process = await agent.create_process(process_id)
            response = await process.action(
                "search_company",
                {"company_name": company.name},
            )
            if response and response.data:
                details = CompanyDetails.model_validate({"process_id": process.process_id, **response.data})
                return details
            return None
        except Exception as e:
            logger.exception(f"Error researching company {company.name}")
            return str(e)

    async def research_and_assign_company(self, process_id: str, company: Company, ):
        # Fetch company information
        company_info = await self._research_company(process_id, company)
        if not isinstance(company_info, str):
            company.researched_details = company_info
            if os.environ.get("HARMONIC_API_KEY"):
                company.researched_details.enriched_with_harmonic = True
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
