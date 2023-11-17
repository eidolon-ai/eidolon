from __future__ import annotations

from fastapi import FastAPI

from .agent_machine import AgentMachine


class AgentCallContext:
    conversation_id: str
    agent_name: str
    state_name: str


class AgentOS:
    machine: AgentMachine
    app: FastAPI = None

    def __init__(self, machine: AgentMachine):
        self.machine = machine

    async def start(self, app: FastAPI):
        self.app = app
        for program in self.machine.agent_programs:
            await program.start(app)

        self.machine.agent_memory.start()

    def stop(self):
        for program in self.machine.agent_programs:
            program.stop(self.app)
        self.machine.agent_memory.stop()

    @staticmethod
    def from_yaml(machine_yaml):
        return AgentOS(AgentMachine.from_yaml(machine_yaml))
