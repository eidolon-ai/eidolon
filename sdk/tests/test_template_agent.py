import pytest

from eidolon_ai_sdk.agent.client import Agent
from eidolon_ai_sdk.agent.template_agent import SimpleAgent
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata


def r(name, **kwargs):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=name),
        spec=dict(implementation=SimpleAgent.__name__, **kwargs),
    )


@pytest.fixture(scope="module")
def default_resource():
    return r("default_template_agent")


@pytest.fixture(scope="module")
async def server(run_app, default_resource):
    async with run_app(default_resource) as ra:
        yield ra


@pytest.fixture
async def default_agent(server):
    return Agent.get("default_template_agent")


async def test_default_agent(default_agent: Agent):
    process = await default_agent.create_process()
    resp = await process.action("converse", body=dict(statement="What is the capital of France?"))
    assert "paris" in resp.data.lower()
