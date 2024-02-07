from pydantic import BaseModel, Field
from typing import List


class Document(BaseModel):
    id: str = Field(default=None, description="The unique identifier for the document")
    page_content: str = Field(..., description="The content of the document.")
    metadata: dict = Field(default_factory=dict, description="The metadata of the document.")


class EmbeddedDocument(BaseModel):
    id: str = Field(description="The unique identifier for the document")
    embedding: List[float] = Field(..., description="The content of the document.")
    metadata: dict = Field(default_factory=dict, description="The metadata of the document.")
