from typing import Any, Union, List, Dict, Optional

from bson import ObjectId

from eidolon_sdk.agent_memory import AgentMemory
from eidolon_sdk.cpu.agent_bus import BusController
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage, ImageURLCPUMessage, ResponseHandler, IOUnit
from eidolon_sdk.cpu.logic_unit import LogicUnit, MethodInfo
from eidolon_sdk.cpu.processing_unit import ProcessingUnit


class AgentCPU:
    bus_controller: BusController
    io_unit: IOUnit
    memory_unit: ProcessingUnit
    llm_unit: ProcessingUnit
    control_unit: ProcessingUnit
    logic_units: List[LogicUnit]

    tools: Dict[str, MethodInfo]

    def __init__(
            self,
            agent_memory: AgentMemory,
            bus_controller: BusController,
            io_unit: IOUnit,
            memory_unit: Optional[ProcessingUnit],
            llm_unit: Optional[ProcessingUnit],
            control_unit: Optional[ProcessingUnit],
            logic_units: List[ProcessingUnit] = None,
    ):
        self.agent_memory = agent_memory
        self.bus_controller = bus_controller

        self.io_unit = io_unit
        self.memory_unit = memory_unit
        self.llm_unit = llm_unit
        self.control_unit = control_unit
        self.logic_units = logic_units or []

        self.processing_units: List[ProcessingUnit] = [self.io_unit, *self.logic_units]
        if self.memory_unit:
            self.processing_units.append(self.memory_unit)
        if self.llm_unit:
            self.processing_units.append(self.llm_unit)
        if self.control_unit:
            self.processing_units.append(self.control_unit)

    async def start(self, response_handler: ResponseHandler):
        # iterate over processing units and initialize them. The initialize method can add to processing_units so the loop needs to be reentrant.
        # first copy off the processing units, so we can iterate over them and detect if any new ones are added.
        processing_units = self.processing_units.copy()
        processing_units_len = len(processing_units)
        while len(processing_units) > 0:
            pu = processing_units.pop(0)
            kwargs = dict(bus_controller=self.bus_controller, cpu=self, memory=self.agent_memory)
            if pu == self.io_unit:
                kwargs['response_handler'] = response_handler
            pu.initialize(**kwargs)
            if len(processing_units) == 0 and len(self.processing_units) > processing_units_len:
                processing_units = self.processing_units[processing_units_len:]
                processing_units_len = len(self.processing_units)

        for pu in self.processing_units:
            self.bus_controller.add_participant(pu)

        self.tools = {}
        for lu in self.logic_units:
            methods = lu.discover()
            for method in methods.values():
                self.tools[f"{method.name}_{str(ObjectId())}"] = method
            # Allow the logic units to self register with the LLM bus by binding their le_read port to the LLM ltc_write port if it isn't already set in the config
            # and their le_write port to the LLM llm_read port if the le_write port isn't already set.
            if lu.spec.lu_read is None:
                lu.spec.lu_read = self.llm_unit.spec.ltc_write
            if lu.spec.lu_write is None:
                lu.spec.lu_write = self.llm_unit.spec.llm_read

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

    def register_logic_unit(self, logic_unit: LogicUnit):
        self.processing_units.append(logic_unit)
        self.logic_units.append(logic_unit)
