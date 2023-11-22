from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional

from eidolon_sdk.agent_memory import AgentMemory

T = TypeVar('T', bound='ProcessingUnit')


class ProcessingUnitLocator:
    @abstractmethod
    def locate_unit(self, unit_type: Type[T]) -> Optional[T]:
        pass


class ProcessingUnit(ABC):
    agent_memory: AgentMemory
    processing_unit_locator: ProcessingUnitLocator

    def __init__(self, memory: AgentMemory, **kwargs):
        self.agent_memory = memory

    def locate_unit(self, unit_type: Type[T]) -> T:
        return self.processing_unit_locator.locate_unit(unit_type)
