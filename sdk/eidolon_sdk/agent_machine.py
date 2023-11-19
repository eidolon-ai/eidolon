from typing import List

import yaml

from .agent_memory import AgentMemory
from .agent_program import AgentProgram
from .cpu.agent_bus import BusController
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
        model = MachineModel(**(yaml.safe_load(machine_yaml)))
        memory = AgentMemory(**{k: v.instantiate() for k, v in model.agent_memory.__dict__.items()})
        machine = AgentMachine(agent_memory=memory, agent_programs=[])

        machine.agent_programs = [
            AgentProgram(name=name, agent=program.agent.instantiate(
                agent_machine=machine, cpu=(_make_cpu(program.cpu, machine))
            )) for name, program in model.agent_programs.items()
        ]
        return machine


def _make_cpu(cpu_model, machine):
    if not cpu_model:
        return None

    bus_controller = BusController()
    cpu = AgentCPU(
        agent_memory=machine.agent_memory,
        bus_controller=bus_controller,
        io_unit=cpu_model.io_unit.instantiate(),
        memory_unit=cpu_model.memory_unit.instantiate() if cpu_model.memory_unit else None,
        llm_unit=cpu_model.llm_unit.instantiate() if cpu_model.llm_unit else None,
        control_unit=cpu_model.control_unit.instantiate() if cpu_model.control_unit else None,
        logic_units={
            name: logic_unit.instantiate(agent_machine=machine, controller=bus_controller)
            for name, logic_unit in cpu_model.logic_units.items()
        },
    )

    return cpu
