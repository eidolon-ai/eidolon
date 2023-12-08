from contextlib import contextmanager
from typing import List, Type

from eidos.memory.agent_memory import AgentMemory
from .agent_controller import AgentController
from .resources import MachineResource, agent_resources, Resource, AgentResource
from ..agent_os import AgentOS


class AgentMachine:
    memory: AgentMemory
    agent_controllers: List[AgentController]

    def __init__(self, agent_memory: AgentMemory, agent_programs: List[AgentController] = None):
        self.memory = agent_memory
        self.agent_controllers = agent_programs or []
        self.app = None

    async def start(self, app):
        if self.app:
            raise Exception("Machine already started")
        for program in self.agent_controllers:
            await program.start(app)
        self.memory.start()
        self.app = app

    def stop(self):
        if self.app:
            for program in self.agent_controllers:
                program.stop(self.app)
            self.memory.stop()
            self.app = None

    @staticmethod
    def from_os(agent_os: Type[AgentOS]):
        machine = agent_os.get_resource(MachineResource.kind_literal()).promote(MachineResource)

        agents = {}
        for name, r in agent_os.get_resources(AgentResource.kind_literal()).items():
            agents[name] = r.promote(agent_resources[r.kind]).instantiate()

        return AgentMachine(
            agent_memory=(machine.spec.get_agent_memory()),
            agent_programs=[AgentController(name, agent) for name, agent in agents.items()],
        )


@contextmanager
def error_logger(filename: str = None):
    try:
        yield
    except Exception as e:
        raise ValueError(f"Error building resource {filename}") from e


def _error_wrapper(resource: Resource):
    return error_logger(AgentOS.get_resource_source(resource.metadata.name))


def _error_wrapped_fn(resource, fn):
    with _error_wrapper(resource):
        return fn()
