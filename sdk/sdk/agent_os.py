from __future__ import annotations

from typing import TypeVar, Generic, Dict

from fastapi import Request
from fastapi.openapi.models import Response

from agent_cpu import LogicUnit

T = TypeVar('T')
V = TypeVar('V')


class Agent:
    """
    placeholder for the object to manipulate when different logic/control units have access to.
    """
    def config(self):
        pass

    def agent_memory(self):
        pass

    def call_llm(self, prompt):
        pass

    def logic_units(self) -> Dict[str, LogicUnit]:
        pass


class IOUnit(Generic[T, V]):
    @staticmethod
    async def read(request: Request) -> T:
        pass

    @staticmethod
    async def write(data: V, response: Response) -> None:
        pass


