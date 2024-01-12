from typing import Annotated

from fastapi import Body
from pydantic import BaseModel

from eidos_sdk.agent.agent import register_program, AgentState, register_action, Agent
from eidos_sdk.cpu.agent_io import UserTextCPUMessage


class IdleStateRepresentation(BaseModel):
    response: str


class AutonomousAgent(Agent):
    @register_program()
    @register_action("idle")
    async def converse(
        self, process_id, question: Annotated[str, Body(description="A question", embed=True)]
    ) -> AgentState[IdleStateRepresentation]:
        thread = await self.cpu.main_thread(process_id)
        response = await thread.schedule_request_raw(
            prompts=[UserTextCPUMessage(prompt=question)], output_format=IdleStateRepresentation.model_json_schema()
        )
        return AgentState(name="idle", data=IdleStateRepresentation(**response))
