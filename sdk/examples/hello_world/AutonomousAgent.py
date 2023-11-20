import asyncio
from asyncio import Queue, Future
from typing import Annotated, Any

from pydantic import Field, BaseModel

from eidolon_sdk.agent import CodeAgent, initializer, AgentState, register_action
from eidolon_sdk.cpu.agent_cpu import AgentCPU, ResponseHandler
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage


class IdleStateRepresentation(BaseModel):
    response: str


class AutonomousAgent(CodeAgent):

    @initializer
    @register_action('idle')
    async def converse(self, question: Annotated[str, Field(description="A question")]) -> AgentState[IdleStateRepresentation]:
        response = await self.cpu_request([UserTextCPUMessage(prompt=question)], {}, IdleStateRepresentation.model_json_schema())
        print("response: ", response)
        return AgentState(name="idle", data=IdleStateRepresentation(**response))
