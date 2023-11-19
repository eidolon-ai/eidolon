import asyncio
from asyncio import Queue, Future
from typing import Annotated, Any

from pydantic import Field, BaseModel

from eidolon_sdk.agent import CodeAgent, initializer, AgentState, register_action
from eidolon_sdk.cpu.agent_cpu import AgentCPU, ResponseHandler
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage


class IdleStateRepresentation(AgentState):
    name: str = "idle"
    response: str


class AutonomousAgent(CodeAgent):

    @initializer
    @register_action('idle')
    async def converse(self, question: Annotated[str, Field(description="A question")]) -> IdleStateRepresentation:
        response = await self.cpu_request([UserTextCPUMessage(prompt=question)], {}, IdleStateRepresentation.model_json_schema())
        return IdleStateRepresentation(**response)
