from typing import Annotated

from fastapi import UploadFile
from pydantic import Field, BaseModel

from eidos.agent.agent import CodeAgent, register_program


class IdleStateRepresentation(BaseModel):
    welcome_message: str


class HelloWorld(CodeAgent):
    @register_program()
    async def execute(self, name: Annotated[str, Field(description="Your name")]) -> IdleStateRepresentation:
        return IdleStateRepresentation(welcome_message=f'Hello, World {name}!')

    @register_program()
    async def describe_image(
            self,
            question: Annotated[str, Field(description="Your question about the image")],
            image: Annotated[UploadFile, Field(description="The image to describe")]
    ) -> IdleStateRepresentation:
        return IdleStateRepresentation(welcome_message=f'Hello, World {question}!')
