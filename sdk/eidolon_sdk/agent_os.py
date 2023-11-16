from __future__ import annotations

from typing import Optional

from fastapi import FastAPI

from .agent_machine import AgentMachine, YamlAgentMachine


class AgentCallContext:
    conversation_id: str
    agent_name: str
    state_name: str


class AgentOS:
    machine: AgentMachine
    app: FastAPI = None

    def __init__(self, machine_yaml: str, machine: Optional[AgentMachine] = None):
        self.machine = machine or YamlAgentMachine(machine_yaml)

    def start(self, app: FastAPI):
        self.app = app
        for program in self.machine.agent_programs:
            program.start(app)

        self.machine.agent_memory.start()

    def stop(self):
        for program in self.machine.agent_programs:
            program.stop(self.app)
        self.machine.agent_memory.stop()
