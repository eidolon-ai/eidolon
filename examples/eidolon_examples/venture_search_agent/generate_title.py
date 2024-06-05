from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.apu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.system.processes import ProcessDoc
from eidolon_examples.venture_search_agent.venture_copilot import Thesis


class GenerateTitle(LogicUnit):
    @llm_function()
    async def generate_title(self, title: str) -> str:
        """
        Used to update the title of the thesis
        :param title: The title of the thesis
        :return:
        """
        process_id = RequestContext.get("process_id")
        thesis = await AgentOS.symbolic_memory.find_one("venture_agent_thesis", {"companyFinderPID": process_id})
        thesis.pop("_id")
        thesis = Thesis.model_validate(thesis)
        process_obj = await ProcessDoc.find_one(query={"_id": thesis.parent_process_id})
        await process_obj.update(title=title)
        return f"Title updated successfully to {title}."
