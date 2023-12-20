from textwrap import dedent
from typing import Annotated, Literal, List

from fastapi import Body
from pydantic import BaseModel

from eidos_sdk.agent.agent import register_program, Agent
from eidos_sdk.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage
from eidos_sdk.util.logger import logger


class TestCase(BaseModel):
    name: str
    details: str
    passed: bool


class QAResponse(BaseModel):
    outcome: Literal["success", "failure"]
    test_cases: List[TestCase]
    synopsis: str


system_message = dedent("""\
    You are a qa agent who is responsible for testing your tools. When asked to test 
    a tool, you will call all methods related to the tool with reasonable inputs and 
    determine if they are operating in a justifiable manner.""")


class QualityAssurance(Agent):
    @register_program()
    async def test(self, process_id, agent: Annotated[str, Body()]) -> QAResponse:
        thread = await self.cpu.main_thread(process_id)
        await thread.set_boot_messages([SystemCPUMessage(prompt=system_message)])
        await thread.schedule_request(prompts=[UserTextCPUMessage(prompt=f"Please test all tools related to {agent}")])
        logger.info(f"Tests Complete for {agent}")
        response: QAResponse = await thread.schedule_request(
            prompts=[UserTextCPUMessage(prompt="Please summarize your test results")],
            output_format=QAResponse,
        )
        if response.outcome != "success":
            logger.error(f"QA failed for agent {agent}, somebody fix it!\n{response.synopsis}",)
        return response
