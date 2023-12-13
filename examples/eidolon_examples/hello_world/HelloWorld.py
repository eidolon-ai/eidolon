from typing import Annotated

from fastapi import UploadFile, Body, File
from pydantic import BaseModel

from eidos.agent.agent import CodeAgent, register_program


class IdleStateRepresentation(BaseModel):
    welcome_message: str


class HelloWorld(CodeAgent):
    @register_program()
    async def execute(self, name: Annotated[str, Body(description="Your name", embed=True)]) -> IdleStateRepresentation:
        return IdleStateRepresentation(welcome_message=f"Hello, World {name}!")

    @register_program()
    async def describe_image(
        self,
        question: str = Body(..., embed=True, description="Your question about the image"),
        image: UploadFile = File(..., description="The image to describe"),
    ) -> IdleStateRepresentation:
        return IdleStateRepresentation(welcome_message=f"Hello, World {question}!  File name is {image.filename}. "
                                                       f"file length is {image.size} bytes. content type is {image.content_type}")
