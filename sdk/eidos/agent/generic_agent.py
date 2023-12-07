from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel

from eidos.agent.agent import Agent, register_program, register_action, AgentState, AgentSpec, SpecRef
from eidos.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage
from eidos.system.reference_model import Specable


# todo, this probably defines states and output schema, but leaving that out for now
class GenericAgentSpec(AgentSpec):
    system_prompt: str
    question_prompt: str
    question_json_schema: dict


class LlmResponse(BaseModel):
    response: str


class GenericAgent(Agent, Specable[GenericAgentSpec]):
    @register_program(input_model=SpecRef.question_json_schema)
    async def question(self, process_id, **kwargs) -> AgentState[LlmResponse]:
        schema = LlmResponse.model_json_schema()
        schema['type'] = 'object'

        env = Environment(undefined=StrictUndefined)
        await self.cpu.main_thread(process_id).set_boot_messages(
            SystemCPUMessage(prompt=(env.from_string(self.spec.system_prompt).render(**kwargs)))
        )
        response = await self.cpu.main_thread(process_id).schedule_request(
            prompts=[UserTextCPUMessage(prompt=(env.from_string(self.spec.question_prompt).render(**kwargs)))],
            output_format=schema
        )
        response = LlmResponse(**response)
        return AgentState(name='idle', data=response)

    @register_action('idle')
    async def respond(self, process_id, statement: str) -> AgentState[LlmResponse]:
        response = await self.cpu.main_thread(process_id).schedule_request([UserTextCPUMessage(prompt=statement)], LlmResponse.model_json_schema())
        return AgentState(name='idle', data=response)
