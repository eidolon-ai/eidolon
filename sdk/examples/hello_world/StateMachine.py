from typing import Annotated, Union

from fastapi import HTTPException
from pydantic import Field, BaseModel

from eidolon_sdk.agent import CodeAgent, initializer, AgentState, register_action


class AState(BaseModel):
    foo: str


class BState(BaseModel):
    bar: str


class CState(BaseModel):
    baz: str


class StateMachine(CodeAgent):
    """
    Initializes in state a, can transform a or b to any state. Can terminate b or c.
    """

    @initializer
    async def execute(self) -> AgentState[str]:
        return AgentState(name="a", data="here is something to transform")

    @register_action("a", "b")
    async def transform(self, requested_state: str) -> AgentState[Union[AState, BState, CState]]:
        if requested_state == "a":
            return AgentState(name="a", data=AState(foo="here ya foo"))
        elif requested_state == "b":
            return AgentState(name="b", data=BState(bar="here ya bar"))
        elif requested_state == "c":
            return AgentState(name="c", data=CState(baz="here ya baz"))
        else:
            raise HTTPException(status_code=400, detail="Invalid state requested")

    @register_action("b", "c")
    async def terminate(self, requested_state: str):
        return "It was a good run while it lasted. 🤘"
