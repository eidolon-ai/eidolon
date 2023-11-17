from abc import ABC

from pydantic import BaseModel

from eidolon_sdk.cpu.agent_bus import BusParticipant, BusController


class LogicUnit(BusParticipant, ABC):
    def __init__(self, agent_machine: 'AgentMachine', controller: BusController):
        super().__init__(controller)
        self.agent_machine = agent_machine

    def input_model(self) -> BaseModel:
        pass

    def output_model(self) -> BaseModel:
        pass

    def execute(self, *args, **kwargs):
        pass
