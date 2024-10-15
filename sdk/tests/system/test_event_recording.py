import httpx
import pytest_asyncio
from fastapi import Body, HTTPException
from typing import Annotated

from eidolon_ai_sdk.agent.agent import register_program
from eidolon_ai_client.client import Agent, ProcessStatus
from eidolon_ai_client.events import (
    AgentStateEvent,
    StringOutputEvent,
    StartAgentCallEvent,
    SuccessEvent,
    UserInputEvent,
)


async def run_program(agent, program, **kwargs) -> ProcessStatus:
    process = await Agent.get(agent).create_process()
    return await process.action(program, **kwargs)


class HelloWorld:
    @register_program()
    async def idle(self, name: Annotated[str, Body()]):
        if name.lower() == "hello":
            raise HTTPException(418, "hello is not a name")
        if name.lower() == "error":
            raise Exception("big bad server error")
        return f"Hello, {name}!"

    @register_program()
    async def idle_streaming(self, name: Annotated[str, Body()]):
        if name.lower() == "hello":
            raise HTTPException(418, "hello is not a name")
        if name.lower() == "error":
            raise Exception("big bad server error")
        yield StringOutputEvent(content="Hello, !")
        yield StringOutputEvent(content=f"{name}!")


class TestHelloWorld:
    @pytest_asyncio.fixture(scope="class")
    async def server(self, run_app):
        async with run_app(HelloWorld) as ra:
            yield ra

    @pytest_asyncio.fixture(scope="function")
    async def client(self, server):
        async with httpx.AsyncClient(base_url=server, timeout=httpx.Timeout(60)) as client:
            yield client

    def compare_events(self, events, expected_events):
        assert len(events) == len(expected_events)
        for event, expected_event in zip(events, expected_events):
            event_copy = event.copy()
            expected_event_copy = expected_event.model_dump()

            if not expected_event_copy["stream_context"]:
                del expected_event_copy["stream_context"]

            expected_event_copy["category"] = expected_event_copy["category"].value
            if hasattr(expected_event_copy["event_type"], "value"):
                expected_event_copy["event_type"] = expected_event_copy["event_type"].value

            assert event_copy == expected_event_copy

    async def test_hello_world(self, server, client):
        process = await Agent.get("HelloWorld").create_process()
        post = await process.action("idle", "world")
        assert post.data == "Hello, world!"
        events = await process.events()
        expected_events = [
            UserInputEvent(input=dict(name="world")),
            StartAgentCallEvent(
                machine=server, agent_name="HelloWorld", call_name="idle", process_id=process.process_id,
                title="", sub_title="",
            ),
            StringOutputEvent(content="Hello, world!"),
            AgentStateEvent(state="terminated", available_actions=[]),
            SuccessEvent(),
        ]

        self.compare_events(events, expected_events)

    async def test_hello_world_streaming(self, client):
        agent = Agent.get("HelloWorld")
        process = await agent.create_process()
        stream = (process).stream_action("idle_streaming", "error")
        server_events = []
        process_id = None
        async for e in stream:
            server_events.append(e)
            if isinstance(e, StartAgentCallEvent):
                process_id = e.process_id

        assert process_id is not None

        events = await process.events()
        self.compare_events(events, server_events)
