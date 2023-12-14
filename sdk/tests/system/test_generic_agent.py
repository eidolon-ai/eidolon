import json

import pytest

from eidos.agent.generic_agent import GenericAgentSpec
from eidos.cpu.conversational_agent_cpu import ConversationalAgentCPUSpec
from eidos.system.resources_base import Resource, Metadata


@pytest.fixture(scope="module")
def generic_agent_root(llm):
    resource = Resource(
        apiVersion="eidolon/v1",
        kind="GenericAgent",
        metadata=Metadata(name="GenericAgent"),
        spec=GenericAgentSpec(
            cpu=dict(spec=ConversationalAgentCPUSpec(llm_unit=llm)),
            system_prompt="You are a machine which follows instructions and returns a summary of your actions.",
            user_prompt="{{instruction}}",
            input_schema=dict(instruction=dict(type="string")),
            description="An agent which can follow instructions and return a summary of its actions.",
        ),
    )
    return resource


@pytest.fixture
def generic_agent(generic_agent_root):
    return generic_agent_root.model_copy(deep=True)


class TestGenericAgent:
    @pytest.fixture(scope="class")
    def client(self, client_builder, generic_agent_root):
        with client_builder(generic_agent_root) as client:
            yield client

    def test_can_start(self, client):
        docs = client.get("/docs")
        assert docs.status_code == 200

    def test_llm_calls(self, client):
        post = client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! What is the capital of France?"),
        )
        post.raise_for_status()
        assert "paris" in post.json()["data"].lower()

    def test_continued_conversation(self, client):
        post = client.post(
            "/agents/GenericAgent/programs/question",
            json=dict(instruction="Hi! my name is Luke"),
        )
        post.raise_for_status()
        process_id = post.json()["process_id"]
        follow_up = client.post(
            f"/agents/GenericAgent/processes/{process_id}/actions/respond",
            json=dict(statement="Can you sing me Happy Birthday?"),
        )
        follow_up.raise_for_status()
        assert "Luke" in post.json()["data"]


def test_generic_agent_supports_object_output(client_builder, generic_agent, dog):
    generic_agent.spec.output_schema = {
        "type": "object",
        "properties": {"capital": {"type": "string"}, "population": {"type": "number"}},
    }
    with client_builder(generic_agent) as client:
        post = client.post(
            "/agents/GenericAgent/programs/question", json=dict(instruction="Tell me about france please")
        )
        post.raise_for_status()
        assert "paris" in post.json()["data"]["capital"].lower()


def test_generic_agent_supports_image(client_builder, generic_agent, dog):
    generic_agent.spec.files = "single"
    with client_builder(generic_agent) as client:
        post = client.post(
            "/agents/GenericAgent/programs/question",
            data=dict(body=json.dumps(dict(instruction="What is in this image?"))),
            files=dict(file=dog),
        )
        post.raise_for_status()
        assert "brown" in post.json()["data"].lower()


def test_generic_agent_supports_multiple_images(client_builder, generic_agent, cat, dog):
    generic_agent.spec.files = "multiple"
    with client_builder(generic_agent) as client:
        post = client.post(
            "/agents/GenericAgent/programs/question",
            data=dict(body=json.dumps(dict(instruction="what do these images have in common?"))),
            files=[("file", dog), ("file", cat)],
        )
        post.raise_for_status()
        assert "animals" in post.json()["data"].lower()

        # followup question should still have access to the image
        process_id = post.json()["process_id"]
        follow_up = client.post(
            f"/agents/GenericAgent/processes/{process_id}/actions/respond",
            json=dict(statement="What is different between them?"),
        )
        follow_up.raise_for_status()
        assert "cat" in follow_up.json()["data"].lower()
