from typing import Literal, Optional

from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function


class SaveCompany(LogicUnit):
    @llm_function(title="Save company information", sub_title="")
    async def save_company_detail_field(self, companyName: str, field: Literal['description', 'stage', 'market_size', 'business_model', 'logo_url', 'other_information', 'founders', 'investors'],
                                        value: str) -> None:
        """
        Used to save information about a company to a database
        :param companyName: The name of the company. This is used to identify the company in the database
        :param field: The field to save the value to. Must one of 'url', 'description', 'stage', 'market_size', 'business_model', 'logo_url', 'other_information', 'founders', 'investors'
        :param value: The value to set the field to
        :return:
        """
        process_id = RequestContext.get("process_id")
        print(f"Saving {field} to {value} for {companyName}, process_id: {process_id}")
        await AgentOS.symbolic_memory.update_many("venture_agent_companies",
                                                  {"researched_details.process_id": process_id, "name": companyName},
                                                  {
                                                      '$set': {
                                                          f"researched_details.{field}": value
                                                      }
                                                  })


class AddCompany(LogicUnit):
    @llm_function(title="Add a company for research", sub_title="")
    async def add_company(self, companyName: str, category: Optional[str]) -> None:
        """
        Adds a company to the research database
        :param companyName: The name of the company. This is used to identify the company in the database
        :param category: The category of the company
        :return:
        """
        process_id = RequestContext.get("process_id")
        await AgentOS.symbolic_memory.insert_one("venture_agent_companies",
                                                 {"name": companyName, "category": category, "process_id": process_id})
