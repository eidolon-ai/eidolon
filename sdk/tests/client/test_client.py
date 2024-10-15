from typing import Annotated

import pytest_asyncio
from fastapi import Body

from eidolon_ai_client import client
from eidolon_ai_client.client import Agent
from eidolon_ai_client.events import (
    StringOutputEvent,
    AgentStateEvent,
    UserInputEvent,
    Category,
    StartAgentCallEvent,
    SuccessEvent,
)
from eidolon_ai_sdk.agent.agent import register_action


class HelloWorld:
    @register_action("initialized", "idle")
    async def idle(self, name: Annotated[str, Body()]):
        yield StringOutputEvent(content=f"Hello, {name}!")
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def reply(self, name: Annotated[str, Body()]):
        yield StringOutputEvent(content=f"Hello, {name}!")
        yield AgentStateEvent(state="idle")


@pytest_asyncio.fixture(scope="module")
async def server(run_app):
    async with run_app(HelloWorld) as ra:
        yield ra


async def test_create_process(server):
    agent = Agent.get("HelloWorld")
    process = await agent.create_process()
    resp = await process.action("idle", body="Dave")
    assert "Hello, Dave!" in resp.data
    resp = await process.action("reply", body="Jim")
    assert "Hello, Jim!" in resp.data


async def test_stream_program(server):
    agent = Agent.get("HelloWorld")
    process = await agent.create_process()
    resp = [event async for event in process.stream_action("idle", body="Dave")]
    expected = [
        UserInputEvent(stream_context=None, category=Category.INPUT, event_type="user_input", input={"name": "Dave"}),
        StartAgentCallEvent(
            stream_context=None,
            category=Category.START,
            event_type="agent_call",
            title='',
            sub_title='',
            machine=client.current_machine_url(),
            agent_name="HelloWorld",
            call_name="idle",
            process_id="test_stream_program_0",
        ),
        StringOutputEvent(stream_context=None, category=Category.OUTPUT, event_type="string", content="Hello, Dave!"),
        AgentStateEvent(
            stream_context=None,
            category=Category.TRANSFORM,
            event_type="agent_state",
            state="idle",
            available_actions=["idle", "reply"],
        ),
        SuccessEvent(stream_context=None, category=Category.END, event_type="success"),
    ]
    assert expected == resp


async def test_stream_followup(server):
    agent = Agent.get("HelloWorld")
    process = await agent.create_process()
    expected = [
        UserInputEvent(stream_context=None, category=Category.INPUT, event_type="user_input", input={"name": "Dave"}),
        StartAgentCallEvent(
            stream_context=None,
            category=Category.START,
            title='',
            sub_title='',
            event_type="agent_call",
            machine=client.current_machine_url(),
            agent_name="HelloWorld",
            call_name="idle",
            process_id="test_stream_followup_0",
        ),
        StringOutputEvent(stream_context=None, category=Category.OUTPUT, event_type="string", content="Hello, Dave!"),
        AgentStateEvent(
            stream_context=None,
            category=Category.TRANSFORM,
            event_type="agent_state",
            state="idle",
            available_actions=["idle", "reply"],
        ),
        SuccessEvent(stream_context=None, category=Category.END, event_type="success"),
    ]
    resp = [event async for event in process.stream_action("idle", body="Dave")]
    assert expected == resp

    expected = [
        UserInputEvent(stream_context=None, category=Category.INPUT, event_type="user_input", input={"name": "Jim"}),
        StartAgentCallEvent(
            stream_context=None,
            category=Category.START,
            title='',
            sub_title='',
            event_type="agent_call",
            machine=client.current_machine_url(),
            agent_name="HelloWorld",
            call_name="reply",
            process_id="test_stream_followup_0",
        ),
        StringOutputEvent(stream_context=None, category=Category.OUTPUT, event_type="string", content="Hello, Jim!"),
        AgentStateEvent(
            stream_context=None,
            category=Category.TRANSFORM,
            event_type="agent_state",
            state="idle",
            available_actions=["idle", "reply"],
        ),
        SuccessEvent(stream_context=None, category=Category.END, event_type="success"),
    ]
    resp = [event async for event in process.stream_action("reply", body="Jim")]
    assert expected == resp
