from typing import Annotated
from fastapi import Body
from eidos_sdk.agent.agent import register_program, register_action, AgentState


class HelloWorld:
    @register_program()
    async def enter(self, name: Annotated[str, Body(description="Your name", embed=True)]) -> AgentState[str]:
        """
        I greet people with a smile!
        """
        return AgentState(name="shopping", data=f"Hello {name}!👋😀")

    @register_action("shopping")
    async def exit(self) -> str:
        """
        I say goodbye to people with a smile!
        """
        return "Goodbye! Don't forget your coat!👋🧥☃️😀"
