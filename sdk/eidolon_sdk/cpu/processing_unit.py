import typing
from abc import ABC

from pydantic import BaseModel

from eidolon_sdk.agent_memory import AgentMemory
from eidolon_sdk.cpu.agent_bus import BusParticipant, BusController

T = typing.TypeVar('T', bound=BaseModel)


# todo, we can probably remove cpu ref here
class ProcessingUnit(BusParticipant, ABC):
    cpu: 'AgentCPU'
    agent_memory: AgentMemory

    # noinspection PyMethodOverriding
    def initialize(self, bus_controller: BusController, cpu: 'AgentCPU', memory: AgentMemory):
        super().initialize(bus_controller)
        self.cpu = cpu
        self.agent_memory = memory
