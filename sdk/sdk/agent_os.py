from typing import TypeVar, Generic

from fastapi import Request
from fastapi.openapi.models import Response

T = TypeVar('T')
V = TypeVar('V')


class Agent:
    def config(self):
        pass

    def agent_memory(self):
        pass


class IOUnit(Generic[T, V]):
    @staticmethod
    async def read(request: Request) -> T:
        pass

    @staticmethod
    async def write(data: V, response: Response) -> None:
        pass


class LogicUnit:
    @staticmethod
    async def execute(instruction, agent: Agent) -> None:
        # unsure of the object we pass of to manipulate framework. Calling it agent for now
        pass


class MemoryUnit:
    @staticmethod
    async def process(prompt, agent: Agent):  # this probably returns whatever a prompt object is
        pass


class ControlUnit(Generic[T, V]):
    @staticmethod
    async def process(request: T, agent: Agent) -> V:
        pass


class LLMUnit:
    @staticmethod
    async def query(prompt):
        pass
