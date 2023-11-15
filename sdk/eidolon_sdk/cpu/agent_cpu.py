from abc import ABC, abstractmethod
from typing import Any, Union, List, Dict

from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.cpu.agent_bus import BusController
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage, ImageURLCPUMessage, IOUnit
from eidolon_sdk.cpu.memory_unit import MemoryUnit, ConversationalMemoryUnit


class ResponseHandler(ABC):
    @abstractmethod
    async def handle_response(self, process_id: str, response: Dict[str, Any]):
        pass


class AgentCPU:
    bus_controller: BusController = BusController()
    io_unit: IOUnit
    memory_unit: MemoryUnit

    def __init__(self, agent_machine: AgentMachine, response_handler: ResponseHandler):
        self.agent_machine = agent_machine
        self.io_unit = IOUnit(self)
        self.memory_unit = ConversationalMemoryUnit(agent_machine)
        self.response_handler = response_handler

    def schedule_request(self, process_id: str, prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]], input_data: dict[str, Any]):
        self.io_unit.process_request(process_id, prompts, input_data)

    async def respond(self, process_id: str, response: Dict[str, Any]):
        await self.response_handler.handle_response(process_id, response)