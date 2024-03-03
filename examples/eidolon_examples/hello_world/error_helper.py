from typing import Union, Annotated

from fastapi.params import Body

from eidolon_ai_sdk.agent.agent import register_program, AgentState, register_action
from fastapi import HTTPException
from pydantic import BaseModel


class TmpBody(BaseModel):
    foo: int
    bar: str


class ErrorProneCodeAgent:
    """
    Initializes in state a, can transform a or b to any state. Can terminate b or c.
    """

    @register_program()
    async def http_exception(self, status_code: int = Body(418, embed=True)) -> AgentState[str]:
        raise HTTPException(status_code=status_code, detail="This is a test")

    @register_program()
    async def naked_exception(self) -> AgentState[str]:
        raise Exception("This is a test")

    @register_program()
    async def runtime_error(self) -> AgentState[str]:
        raise RuntimeError("This is a test")

    @register_program()
    async def value_error(self) -> AgentState[str]:
        raise ValueError("This is a test")

    @register_action("initialized", "http_error", "unhandled_error")
    async def handle(self):
        return AgentState(name="initialized", data="blah")

    @register_action("initialized", "http_error", "unhandled_error")
    async def body_test(self, body: TmpBody):
        return AgentState(name="initialized", data="blah")
