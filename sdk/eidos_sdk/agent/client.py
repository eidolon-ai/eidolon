from __future__ import annotations

import os
from typing import List, Any
from urllib.parse import urljoin

import jsonref
from aiohttp import ClientResponse
from pydantic import BaseModel

from eidos_sdk.util.aiohttp import ContextualClientSession

_default_machine = os.environ.get("EIDOS_LOCAL_MACHINE", "localhost:8080")


async def _process_status_from_resp(machine: str, agent: str, resp: ClientResponse) -> ProcessStatus:
    resp.raise_for_status()
    json_ = await resp.json()
    return ProcessStatus(machine=machine, agent=agent, **json_)


class Machine(BaseModel):
    machine: str = _default_machine

    async def get_schema(self) -> dict:
        url = urljoin(self.machine, "openapi.json")
        async with ContextualClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                json_ = await resp.json()
                return jsonref.replace_refs(json_)

    def agent(self, agent_name: str) -> Agent:
        return Agent(machine=self.machine, agent=agent_name)


class Agent(BaseModel):
    machine: str = _default_machine
    agent: str

    async def program(self, program_name: str, body: dict | BaseModel) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/programs/{program_name}")
        body = body.model_dump() if isinstance(body, BaseModel) else body
        async with ContextualClientSession() as session:
            async with session.post(url, json=body) as resp:
                return await _process_status_from_resp(self.machine, self.agent, resp)

    def process(self, process_id: str) -> Process:
        return Process(machine=self.machine, agent=self.agent, pid=process_id)

    @classmethod
    def get(cls, location: str) -> Agent:
        """
        Convenience method to create Agents from dot notation. Ie: machine_loc.agent_name
        """
        if "." in location:
            parts = location.split()
            return cls(machine=".".join(parts[:-1]), agent=parts[-1])
        else:
            return cls(agent=location)


class Process(BaseModel):
    machine: str = _default_machine
    agent: str
    process_id: str

    async def action(self, action_name: str, body: dict | BaseModel) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}/actions/{action_name}")
        body = body.model_dump() if isinstance(body, BaseModel) else body
        async with ContextualClientSession() as session:
            async with session.post(url, json=body) as resp:
                return await _process_status_from_resp(self.machine, self.agent, resp)

    async def status(self) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}/status")
        async with ContextualClientSession() as session:
            async with session.get(url) as resp:
                return await _process_status_from_resp(self.machine, self.agent, resp)


class ProcessStatus(Process):
    state: str
    available_actions: List[str]
    data: Any
