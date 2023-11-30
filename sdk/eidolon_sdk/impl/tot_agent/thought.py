from __future__ import annotations

from typing import Literal, List

from pydantic import BaseModel, Field


class ThoughtValidity(BaseModel):
    validity: Literal["INTERMEDIATE", "VALID", "INVALID"]


class Thought(ThoughtValidity):
    text: str
    children: List[Thought] = Field(default_factory=list)

    def __hash__(self) -> int:
        return id(self)
