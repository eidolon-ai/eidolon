from __future__ import annotations

import logging.config

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
        logger = logging.getLogger("eidolon")
        logger.info("Starting AgentOS")
        self.app = app
        await self.machine.start(app)

    async def stop(self):
        await self.machine.stop()
