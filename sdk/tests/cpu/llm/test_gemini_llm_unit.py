from pytest import fixture

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata


@fixture(scope="module", autouse=True)
async def server(run_app):
    resources = [
        Resource(
            apiVersion="eidolon/v1",
            kind="Agent",
            metadata=Metadata(name="default"),
            spec=dict(implementation=SimpleAgent.__name__,
                      apu="Gemini-1.5-Flash"),
        )
    ]
    async with run_app(*resources) as ra:
        yield ra


async def test_gemini(server):
    process = await Agent.get("default").create_process()
    resp = await process.action("converse", body="What is the capital of France?")
    assert "paris" in resp.data.lower()
