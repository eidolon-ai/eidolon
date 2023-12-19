from typing import Annotated, Literal, List

from fastapi import Body
from pydantic import BaseModel

from eidos_sdk.agent.agent import register_program, AgentState, Agent
from eidos_sdk.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage


class TestCase(BaseModel):
    name: str
    details: str
    passed: bool


class QAResponse(BaseModel):
    outcome: Literal["success", "failure"]
    test_cases: List[TestCase]
    synopsis: str


class QualityAssurance(Agent):
    @register_program()
    async def test(self, process_id, agent: Annotated[str, Body()]) -> QAResponse:
        thread = await self.cpu.main_thread(process_id)
        await thread.set_boot_messages(SystemCPUMessage(prompt="Running tests..."))
        response = await thread.schedule_request(UserTextCPUMessage(prompt="Running tests..."))
