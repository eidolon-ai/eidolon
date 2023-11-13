from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')
V = TypeVar('V')


class ControlUnit(BaseModel, Generic[T, V], ABC):
    @abstractmethod
    async def process(self, request: T) -> V:
        pass
