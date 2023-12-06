from typing import Annotated

from pydantic import Field, BaseModel

from eidos.agent import CodeAgent, register_program, AgentState, register_action
from eidos.cpu.agent_io import UserTextCPUMessage


class IdleStateRepresentation(BaseModel):
    response: str


class AutonomousAgent(CodeAgent):

    @register_program()
    @register_action('idle')
    async def converse(self, question: Annotated[str, Field(description="A question")]) -> AgentState[IdleStateRepresentation]:
        response = await self.cpu_request([UserTextCPUMessage(prompt=question)], IdleStateRepresentation.model_json_schema())
        return AgentState(name="idle", data=IdleStateRepresentation(**response))
