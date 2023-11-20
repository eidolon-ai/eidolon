from abc import ABC

from pydantic import BaseModel

from eidolon_sdk.cpu.agent_bus import BusParticipant, BusEvent
from eidolon_sdk.cpu.bus_messages import AddConversationHistory, OutputResponse
from eidolon_sdk.reference_model import Specable


class ControlUnitConfig(BaseModel):
    pass


class ControlUnit(BusParticipant, Specable[ControlUnitConfig], ABC):
    def __init__(self, spec: ControlUnitConfig = None):
        self.spec = spec

