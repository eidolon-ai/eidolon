import pytest

from eidolon_ai_sdk.agent.client import Agent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.cpu.logic_unit import llm_function, LogicUnit
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn


class MeaningOfLife(LogicUnit):
    @llm_function()
    async def meaning_of_life_tool(self) -> str:
        """
        call this tool to get the meaning of life
        """
        return "42"


def r(name, **kwargs):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=name),
        spec=dict(implementation=SimpleAgent.__name__, **kwargs),
    )


image_compatible_cpu = dict(
    model="gpt-4-vision-preview",
    force_json=False,
    max_tokens=4096,
)


resources = [
    r("default"),
    r("multiple_prompt_args", actions=[dict(user_prompt="{{ a1 }} {{ a2 }}")]),
    r("json_output", actions=[
        dict(output_schema=dict(type="object", properties=dict(capital=dict(type="string"), population=dict(type="number"))))
    ]),
    r("states", actions=[
        dict(name="first", allowed_states=["initialized"], output_state="s2"),
        dict(name="second", allowed_states=["s2"])]),
    r("refs", agent_refs=['default']),
    r("with_tools", cpu=dict(logic_units=[fqn(MeaningOfLife)])),
    r("optional_file", files="single-optional", cpu=image_compatible_cpu),
    r("single_file", files="single", cpu=image_compatible_cpu),
    r("multiple_files", files="multiple", cpu=image_compatible_cpu),
]


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    async with run_app(*resources) as ra:
        yield ra


async def test_default_agent():
    body = dict(statement="What is the capital of France?")
    resp = await Agent.get('default').program("converse", body=body)
    assert "paris" in resp.data.lower()
