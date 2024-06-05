from fastapi import Body
from pydantic import BaseModel
from typing import Annotated

from eidolon_ai_sdk.agent.agent import register_program, AgentState, register_action, Agent
from eidolon_ai_sdk.apu.agent_io import UserTextAPUMessage
from eidolon_ai_client.events import AgentStateEvent


class IdleStateRepresentation(BaseModel):
    response: str


class AutonomousAgent(Agent):
    @register_program()
    @register_action("idle")
    async def converse(
        self, process_id, question: Annotated[str, Body(description="A question", embed=True)]
    ) -> AgentState[IdleStateRepresentation]:
        thread = await self.apu.main_thread(process_id)
        response = await thread.run_request(
            prompts=[UserTextAPUMessage(prompt=question)], output_format=IdleStateRepresentation.model_json_schema()
        )
        return AgentState(name="idle", data=IdleStateRepresentation(**response))

    @register_program()
    @register_action("idle")
    async def stream_response(self, process_id, question: Annotated[str, Body(description="A question", embed=True)]):
        thread = await self.apu.main_thread(process_id)
        stream = thread.stream_request(prompts=[UserTextAPUMessage(prompt=question)], output_format=str)
        async for event in stream:
            yield event

        yield AgentStateEvent(state="idle")
