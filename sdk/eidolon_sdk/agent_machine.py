from typing import List

import yaml
from pydantic import ValidationError

from .agent_memory import AgentMemory
from .agent_program import AgentProgram
from .cpu.agent_cpu import AgentCPU
from .machine_model import MachineModel


class AgentMachine:
    agent_memory: AgentMemory
    agent_programs: List[AgentProgram]

    def __init__(self, agent_memory: AgentMemory, agent_programs: List[AgentProgram]):
        self.agent_memory = agent_memory
        self.agent_programs = agent_programs

    @staticmethod
    def from_yaml(machine_yaml):
        try:
            model = MachineModel(**(yaml.safe_load(machine_yaml)))
            memory = AgentMemory(**{k: v.instantiate() for k, v in model.agent_memory.__dict__.items()})
            machine = AgentMachine(agent_memory=memory, agent_programs=[])

            machine.agent_programs = [
                AgentProgram(name=name, agent=program.agent.instantiate(
                    agent_machine=machine, cpu=(_make_cpu(program.cpu, machine))
                )) for name, program in model.agent_programs.items()
            ]
            return machine
        except ValidationError as e:
            print(e.errors())
            raise Exception(f"Invalid machine model: {e}")


def _make_cpu(cpu_model, machine):
    if not cpu_model:
        return None

    kwargs = dict(memory=machine.agent_memory)
    io_unit = cpu_model.io_unit.instantiate(**kwargs)
    memory_unit = cpu_model.memory_unit.instantiate(**kwargs)
    llm_unit = cpu_model.llm_unit.instantiate(**kwargs)
    logic_units = [logic_unit.instantiate(**kwargs) for logic_unit in cpu_model.logic_units]
    control_unit = cpu_model.control_unit.instantiate(io_unit=io_unit, memory_unit=memory_unit, llm_unit=llm_unit, logic_units=logic_units, **kwargs)

    cpu = AgentCPU(
        agent_memory=machine.agent_memory,
        control_unit=control_unit
    )

    io_unit.processing_unit_locator = cpu
    memory_unit.processing_unit_locator = cpu
    llm_unit.processing_unit_locator = cpu
    control_unit.processing_unit_locator = cpu
    for logic_unit in logic_units:
        logic_unit.processing_unit_locator = cpu

    return cpu
