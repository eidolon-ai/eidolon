from typing import Dict

from agent_os import ControlUnit, LogicUnit, IOUnit, MemoryUnit, LLMUnit


class AgentProgram:
    def __init__(self, io_unit: IOUnit, control_unit: ControlUnit, logic_units: Dict[str, LogicUnit], memory_unit: MemoryUnit, llm_unit: LLMUnit):
        self.llm_unit = llm_unit
        self.memory_unit = memory_unit
        self.logic_units = logic_units
        self.control_unit = control_unit
        self.io_unit = io_unit
