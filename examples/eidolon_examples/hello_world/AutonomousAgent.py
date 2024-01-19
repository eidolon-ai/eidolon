from fastapi import Body
from pydantic import BaseModel
from typing import Annotated

from eidos_sdk.agent.agent import register_program, AgentState, register_action, Agent
from eidos_sdk.cpu.agent_io import UserTextCPUMessage
from eidos_sdk.io.events import AgentStateEvent


class IdleStateRepresentation(BaseModel):
    response: str


class AutonomousAgent(Agent):
    @register_program()
    @register_action("idle")
    async def converse(
            self, process_id, question: Annotated[str, Body(description="A question", embed=True)]
    ) -> AgentState[IdleStateRepresentation]:
        thread = await self.cpu.main_thread(process_id)
        response = await thread.run_request(
            prompts=[UserTextCPUMessage(prompt=question)], output_format=IdleStateRepresentation.model_json_schema()
        )
        return AgentState(name="idle", data=IdleStateRepresentation(**response))

    @register_program()
    @register_action("idle")
    async def stream_response(self, process_id, question: Annotated[str, Body(description="A question", embed=True)]):
        try:
            thread = await self.cpu.main_thread(process_id)
            print("here")
            stream = thread.stream_request(
                prompts=[UserTextCPUMessage(prompt=question)], output_format=IdleStateRepresentation.model_json_schema()
            )
            print("here2")
            async for event in stream:
                print("here3")
                yield event
            print("here4")

            yield AgentStateEvent(state="idle")
            print("here5")
        except Exception as e:
            print("here6")
            print(e)
            raise e
