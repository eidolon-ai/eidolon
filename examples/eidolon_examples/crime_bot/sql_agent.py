from jinja2 import Environment, StrictUndefined

from eidolon_ai_sdk.agent.agent import Agent, AgentSpec, register_program
from eidolon_ai_sdk.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.logger import logger


class SqlAgentSpec(AgentSpec):
    system_prompt: str
    user_prompt: str
    extra_template_args: dict = {}


class SqlAgent(Agent, Specable[SqlAgentSpec]):
    @register_program()
    async def execute(self, process_id, query: str):
        """
        execute sql query from natural language
        :param process_id:
        :param query:
        :return:
        """
        env = Environment(undefined=StrictUndefined)
        system_prompt = env.from_string(self.spec.system_prompt).render(query=query, **self.spec.extra_template_args)
        user_prompt = env.from_string(self.spec.user_prompt).render(query=query, **self.spec.extra_template_args)

        llm_thread = await self.cpu.main_thread(process_id)
        response_text = await llm_thread.run_request(
            [SystemCPUMessage(prompt=system_prompt), UserTextCPUMessage(prompt=user_prompt)]
        )
        response_text = response_text.replace("```SQL", "").replace("```", "").strip()
        start_idx = response_text.find("SELECT")
        sql_query = response_text[start_idx:] if start_idx != -1 else response_text
        sql_query = sql_query.rstrip(';').strip()
        logger.info(sql_query)
#         todo actually execute sql
        return sql_query
