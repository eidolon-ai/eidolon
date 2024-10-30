import pytest
from pydantic import BaseModel

from eidolon_ai_client import client
from eidolon_ai_client.events import StringOutputEvent
from eidolon_ai_sdk.system.agent_builder import Agent
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata


class Spec(BaseModel):
    foo: str


def r(impl, **kwargs):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=impl),
        spec=dict(implementation=__name__ + "." + impl, **kwargs),
    )


basic_agent = Agent(Spec)


@basic_agent.action()
async def ba_action(spec: Spec):
    return spec.foo


dynamic_agent = Agent(Spec)


@dynamic_agent.dynamic_contract
def da_contract(spec: Spec):
    @dynamic_agent.action()
    async def da_action():
        return spec.foo


yielding_agent = Agent()


@yielding_agent.action()
async def ya_action():
    yield StringOutputEvent(content="b")
    yield StringOutputEvent(content="a")
    yield StringOutputEvent(content="r")


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    async with run_app(
            r("basic_agent", foo="bar"),
            r("dynamic_agent", foo="bar"),
            r("yielding_agent"),
    ) as ra:
        yield ra


async def test_action():
    process = await client.Agent.get("basic_agent").create_process()
    resp = await process.action("ba_action")
    assert resp.data == "bar"


async def test_dynamic_contract():
    process = await client.Agent.get("dynamic_agent").create_process()
    resp = await process.action("da_action")
    assert resp.data == "bar"


async def test_yielding_agent():
    process = await client.Agent.get("yielding_agent").create_process()
    resp = await process.action("ya_action")
    assert resp.data == "bar"
