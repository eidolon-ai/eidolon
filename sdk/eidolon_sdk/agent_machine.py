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
    memory_unit = None
    llm_unit = None
    control_unit = None
    if cpu_model.memory_unit:
        memory_unit = cpu_model.memory_unit.instantiate()
    if cpu_model.llm_unit:
        llm_unit = cpu_model.llm_unit.instantiate()
    if cpu_model.control_unit:
        control_unit = cpu_model.control_unit.instantiate()

    cpu = AgentCPU(
        bus_controller=bus_controller,
        io_unit=cpu_model.io_unit.instantiate(),
        memory_unit=memory_unit,
        llm_unit=llm_unit,
        control_unit=control_unit,
        logic_units={
            name: logic_unit.instantiate(agent_machine=machine, controller=bus_controller)
            for name, logic_unit in cpu_model.logic_units.items()
        },
    )

    cpu.io_unit.initialize(bus_controller, cpu, machine.agent_memory)
    if cpu.memory_unit:
        cpu.memory_unit.initialize(bus_controller, cpu, machine.agent_memory)

    if cpu.llm_unit:
        cpu.llm_unit.initialize(bus_controller, cpu, machine.agent_memory)

    if cpu.control_unit:
        cpu.control_unit.initialize(bus_controller, cpu, machine.agent_memory)

    for logic_unit in cpu.logic_units.values():
        logic_unit.initialize(bus_controller, cpu, machine.agent_memory)

    return cpu
