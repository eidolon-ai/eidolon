from pydantic import BaseModel

from eidolon_sdk.agent import Agent, initializer, register_action, AgentState
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage
from eidolon_sdk.reference_model import Specable
from eidolon_sdk.util.schema_to_model import schema_to_model


# todo, this probably defines states and output schema, but leaving that out for now
class GenericAgentSpec(BaseModel):
    system_prompt: str
    question_prompt: str
    question_json_schema: dict


class LlmResponse(BaseModel):
    response: str


class GenericAgent(Agent, Specable[GenericAgentSpec]):
    def get_input_model(self, action: str):
        if action == 'INIT':
            return schema_to_model(self.spec.question_json_schema, "InitialQuestionInputModel")
        else:
            return super().get_input_model(action)

    @initializer
    async def question(self, **kwargs) -> AgentState[LlmResponse]:
        schema = LlmResponse.model_json_schema()
        schema['type'] = 'object'
        response = await self.cpu_request(
            [SystemCPUMessage(prompt=self.spec.system_prompt), UserTextCPUMessage(prompt=self.spec.question_prompt)],
            kwargs,
            schema
        )
        response = LlmResponse(**response)
        return AgentState(name='idle', data=response)

    @register_action('idle')
    async def respond(self, statement: str) -> AgentState[LlmResponse]:
        response = await self.cpu_request([UserTextCPUMessage(prompt=statement)], {}, LlmResponse.model_json_schema())
        return AgentState(name='idle', data=response)
