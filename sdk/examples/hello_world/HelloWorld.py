from typing import Annotated

from pydantic import Field, BaseModel

from eidolon_sdk.agent import CodeAgent, register


class IdleStateRepresentation(BaseModel):
    welcome_message: str


class HelloWorld(CodeAgent):
    @register(state='idle', transition_to=['idle'], state_representation=IdleStateRepresentation)
    async def execute(self, name: Annotated[str, Field(description="Your name")]) -> dict:
        return {
            "welcome_message": f'Hello, World {name}!'
        }
