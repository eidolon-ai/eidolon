from __future__ import annotations

import jsonref
import os
from pydantic import BaseModel
from typing import List, Any, AsyncIterator
from urllib.parse import urljoin

from eidos_sdk.io.events import StreamEvent, StartAgentCallEvent, AgentStateEvent
from eidos_sdk.util.aiohttp import ContextualClientSession, stream_content

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

    def stream_program(self, program_name, body: Any) -> AsyncIterator[StreamEvent]:
        body = body.model_dump() if isinstance(body, BaseModel) else body
        url = urljoin(self.machine, f"agents/{self.agent}/programs/{program_name}")
        return AgentResponseIterator(stream_content(url, body))

    def stream_action(self, action_name: str, process_id: str, body: Any) -> AsyncIterator[StreamEvent]:
        body = body.model_dump() if isinstance(body, BaseModel) else body
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{process_id}/actions/{action_name}")
        return AgentResponseIterator(stream_content(url, body))

    async def program(self, program_name: str, body: dict | BaseModel) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/programs/{program_name}")
        body = body.model_dump() if isinstance(body, BaseModel) else body
        json_ = await _post(url, body)
        return ProcessStatus(machine=self.machine, agent=self.agent, **json_)

    def process(self, process_id: str) -> Process:
        return Process(machine=self.machine, agent=self.agent, process_id=process_id)

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


class AgentResponseIterator:
    data: AsyncIterator[StreamEvent]
    machine: str
    agent: str
    process_id: str
    state: str
    available_actions: List[str]

    def __init__(self, data: AsyncIterator[StreamEvent]):
        self.data = data.__aiter__()

    async def __anext__(self):
        try:
            event = await self.data.__anext__()
        except StopAsyncIteration:
            await self.iteration_complete()
            raise
        if event.is_root_and_type(StartAgentCallEvent):
            self.machine = event.machine
            self.agent = event.agent_name
            self.process_id = event.process_id
        elif event.is_root_and_type(AgentStateEvent):
            self.state = event.state
            self.available_actions = event.available_actions

        return event

    def __aiter__(self):
        return self

    async def iteration_complete(self):
        pass
