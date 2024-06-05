import logging
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional

from eidolon_ai_sdk.cpu.call_context import CallContext

PU_T = TypeVar("PU_T", bound="ProcessingUnit")


class ProcessingUnitLocator:
    @abstractmethod
    def locate_unit(self, unit_type: Type[PU_T]) -> Optional[PU_T]:
        pass


class ProcessingUnit(ABC):
    processing_unit_locator: ProcessingUnitLocator
    logger = logging.getLogger("eidolon")

    def __init__(self, processing_unit_locator: ProcessingUnitLocator, **kwargs):
        self.processing_unit_locator = processing_unit_locator

    def locate_unit(self, unit_type: Type[PU_T]) -> PU_T:
        return self.processing_unit_locator.locate_unit(unit_type)

    async def clone_thread(self, old_context: CallContext, new_context: CallContext):
        pass
