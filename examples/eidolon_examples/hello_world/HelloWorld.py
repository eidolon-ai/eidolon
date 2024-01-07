from fastapi import UploadFile, Body, File
from pydantic import BaseModel, Field
from typing import Annotated, List

from eidos_sdk.agent.agent import register_program


class IdleStateRepresentation(BaseModel):
    welcome_message: str


class NestedObject(BaseModel):
    str_field: str
    int_field: int
    float_field: float
    bool_field: bool


class ComplexInput(BaseModel):
    int_field: int = Field(description="An integer field")
    float_field: float = Field(description="A float field")
    bool_field: bool = Field(description="A boolean field")
    str_field: str = Field(description="A string field")
    optional_str_field: str = Field(default=None, description="An optional string field")

    nested_object: NestedObject = Field(description="A nested object")
    optional_nested_object: NestedObject = Field(default=None, description="A nested object")

    array_of_strings: list[str] = Field(description="An array of strings")
    optional_array_of_strings: list[str] = Field(default=None, description="An array of strings")
    array_of_objects: list[NestedObject] = Field(description="An array of objects")

    single_file: UploadFile = Field(description="A single file")
    multiple_files: list[UploadFile] = Field(description="A list of files")

    optional_file: UploadFile = Field(default=None, description="A single file")
    optional_multiple_files: list[UploadFile] = Field(default=None, description="A list of files")


class HelloWorld:
    @register_program()
    async def execute(self, name: Annotated[str, Body(description="Your name", embed=True)]) -> IdleStateRepresentation:
        return IdleStateRepresentation(welcome_message=f"Hello, World {name}!")

    @register_program()
    async def describe_image(
        self,
        question: str = Body(..., embed=True, description="Your question about the image"),
        image: UploadFile = File(..., description="The image to describe"),
    ) -> IdleStateRepresentation:
        return IdleStateRepresentation(
            welcome_message=f"Hello, World {question}!  File name is {image.filename}. "
            f"file length is {image.size} bytes. content type is {image.content_type}"
        )

    @register_program()
    async def describe_images(
        self,
        question: str = Body(..., embed=True, description="Your question about the image"),
        images: List[UploadFile] = File(description="The images to describe"),
    ) -> IdleStateRepresentation:
        files_msg = "\n".join(
            [
                f"File name is {image.filename}. file length is {image.size} bytes. content type is {image.content_type}"
                for image in images
            ]
        )
        return IdleStateRepresentation(welcome_message=f"Hello, World {question}!\n{files_msg}")

    @register_program()
    async def return_string(self, name: Annotated[str, Body(description="Your name", embed=True)]) -> str:
        return f"Hello, World {name}!"

    @register_program()
    async def return_complex_object(self, c_obj: Annotated[ComplexInput, Body(embed=True)]) -> ComplexInput:
        return c_obj
