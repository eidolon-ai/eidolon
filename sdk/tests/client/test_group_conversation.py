from typing import Annotated

import pytest_asyncio
from fastapi import Body
from pydantic import BaseModel

from eidolon_ai_client.client import Machine
from eidolon_ai_client.events import (
    StringOutputEvent,
    AgentStateEvent,
    StartAgentCallEvent,
    StartStreamContextEvent,
    UserInputEvent,
    SuccessEvent,
    EndStreamContextEvent,
)
from eidolon_ai_client.group_conversation import GroupConversation
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.system.resources.resources_base import Metadata, Resource
from eidolon_ai_sdk.util.class_utils import fqn


class HelloWorldSpec(BaseModel):
    my_name: str


class HelloWorld(Specable[HelloWorldSpec]):
    @register_action("initialized", "idle")
    async def idle(self, name: Annotated[str, Body()]):
        yield StringOutputEvent(content=f"{self.spec.my_name} says: hello, {name}!")
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def reply(self, name: Annotated[str, Body()]):
        yield StringOutputEvent(content=f"{self.spec.my_name} says: hello, {name}!")
        yield AgentStateEvent(state="idle")


def a(name: str):
    # noinspection PyArgumentList
    return Resource(
        kind="Agent",
        apiVersion="eidolon/v1",
        spec=dict(implementation=fqn(HelloWorld), my_name=name),
        metadata=Metadata(name=name),
    )


@pytest_asyncio.fixture(scope="module")
async def server(run_app):
    async with run_app(a("fred"), a("barney"), a("wilma"), a("betty")) as ra:
        yield ra


async def test_action(server):
    conversation = await GroupConversation.create(["fred", "barney", "wilma", "betty"])
    results = await conversation.action("idle", body="Dave")
    expected = [
        "fred says: hello, Dave!",
        "barney says: hello, Dave!",
        "wilma says: hello, Dave!",
        "betty says: hello, Dave!",
    ]
    assert expected == [event.data for event in results]


async def test_stream_action(server):
    conversation = await GroupConversation.create(["fred", "barney", "wilma", "betty"])
    conversations_by_context = {}
    agents_to_context = {}
    async for event in conversation.stream_action("idle", body="Dave"):
        context = event.stream_context or ""
        if context not in conversations_by_context:
            conversations_by_context[context] = []
        conversations_by_context[context].append(event)
        if isinstance(event, StartAgentCallEvent):
            agents_to_context[event.agent_name] = event.process_id

    def expected_user_events(name, process_id):
        return [
            UserInputEvent(stream_context=name, input={"name": "Dave"}),
            StartAgentCallEvent(
                stream_context=name, machine=Machine().machine, agent_name=name, call_name="idle", process_id=process_id,
                title='', sub_title=''
            ),
            StringOutputEvent(stream_context=name, content=f"{name} says: hello, Dave!"),
            AgentStateEvent(stream_context=name, state="idle", available_actions=["idle", "reply"]),
            SuccessEvent(
                stream_context=name,
            ),
        ]

    for name in ["fred", "barney", "wilma", "betty"]:
        assert StartStreamContextEvent(context_id=name, title=name) in conversations_by_context[""]
        assert EndStreamContextEvent(context_id=name) in conversations_by_context[""]
        assert conversations_by_context[name] == expected_user_events(name, agents_to_context[name])
