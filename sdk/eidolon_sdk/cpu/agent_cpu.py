from abc import ABC, abstractmethod
from typing import Any, Union, List, Dict, Callable, Awaitable

from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.cpu.agent_bus import BusController
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage, ImageURLCPUMessage, IOUnit
from eidolon_sdk.cpu.control_unit import ConversationalControlUnit
from eidolon_sdk.cpu.llm_unit import OpenAIGPT
from eidolon_sdk.cpu.memory_unit import MemoryUnit, ConversationalMemoryUnit


class ResponseHandler(ABC):
    @abstractmethod
    async def handle_response(self, process_id: str, response: Dict[str, Any]):
        pass


class AgentCPU:
    bus_controller: BusController = BusController()
    io_unit: IOUnit
    memory_unit: MemoryUnit

    def __init__(self, agent_machine: AgentMachine, response_handler: Callable[[str, Dict[str, Any]], Awaitable[None]]):
        self.agent_machine = agent_machine
        self.io_unit = IOUnit(self)
        self.io_unit.controller = self.bus_controller
        self.io_unit.agent_machine = agent_machine
        self.bus_controller.add_participant(self.io_unit)

        self.memory_unit = ConversationalMemoryUnit(agent_machine)
        self.memory_unit.controller = self.bus_controller
        self.memory_unit.agent_machine = agent_machine
        self.bus_controller.add_participant(self.memory_unit)

        self.llm_unit = OpenAIGPT("gpt-4-1106-preview", .3)
        self.llm_unit.controller = self.bus_controller
        self.llm_unit.agent_machine = agent_machine
        self.bus_controller.add_participant(self.llm_unit)

        self.control_unit = ConversationalControlUnit()
        self.control_unit.controller = self.bus_controller
        self.control_unit.agent_machine = agent_machine
        self.bus_controller.add_participant(self.control_unit)

        self.response_handler = response_handler

    async def start(self):
        await self.bus_controller.start()

    async def stop(self):
        await self.bus_controller.stop()

    def schedule_request(self, process_id: str, prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]], input_data: dict[str, Any],
                         output_format: Dict[str, Any]):
        self.io_unit.process_request(process_id, prompts, input_data, output_format)

    async def respond(self, process_id: str, response: Dict[str, Any]):
        await self.response_handler(process_id, response)
