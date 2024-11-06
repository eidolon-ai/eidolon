from typing import Type

import pytest

from eidolon_ai_client import client
from eidolon_ai_client.events import StringOutputEvent
from eidolon_ai_sdk.system.agent_builder import AgentBuilderBase
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn


def r(impl: Type[AgentBuilderBase], **kwargs):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=impl.__name__),
        spec=dict(implementation=fqn(impl), **kwargs),
    )


class BasicAgent(AgentBuilderBase):
    foo: str


@BasicAgent.action()
async def ba_action(spec: BasicAgent):
    return spec.foo


class DynamicAgent(AgentBuilderBase):
    foo: str


@DynamicAgent.dynamic_contract
def da_contract(spec: DynamicAgent):
    @DynamicAgent.action()
    async def da_action():
        return spec.foo


class YieldingAgent(AgentBuilderBase):
    pass


@YieldingAgent.action()
async def ya_action():
    yield StringOutputEvent(content="b")
    yield StringOutputEvent(content="a")
    yield StringOutputEvent(content="r")


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    async with run_app(
            r(BasicAgent, foo="bar"),
            r(DynamicAgent, foo="bar"),
            r(YieldingAgent),
    ) as ra:
        yield ra


async def test_action():
    process = await client.Agent.get(BasicAgent.__name__).create_process()
    resp = await process.action("ba_action")
    assert resp.data == "bar"


async def test_dynamic_contract():
    process = await client.Agent.get(DynamicAgent.__name__).create_process()
    resp = await process.action("da_action")
    assert resp.data == "bar"


async def test_yielding_agent():
    process = await client.Agent.get(YieldingAgent.__name__).create_process()
    resp = await process.action("ya_action")
    assert resp.data == "bar"
