from abc import ABC, abstractmethod
from typing import TypeVar, Type

from eidolon_sdk.agent_memory import AgentMemory

T = TypeVar('T', bound='ProcessingUnit')


class ProcessingUnitLocator:

    @abstractmethod
    def locate_unit(self, unit_type: Type[T]) -> T:
        pass


class ProcessingUnit(ABC):
    agent_memory: AgentMemory

    def __init__(self, memory: AgentMemory, processing_unit_locator: ProcessingUnitLocator, **kwargs):
        self.agent_memory = memory
        self.processing_unit_locator = processing_unit_locator

    def locate_unit(self, unit_type: Type[T]) -> T:
        return self.processing_unit_locator.locate_unit(unit_type)
