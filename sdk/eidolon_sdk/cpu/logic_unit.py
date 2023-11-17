from abc import ABC

from pydantic import BaseModel, Field

from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.cpu.bus_messages import READ_PORT
from eidolon_sdk.reference_model import Specable


class LogicUnitConfig:
    le_read: READ_PORT = Field(description="A port that, when bound to an event, will read the LLM tool call from the bus.")
    lr_write: READ_PORT = Field(description="A port that, when bound to an event, will write the tool call response to the bus.")


class LogicUnit(ProcessingUnit, Specable[LogicUnitConfig], ABC):
    def __init__(self, spec: LogicUnitConfig = None):
        self.spec = spec

    def input_model(self) -> BaseModel:
        pass

    def output_model(self) -> BaseModel:
        pass

    def execute(self, *args, **kwargs):
        pass
