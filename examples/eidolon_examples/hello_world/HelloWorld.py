from typing import Annotated

from pydantic import Field, BaseModel

from eidos.agent.agent import CodeAgent, register_program


class IdleStateRepresentation(BaseModel):
    welcome_message: str


class HelloWorld(CodeAgent):
    @register_program()
    async def execute(self, name: Annotated[str, Field(description="Your name")]) -> IdleStateRepresentation:
        return IdleStateRepresentation(welcome_message=f'Hello, World {name}!')
