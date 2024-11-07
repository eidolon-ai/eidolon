from pytest import fixture

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.apu.llm.ollama_llm_unit import OllamaLLMUnit
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@fixture(scope="module", autouse=True)
async def server(run_app):
    resources = [
        Resource(
            apiVersion="eidolon/v1",
            kind="Reference",
            metadata=Metadata(name="OllamaLLMUnit"),
            spec=dict(
                implementation=fqn(OllamaLLMUnit),
                temperature=-1
            ),

        ),
        Resource(
            apiVersion="eidolon/v1",
            kind="Agent",
            metadata=Metadata(name="default"),
            spec=dict(implementation="SimpleAgent", apu="Llamma3-8b"),
        )
    ]
    async with run_app(*resources) as ra:
        yield ra


async def test_llama3(server):
    process = await Agent.get("default").create_process()
    resp = await process.action("converse", body="What is the capital of France?")
    assert "paris" in resp.data.lower()
