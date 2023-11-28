from __future__ import annotations

from enum import Enum
from typing import Set, Literal

from pydantic import BaseModel, Field


class ThoughtValidity(BaseModel):
    validity: Literal["VALID_INTERMEDIATE", "VALID_FINAL", "INVALID"]


class Thought(ThoughtValidity):
    text: str
    children: Set[Thought] = Field(default_factory=set)

    def __hash__(self) -> int:
        return id(self)
