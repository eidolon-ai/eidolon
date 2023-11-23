import logging
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional

from eidolon_sdk.agent_memory import AgentMemory

PU_T = TypeVar('T', bound='ProcessingUnit')


class ProcessingUnitLocator:
    @abstractmethod
    def locate_unit(self, unit_type: Type[PU_T]) -> Optional[PU_T]:
        pass


class ProcessingUnit(ABC):
    agent_memory: AgentMemory
    processing_unit_locator: ProcessingUnitLocator
    logger = logging.getLogger("eidolon")

    def __init__(self, agent_memory: AgentMemory, processing_unit_locator: ProcessingUnitLocator, **kwargs):
        self.agent_memory = agent_memory
        self.processing_unit_locator = processing_unit_locator

    def locate_unit(self, unit_type: Type[PU_T]) -> PU_T:
        return self.processing_unit_locator.locate_unit(unit_type)
