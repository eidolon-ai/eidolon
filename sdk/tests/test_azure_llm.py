import os

import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.test_utils.machine import TestMachine
from eidolon_ai_sdk.test_utils.server import serve_thread


os.environ.setdefault("AZURE_OPENAI_API_KEY", "testkey")

@pytest.fixture(scope="module")
def machine(tmp_path_factory):
    return TestMachine(tmp_path_factory.mktemp("test_utils_storage"))


@pytest.fixture(scope="module", autouse=True)
def server(machine):
    with serve_thread([machine, AgentResource(
        apiVersion="server.eidolonai.com/v1alpha1",
        metadata=Metadata(name="hello-world"),
        spec=dict(
            description="test agent",
            system_prompt="you are a helpful assistant who love emojis",
            apu=dict(llm_unit=dict(
                    implementation="AzureLLMUnit",
                    azure_endpoint="https://testinstancename.openai.azure.com/",
                    model=dict(implementation="gpt-3.5-turbo", name="gpt-35-turbo-16k"),
            ))
        )
    )]):
        yield


@pytest.mark.vcr
async def test_can_hit_generic_agent():
    process = await Agent.get("hello-world").create_process()
    response = await process.action("converse", json="what is the capital of france?")
    assert "paris" in response.data.lower()
