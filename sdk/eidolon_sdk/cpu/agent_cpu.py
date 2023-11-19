from typing import Any, Union, List, Dict, Optional

from eidolon_sdk.agent_memory import AgentMemory
from eidolon_sdk.cpu.agent_bus import BusController, BusParticipant
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage, ImageURLCPUMessage, ResponseHandler, IOUnit
from eidolon_sdk.cpu.logic_unit import LogicUnit
from eidolon_sdk.cpu.processing_unit import ProcessingUnit


class AgentCPU:
    bus_controller: BusController
    io_unit: IOUnit
    memory_unit: ProcessingUnit
    llm_unit: ProcessingUnit
    control_unit: ProcessingUnit
    logic_units: Dict[str, LogicUnit]

    def __init__(
            self,
            agent_memory: AgentMemory,
            bus_controller: BusController,
            io_unit: IOUnit,
            memory_unit: Optional[ProcessingUnit],
            llm_unit: Optional[ProcessingUnit],
            control_unit: Optional[ProcessingUnit],
            logic_units: Dict[str, ProcessingUnit] = None,
    ):
        self.agent_memory = agent_memory
        self.bus_controller = bus_controller

        self.io_unit = io_unit
        self.memory_unit = memory_unit
        self.llm_unit = llm_unit
        self.control_unit = control_unit
        self.logic_units = logic_units or {}

        self.processing_units: List[ProcessingUnit] = [self.io_unit, *self.logic_units.values()]
        if self.memory_unit:
            self.processing_units.append(self.memory_unit)
        if self.llm_unit:
            self.processing_units.append(self.llm_unit)
        if self.control_unit:
            self.processing_units.append(self.control_unit)

    async def start(self, response_handler: ResponseHandler):
        for pu in self.processing_units:
            kwargs = dict(bus_controller=self.bus_controller, cpu=self, memory=self.agent_memory)
            if pu == self.io_unit:
                kwargs['response_handler'] = response_handler
            pu.initialize(**kwargs)
            self.bus_controller.add_participant(pu)

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
