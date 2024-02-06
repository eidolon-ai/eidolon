from contextlib import contextmanager
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

from eidolon_ai_sdk.memory.agent_memory import AgentMemory
from .agent_controller import AgentController
from .reference_model import AnnotatedReference, Specable
from .resources.agent_resource import AgentResource
from .resources.resources_base import Resource
from ..agent_os import AgentOS
from ..memory.file_memory import FileMemory
from ..memory.semantic_memory import SymbolicMemory
from ..memory.similarity_memory import SimilarityMemory
from ..security.security_manager import SecurityManager


class MachineSpec(BaseModel):
    symbolic_memory: AnnotatedReference[SymbolicMemory] = Field(description="The Symbolic Memory implementation.")
    file_memory: AnnotatedReference[FileMemory] = Field(desciption="The File Memory implementation.")
    similarity_memory: AnnotatedReference[SimilarityMemory] = Field(description="The Vector Memory implementation.")
    security_manager: AnnotatedReference[SecurityManager] = Field(description="The Security Manager implementation.")

    def get_agent_memory(self):
        file_memory = self.file_memory.instantiate()
        symbolic_memory = self.symbolic_memory.instantiate()
        vector_memory = self.similarity_memory.instantiate()
        return AgentMemory(
            file_memory=file_memory,
            symbolic_memory=symbolic_memory,
            similarity_memory=vector_memory,
        )


class AgentMachine(Specable[MachineSpec]):
    memory: AgentMemory
    security_manager: SecurityManager
    agent_controllers: List[AgentController]
    app: Optional[FastAPI]

    def __init__(self, spec: MachineSpec):
        super().__init__(spec)
        agents = {}
        for name, r in AgentOS.get_resources(AgentResource).items():
            with _error_wrapper(r):
                agents[name] = r.spec.instantiate()

        self.memory = self.spec.get_agent_memory()
        self.agent_controllers = [AgentController(name, agent) for name, agent in agents.items()]
        self.app = None
        self.security_manager = self.spec.security_manager.instantiate()

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


@contextmanager
def error_logger(filename: str = None):
    try:
        yield
    except Exception as e:
        raise ValueError(f"Error building resource {filename}") from e


def _error_wrapper(resource: Resource):
    return error_logger(AgentOS.get_resource_source(resource.kind, resource.metadata.name))
