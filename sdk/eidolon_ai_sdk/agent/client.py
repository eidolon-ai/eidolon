from __future__ import annotations

import jsonref
from pydantic import BaseModel, Field, Extra
from typing import List, Any, AsyncIterator, Optional
from urllib.parse import urljoin

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.io.events import StreamEvent, StartAgentCallEvent, AgentStateEvent
from eidolon_ai_sdk.util.aiohttp import stream_content, get_content, post_content


class Machine(BaseModel):
    machine: str = Field(default_factory=AgentOS.current_machine_url)

    async def get_schema(self) -> dict:
        url = urljoin(self.machine, "openapi.json")
        json_ = await get_content(url)
        return jsonref.replace_refs(json_)

    def agent(self, agent_name: str) -> Agent:
        return Agent(machine=self.machine, agent=agent_name)


class Agent(BaseModel):
    machine: str = Field(default_factory=AgentOS.current_machine_url)
    agent: str

    def stream_program(self, program_name: str, body: Optional[Any] = None) -> AgentResponseIterator:
        return Program(machine=self.machine, agent=self.agent, program=program_name).stream_execute(body)

    async def program(self, program_name: str, body: Optional[Any] = None) -> ProcessStatus:
        return await Program(machine=self.machine, agent=self.agent, program=program_name).execute(body)

    def stream_action(self, action_name: str, process_id: str, body: Any) -> AgentResponseIterator:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{process_id}/actions/{action_name}")
        return AgentResponseIterator(stream_content(url, body))

    def process(self, process_id: str) -> Process:
        return Process(machine=self.machine, agent=self.agent, process_id=process_id)

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


class Program(BaseModel):
    machine: str = Field(default_factory=AgentOS.current_machine_url)
    agent: str
    program: str

    @classmethod
    def get(cls, location: str):
        parts = location.split(".")
        kwargs = dict(program=parts[-1], agent=parts[-2])
        if len(parts) > 2:
            kwargs["machine"] = ".".join(parts[:-2])
        return cls(**kwargs)

    def stream_execute(self, body: Optional[Any] = None) -> AgentResponseIterator:
        url = urljoin(self.machine, f"agents/{self.agent}/programs/{self.program}")
        return AgentResponseIterator(stream_content(url, body))

    async def execute(self, body: Optional[Any] = None) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/programs/{self.program}")
        json_ = await post_content(url, body)
        return ProcessStatus(machine=self.machine, agent=self.agent, **json_)


class Process(BaseModel):
    machine: str = Field(default_factory=AgentOS.current_machine_url)
    agent: str
    process_id: str

    async def action(self, action_name: str, body: dict | BaseModel) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}/actions/{action_name}")
        json_ = await post_content(url, body)
        return ProcessStatus(machine=self.machine, agent=self.agent, **json_)

    async def status(self) -> ProcessStatus:
        url = urljoin(self.machine, f"agents/{self.agent}/processes/{self.process_id}/status")
        json_ = await get_content(url)
        return ProcessStatus(machine=self.machine, agent=self.agent, **json_)

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
