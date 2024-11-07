from __future__ import annotations

import os
from typing import List, Any, AsyncIterator, Optional
from urllib.parse import urljoin

import jsonref
from pydantic import BaseModel, Field

from eidolon_ai_client.events import StreamEvent, StartAgentCallEvent, AgentStateEvent, FileHandle
from eidolon_ai_client.util.aiohttp import stream_content, get_content, post_content, delete, get_raw


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

    async def process(self, process_id: str) -> ProcessStatus:
        url = urljoin(self.machine, f"processes/{process_id}")
        json_ = await get_content(url)
        if 'machine' not in json_:
            json_['machine'] = self.machine
        return ProcessStatus(**json_)

    async def processes(self) -> ProcessesResponse:
        url = urljoin(self.machine, "/processes")
        json_ = await get_content(url)
        json_['processes'] = [{"machine":self.machine, **kwargs} for kwargs in json_['processes']]
        return ProcessesResponse(**json_)

    async def openapi(self) -> dict:
        url = urljoin(self.machine, "/openapi.json")
        return await get_content(url)

    async def list_agents(self) -> List[str]:
        schema = await self.openapi()
        return [p.split("/")[2] for p in schema["paths"] if p.startswith("/agents/")]


class Agent(BaseModel):
    machine: str = Field(default_factory=current_machine_url)
    agent: str

    async def programs(self) -> List[str]:
        url = urljoin(self.machine, f"agents/{self.agent}/programs")
        return await get_content(url)

    async def create_process(self, parent_process_id: Optional[str] = None) -> ProcessStatus:
        url = urljoin(self.machine, "/processes")
        options = {
            "agent": self.agent
        }
        if parent_process_id:
            options["parent_process_id"] = parent_process_id
        json_ = await post_content(url, json=options)
        return ProcessStatus(**{"machine":self.machine, **json_})

    def process(self, process_id: str) -> Process:
        return Process(machine=self.machine, agent=self.agent, process_id=process_id)

    async def processes(self) -> ProcessesResponse:
        url = urljoin(self.machine, "/processes")
        json_ = await get_content(url)
        json_['processes'] = [{"machine":self.machine, **kwargs} for kwargs in json_['processes']]
        return ProcessesResponse(**json_)

    async def run_program(self, action_name: str, body: dict | BaseModel | str | None = None, **kwargs) -> ProcessStatus:
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
    process_id: str

    async def upload_file(self, file_contents: bytes) -> FileHandle:
        url = urljoin(self.machine, f"processes/{self.process_id}/files")
        json_ = await post_content(url, content=file_contents, headers={"Content-Type": "application/octet-stream"})
        return FileHandle.model_validate(json_)

    async def set_metadata(self, file_id: str, metadata: dict):
        url = urljoin(self.machine, f"processes/{self.process_id}/files/{file_id}/metadata")
        json_ = await post_content(url, json=metadata)
        return FileHandle.model_validate(json_)

    async def download_file(self, file_id: str) -> bytes:
        url = urljoin(self.machine, f"processes/{self.process_id}/files/{file_id}")
        return await get_raw(url)

    async def delete_file(self, file_id: str) -> None:
        url = urljoin(self.machine, f"processes/{self.process_id}/files/{file_id}")
        await delete(url)

    async def action(self, agent: str, action_name: str, body: dict | BaseModel | str | None = None, **kwargs) -> ProcessStatus:
        url = urljoin(self.machine, f"processes/{self.process_id}/agent/{agent}/actions/{action_name}")
        args = {
            "url": url, **kwargs
        }
        if body:
            args["json"] = body
        json_ = await post_content(**args)
        return ProcessStatus(**{"machine": self.machine, **json_})

    def stream_action(self, agent: str, action_name: str, body: Optional[Any] = None, **kwargs) -> AgentResponseIterator:
        url = urljoin(self.machine, f"processes/{self.process_id}/agent/{agent}/actions/{action_name}")
        return AgentResponseIterator(stream_content(url, body, **kwargs))

    async def status(self) -> ProcessStatus:
        url = urljoin(self.machine, f"processes/{self.process_id}")
        json_ = await get_content(url)
        if 'machine' not in json_:
            json_['machine'] = self.machine
        return ProcessStatus(**json_)

    async def events(self):
        url = urljoin(self.machine, f"processes/{self.process_id}/events")
        return await get_content(url)

    async def delete(self) -> DeleteProcessResponse:
        deleted = await delete(urljoin(self.machine, f"processes/{self.process_id}"))
        return DeleteProcessResponse.model_validate(deleted)

    @classmethod
    def get(cls, stream_response: AgentResponseIterator):
        if not stream_response.machine or not stream_response.agent or not stream_response.process_id:
            raise ValueError("stream_response insufficiently iterated")
        return cls(machine=stream_response.machine, agent=stream_response.agent, process_id=stream_response.process_id)


class ProcessesResponse(BaseModel):
    total: int
    processes: List[ProcessStatus]
    next: Optional[str] = None


class ProcessStatus(Process, extra="allow"):
    agent: str
    state: str
    title: Optional[str]
    available_actions: List[str]

    async def action(self, action_name: str, body: dict | BaseModel | str | None = None, **kwargs) -> ProcessStatus:
        if "agent" in kwargs:
            del kwargs["agent"]
        return await super().action(self.agent, action_name, body, **kwargs)

    def stream_action(self, action_name: str, body: Optional[Any] = None, **kwargs) -> AgentResponseIterator:
        if "agent" in kwargs:
            del kwargs["agent"]
        return super().stream_action(self.agent, action_name, body, **kwargs)


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
