from typing import Any, Union, List, Dict

from eidolon_sdk.cpu.agent_bus import BusController, BusParticipant
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage, ImageURLCPUMessage, IOUnit, ResponseHandler
from eidolon_sdk.cpu.control_unit import ConversationalControlUnit, ControlUnit
from eidolon_sdk.cpu.llm_unit import OpenAIGPT, LLMUnit
from eidolon_sdk.cpu.logic_unit import LogicUnit
from eidolon_sdk.cpu.memory_unit import MemoryUnit


class AgentCPU:
    bus_controller: BusController
    io_unit: IOUnit
    memory_unit: MemoryUnit
    llm_unit: LLMUnit
    control_unit: ControlUnit
    logic_units: Dict[str, LogicUnit]

    def __init__(
            self,
            io_unit: IOUnit,
            memory_unit: MemoryUnit,
            llm_unit: OpenAIGPT,
            control_unit: ConversationalControlUnit,
            logic_units: Dict[str, LogicUnit] = None,
            bus_controller: BusController = BusController(),
    ):
        self.bus_controller = bus_controller

        self.io_unit = io_unit
        self.memory_unit = memory_unit
        self.llm_unit = llm_unit
        self.control_unit = control_unit
        self.logic_units = logic_units or {}

    async def start(self, response_handler: ResponseHandler):
        self.io_unit.start(response_handler)
        participants: List[BusParticipant] = [self.memory_unit, self.llm_unit, self.control_unit, self.io_unit]
        participants.extend(self.logic_units.values())
        for participant in participants:
            self.bus_controller.add_participant(participant)
        await self.bus_controller.start()

    async def stop(self):
        await self.bus_controller.stop()

    def schedule_request(
            self,
            process_id: str,
            prompts: List[Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]],
            input_data: Dict[str, Any],
            output_format: Dict[str, Any]
    ):
        self.io_unit.process_request(process_id, prompts, input_data, output_format)
