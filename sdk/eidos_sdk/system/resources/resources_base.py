from __future__ import annotations

from typing import List, Literal, Optional, TypeVar, Type

from pydantic import BaseModel


class Metadata(BaseModel):
    name: str
    annotations: List[str] = []
    labels: List[str] = []


T = TypeVar("T", bound=BaseModel)


class Resource(BaseModel, extra="allow"):
    apiVersion: Literal["eidolon/v1"]
    kind: str
    metadata: Metadata = Metadata(name="DEFAULT")

    @classmethod
    def kind_literal(cls) -> Optional[str]:
        return getattr(cls.model_fields["kind"].annotation, "__args__", [None])[0]

    def promote(self, clazz: Type[T]) -> T:
        return clazz.model_validate(self.model_dump())
