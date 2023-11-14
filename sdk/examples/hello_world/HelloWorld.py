from typing import Annotated

from pydantic import Field, BaseModel

from eidolon_sdk.agent import CodeAgent, initializer


class IdleStateRepresentation(BaseModel):
    welcome_message: str


class HelloWorld(CodeAgent):
    @initializer
    async def execute(self, name: Annotated[str, Field(description="Your name")]) -> IdleStateRepresentation:
        return IdleStateRepresentation(welcome_message=f'Hello, World {name}!')
