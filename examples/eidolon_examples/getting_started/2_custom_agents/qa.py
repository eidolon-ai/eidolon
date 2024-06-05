from typing import Annotated, Literal, List

from fastapi import Body, HTTPException
from pydantic import BaseModel

from eidolon_ai_sdk.agent.agent import register_program, Agent, AgentSpec
from eidolon_ai_sdk.cpu.agent_io import SystemAPUMessage, UserTextAPUMessage
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_client.util.logger import logger


class TestCase(BaseModel):
    name: str
    details: str
    passed: bool


class QAResponse(BaseModel):
    outcome: Literal["success", "failure"]
    test_cases: List[TestCase]
    synopsis: str


system_message = "You are a qa agent who is responsible for testing your tools. When asked to test a tool, you will call all methods related to the tool with reasonable inputs and determine if they are operating in a justifiable manner."


class QASpec(AgentSpec):
    validate_agent: bool = False


class QualityAssurance(Agent, Specable[QASpec]):
    def __init__(self, **kwargs):
        Agent.__init__(self, **kwargs)

    @register_program()
    async def test(self, process_id, agent: Annotated[str, Body()]) -> QAResponse:
        if self.spec.validate_agent and agent not in self.spec.agent_refs:
            raise HTTPException(
                status_code=404,
                detail=f"Unable to communicate with {agent}. Legal agents are {self.spec.agent_refs}. "
                f"NOTE: the input should be a bare json string. Do not wrap it in quotes.",
            )

        thread = await self.cpu.main_thread(process_id)
        await thread.set_boot_messages([SystemAPUMessage(prompt=system_message)])
        await thread.run_request(prompts=[UserTextAPUMessage(prompt=f"Please test all tools related to {agent}")])
        logger.info(f"Tests Complete for {agent}")
        response: QAResponse = await thread.run_request(
            prompts=[UserTextAPUMessage(prompt="Please summarize your test results")],
            output_format=QAResponse,
        )
        if response.outcome != "success":
            logger.error(
                f"QA failed for agent {agent}, somebody fix it!\n{response.synopsis}",
            )
        return response
