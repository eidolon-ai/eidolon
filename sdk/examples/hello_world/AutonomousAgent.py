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
        process_id = self.get_context().process_id

        f = Future()
        class AAResponseHandler(ResponseHandler):
            async def handle(self, process_id: str, response: dict[str, Any]):
                print("here")
                print(response)
                f.set_result(IdleStateRepresentation.model_validate(response))

        agent_cpu = AgentCPU(self.agent_machine)
        await agent_cpu.start(AAResponseHandler())
        agent_cpu.schedule_request(process_id, [UserTextCPUMessage(prompt=question)], {}, IdleStateRepresentation.model_json_schema())
        return await f
