from __future__ import annotations

import os
from typing import List, Any, TypeVar, Type
from urllib.parse import urljoin

import jsonref
from pydantic import BaseModel, TypeAdapter
from pydantic_core import to_jsonable_python

from eidos_sdk.util.aiohttp import ContextualClientSession

_default_machine = os.environ.get("EIDOS_LOCAL_MACHINE", "http://localhost:8080")


class Machine(BaseModel):
    machine: str = _default_machine

    async def get_schema(self) -> dict:
        url = urljoin(self.machine, "openapi.json")
        json_ = await _get(url)
        return jsonref.replace_refs(json_)

    def agent(self, agent_name: str) -> Agent:
        return Agent(machine=self.machine, agent=agent_name)


class Agent(BaseModel):
    machine: str = _default_machine
    agent: str

    async def program(self, program_name: str, body) -> ProcessStatus:
        return await Program(machine=self.machine, agent=self.agent, program=program_name).execute(body)

    def process(self, process_id: str) -> Process:
        return Process(machine=self.machine, agent=self.agent, process_id=process_id)

    @classmethod
    def get(cls, location: str) -> Agent:
        """
        Convenience method to create Agents from dot notation. Ie: machine_loc.agent_name
        """
        machine, agent = _parse_agent(location)
        return cls(machine=machine, agent=agent)


class Program(BaseModel):
    machine: str = _default_machine
    agent: str
    program: str

    async def execute(self, body) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/programs/{self.program}")
        json_ = await _post(url, to_jsonable_python(body))
        return ProcessStatus(machine=self.machine, agent=self.agent, **json_)

    @classmethod
    def get(cls, location: str):
        parts = location.split(".")
        machine, agent = _parse_agent(".".join(parts[:-1]))
        return cls(machine=machine, agent=agent, program=parts[-1])


T = TypeVar("T")


class Process(BaseModel):
    machine: str = _default_machine
    agent: str
    process_id: str

    async def action(self, action_name: str, body: dict | BaseModel) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}/actions/{action_name}")
        body = body.model_dump() if isinstance(body, BaseModel) else body
        json_ = await _post(url, body)
        return ProcessStatus(machine=self.machine, agent=self.agent, **json_)

    async def status(self) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}/status")
        json_ = await _get(url)
        return ProcessStatus(machine=self.machine, agent=self.agent, **json_)


class ProcessStatus(Process):
    state: str
    available_actions: List[str]
    data: Any

    def parse(self, t: Type[T]) -> T:
        model = TypeAdapter(t)
        return model.validate_python(self.data)


#  _get and _post are separated to be easily mocked by tests


async def _get(url):
    async with ContextualClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()


async def _post(url, json):
    async with ContextualClientSession() as session:
        async with session.post(url, json=json) as resp:
            resp.raise_for_status()
            return await resp.json()


def _parse_agent(location: str):
    if "." in location:
        parts = location.split(".")
        return ".".join(parts[:-1]), parts[-1]
    else:
        return _default_machine, location
