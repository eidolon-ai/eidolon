from contextlib import contextmanager
from typing import List, Iterable, Tuple

import yaml

from eidos_sdk.memory.agent_memory import AgentMemory
from .agent_controller import AgentController
from .resources import MachineResource, agent_resources, Resource
from ..agent_os import AgentOS
from ..util.logger import logger


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
    def from_resources(resources: Iterable[Resource | Tuple[Resource, str]], machine_name: str):
        for resource_or_tuple in resources:
            if isinstance(resource_or_tuple, Resource):
                resource, source = resource_or_tuple, None
            else:
                resource, source = resource_or_tuple
            AgentOS.register_resource(resource=resource, source=source)
        machine = AgentOS.get_resource(MachineResource.kind_literal(), machine_name)
        machine: MachineResource = machine.promote(MachineResource)

        agents = {}
        for kind, agent_resource_class in agent_resources.items():
            for name, r in AgentOS.get_resources(kind).items():
                with _error_wrapper(r):
                    agents[name] = r.promote(agent_resource_class).instantiate()

        logger.info(f"Building machine '{machine_name}'")
        logger.debug(yaml.safe_dump(machine.model_dump()))

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
    return error_logger(AgentOS.get_resource_source(resource.kind, resource.metadata.name))


def _error_wrapped_fn(resource, fn):
    with _error_wrapper(resource):
        return fn()
