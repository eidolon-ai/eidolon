import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.cpu.llm.open_ai_llm_unit import ArgBuilder
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


class BadTokenArgBuilder(ArgBuilder):
    def get_args(self) -> dict:
        return {"base_url": "foobar", "timeout": .1}


def r(name, **kwargs):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=name),
        spec=dict(implementation=SimpleAgent.__name__, **kwargs),
    )


image_compatible_cpu = dict(
    llm_unit=dict(
        model="gpt-4-vision-preview",
        force_json=False,
        max_tokens=4096,
    )
)

resources = [
    r("default"),
    r("test_no_vars", actions=[dict(user_prompt="What is the capital of France?")]),
    r("multiple_prompt_args", actions=[dict(user_prompt="{{ a1 }} {{ a2 }}")]),
    r(
        "json_output",
        actions=[
            dict(
                output_schema=dict(
                    type="object", properties=dict(capital=dict(type="string"), population=dict(type="number"))
                )
            )
        ],
    ),
    r(
        "states",
        actions=[
            dict(name="first", allowed_states=["initialized"], output_state="s2"),
            dict(name="second", allowed_states=["s2"]),
        ],
    ),
    r("system_prompt", system_prompt="You are a helpful assistant, and your favorite country is France"),
    r("refs", agent_refs=["system_prompt"]),
    r("with_tools", cpu=dict(logic_units=[fqn(MeaningOfLife)])),
    r("optional_file", actions=[dict(files="single-optional")], cpu=image_compatible_cpu),
    r(
        "optional_file_no_body",
        actions=[dict(files="single-optional", user_prompt="How many legs does the animal have?")],
        cpu=image_compatible_cpu,
    ),
    r("single_file", actions=[dict(files="single")], cpu=image_compatible_cpu),
    r(
        "single_file_no_body",
        actions=[dict(files="single", user_prompt="How many legs does the animal have?")],
        cpu=image_compatible_cpu,
    ),
    r("multiple_files", actions=[dict(files="multiple")], cpu=image_compatible_cpu),
    r(
        "multiple_files_no_body",
        actions=[dict(files="multiple", user_prompt="what do these images have in common?")],
        cpu=image_compatible_cpu,
    ),
    r("dynamic_client_args", cpu=dict(llm_unit=dict(client_arg_builder=dict(implementation=fqn(BadTokenArgBuilder))))),
]


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    async with run_app(*resources) as ra:
        yield ra


async def test_default_agent():
    process = await Agent.get("default").create_process()
    resp = await process.action("converse", body="What is the capital of France?")
    assert "paris" in resp.data.lower()


async def test_no_vars():
    process = await Agent.get("test_no_vars").create_process()
    resp = await process.action("converse")
    assert "paris" in resp.data.lower()


async def test_multiple_prompt_args():
    process = await Agent.get("multiple_prompt_args").create_process()
    resp = await process.action("converse", body=dict(a1="What is the capital of", a2="France?"))
    assert "paris" in resp.data.lower()


async def test_json_output():
    process = await Agent.get("json_output").create_process()
    resp = await process.action("converse", body="What is the capital of France?")
    assert "population" in resp.data
    assert isinstance(resp.data["population"], int) and resp.data["population"] > 0
    assert "paris" in resp.data["capital"].lower()


async def test_states():
    process = await Agent.get("states").create_process()
    status = await process.status()
    assert status.state == "initialized"
    assert status.available_actions == ["first"]
    first = await process.action("first", body="What is the capital of France?")
    status = await first.status()
    assert status.state == "s2"
    assert status.available_actions == ["second"]
    assert "paris" in first.data.lower()
    second = await first.action("second", body="What about Spain?")
    status = await second.status()
    assert status.state == "idle"
    assert status.available_actions == []
    assert "madrid" in second.data.lower()

    with pytest.raises(AgentError) as e:
        await second.action("first", body="What is the capital of France?")
    assert e.value.status_code == 409


async def test_states_bad_initial_program():
    process = await Agent.get("states").create_process()
    with pytest.raises(AgentError) as e:
        await process.action("second", body="What is the capital of France?")
    assert e.value.status_code == 409


async def test_refs():
    process = await Agent.get("refs").create_process()
    resp = await process.action(
        "converse", body="Start a conversation with system_prompt and what its favorite country is."
    )
    assert "france" in resp.data.lower()


async def test_with_tools():
    process = await Agent.get("with_tools").create_process()
    resp = await process.action("converse", body="What is the meaning of life?")
    assert "42" in resp.data.lower()


async def test_optional_file_with_no_file():
    process = await Agent.get("optional_file").create_process()
    resp = await process.action("converse", data=dict(body="What is the capital of France?"))
    assert "paris" in resp.data.lower()


async def test_optional_file_with_file(dog):
    process = await Agent.get("optional_file").create_process()
    resp = await process.action(
        "converse",
        data=dict(body="How many legs does the animal have?"),
        files=dict(file=dog),
    )
    assert "four" in resp.data.lower()


async def test_optional_file_no_body_with_no_file():
    process = await Agent.get("optional_file_no_body").create_process()
    resp = await process.action("converse")
    assert resp.data  # no error, llm will complain about lack of file but that is irrelevant


async def test_optional_file_no_body_with_file(dog):
    process = await Agent.get("optional_file_no_body").create_process()
    resp = await process.action("converse", files=dict(file=dog))
    assert "four" in resp.data.lower()


async def test_single_file_with_no_file():
    with pytest.raises(AgentError) as e:
        process = await Agent.get("single_file").create_process()
        await process.action("converse", body="What is the capital of France?")
    assert e.value.status_code == 422


async def test_single_file_with_file(dog):
    process = await Agent.get("single_file").create_process()
    resp = await process.action(
        "converse",
        data=dict(body="How many legs does the animal have?"),
        files=dict(file=dog),
    )
    assert "four" in resp.data.lower()


async def test_single_file_no_body_with_no_file():
    with pytest.raises(AgentError) as e:
        process = await Agent.get("single_file_no_body").create_process()
        await process.action("converse", None)
    assert e.value.status_code == 422


async def test_single_file_no_body_with_file(dog):
    process = await Agent.get("single_file_no_body").create_process()
    resp = await process.action("converse", files=dict(file=dog))
    assert "four" in resp.data.lower()


async def test_multiple_files(cat, dog):
    process = await Agent.get("multiple_files").create_process()
    resp = await process.action(
        "converse", data=dict(body="what do these images have in common?"), files=[("file", dog), ("file", cat)]
    )
    assert "animals" in resp.data.lower()


async def test_multiple_files_no_body(cat, dog):
    process = await Agent.get("multiple_files_no_body").create_process()
    resp = await process.action("converse", files=[("file", dog), ("file", cat)])
    assert "animals" in resp.data.lower()


async def test_dynamic_client_args():
    with pytest.raises(AgentError) as e:
        await Agent.get("dynamic_client_args").run_program("converse", body="What is the capital of France?")
    assert e.value.status_code == 502
