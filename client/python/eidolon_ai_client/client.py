from __future__ import annotations

import os
from typing import List, Any, AsyncIterator, Optional
from urllib.parse import urljoin

import jsonref
from pydantic import BaseModel, Field, Extra

from eidolon_ai_client.events import StreamEvent, StartAgentCallEvent, AgentStateEvent
from eidolon_ai_client.util.aiohttp import stream_content, get_content, post_content, delete


def current_machine_url() -> str:
    return os.environ.get("EIDOLON_LOCAL_MACHINE", "http://localhost:8080")


class Machine(BaseModel):
    machine: str = Field(default_factory=current_machine_url)

    async def get_schema(self) -> dict:
        url = urljoin(self.machine, "openapi.json")
        json_ = await get_content(url)
        return jsonref.replace_refs(json_)

    def agent(self, agent_name: str) -> Agent:
        return Agent(machine=self.machine, agent=agent_name)


class Agent(BaseModel):
    machine: str = Field(default_factory=current_machine_url)
    agent: str

    async def programs(self) -> List[str]:
        url = urljoin(self.machine, f"agents/{self.agent}/programs")
        return await get_content(url)

    async def create_process(self) -> Process:
        url = urljoin(self.machine, f"agents/{self.agent}/processes")
        json_ = await post_content(url)
        return Process(machine=self.machine, agent=self.agent, **json_)

    def process(self, process_id: str) -> Process:
        return Process(machine=self.machine, agent=self.agent, process_id=process_id)

    async def run_program(self, action_name: str, body: dict | BaseModel | str | None = None, **kwargs):
        process = await self.create_process()
        return await process.action(action_name, body, **kwargs)

    async def stream_program(self, action_name: str, body: Optional[Any] = None, **kwargs):
        process = await self.create_process()
        async for event in process.stream_action(action_name, body, **kwargs):
            yield event

    @classmethod
    def get(cls, location: str) -> Agent:
        """
        Convenience method to create Agents from dot notation. Ie: machine_loc.agent_name
        """
        if "." in location:
            parts = location.split(".")
            return cls(machine=".".join(parts[:-1]), agent=parts[-1])
        else:
            return cls(agent=location)


class Process(BaseModel):
    machine: str = Field(default_factory=current_machine_url)
    agent: str
    process_id: str

    async def action(self, action_name: str, body: dict | BaseModel | str | None = None, **kwargs) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}/actions/{action_name}")
        args = {
            "url": url, **kwargs
        }
        if body:
            args["json"] = body
        json_ = await post_content(**args)
        return ProcessStatus(machine=self.machine, agent=self.agent, **json_)

    def stream_action(self, action_name: str, body: Optional[Any] = None, **kwargs) -> AgentResponseIterator:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}/actions/{action_name}")
        return AgentResponseIterator(stream_content(url, body, **kwargs))

    async def status(self) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}/status")
        json_ = await get_content(url)
        return ProcessStatus(machine=self.machine, agent=self.agent, **json_)

    async def delete(self) -> DeleteProcessResponse:
        deleted = await delete(urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}"))
        return DeleteProcessResponse.model_validate(deleted)

    @classmethod
    def get(cls, stream_response: AgentResponseIterator):
        if not stream_response.machine or not stream_response.agent or not stream_response.process_id:
            raise ValueError("stream_response insufficiently iterated")
        return cls(machine=stream_response.machine, agent=stream_response.agent, process_id=stream_response.process_id)


class ProcessStatus(Process, extra=Extra.allow):
    state: str
    available_actions: List[str]


class AgentResponseIterator(AsyncIterator[StreamEvent]):
    """
    This class is used to iterate over the responses from an agent call and store the state of the conversation after the stream is complete.

    For example::

        agent_it = agent.stream_program("program_name", "some data")
        async for event in agent_it:
            # ... do something with the event ...
        process_id = agent_it.process_id

    """

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


class DeleteProcessResponse(BaseModel):
    process_id: str
    deleted: int
