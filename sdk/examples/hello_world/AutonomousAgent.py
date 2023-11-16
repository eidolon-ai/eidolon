import asyncio
from typing import Annotated, Any

from pydantic import Field, BaseModel

from eidolon_sdk.agent import CodeAgent, initializer
from eidolon_sdk.cpu.agent_cpu import AgentCPU
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage


class IdleStateRepresentation(BaseModel):
    response: str


class AutonomousAgent(CodeAgent):

    @initializer
    async def execute(self, question: Annotated[str, Field(description="A question")]) -> IdleStateRepresentation:
        process_id = self.get_context().process_id

        retValue = []
        lock = asyncio.Event()
        async def response_handler(ret_p_id: str, response: dict[str, Any]):
            print("here")
            print(response)
            retValue.append(IdleStateRepresentation.model_validate(response))
            lock.set()

        agent_cpu = AgentCPU(self.agent_machine, response_handler)
        await agent_cpu.start()
        agent_cpu.schedule_request(process_id, [UserTextCPUMessage(prompt=question)], {}, IdleStateRepresentation.model_json_schema())
        await lock.wait()
        return retValue[0]
