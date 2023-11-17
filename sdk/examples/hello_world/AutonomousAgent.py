import asyncio
from asyncio import Queue, Future
from typing import Annotated, Any

from pydantic import Field, BaseModel

from eidolon_sdk.agent import CodeAgent, initializer
from eidolon_sdk.cpu.agent_cpu import AgentCPU, ResponseHandler
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage


class IdleStateRepresentation(BaseModel):
    response: str


class AutonomousAgent(CodeAgent):

    @initializer
    async def execute(self, question: Annotated[str, Field(description="A question")]) -> IdleStateRepresentation:
        response = await self.cpu_request([UserTextCPUMessage(prompt=question)], {}, IdleStateRepresentation.model_json_schema())
        return IdleStateRepresentation(**response)
