from contextlib import asynccontextmanager

import pytest

from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.cpu.llm.open_ai_image_unit import OpenAIImageUnit
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture(scope="module")
def open_ai_image_unit():
    @asynccontextmanager
    async def cm():
        ref = Reference(
            implementation=fqn(OpenAIImageUnit),
        )
        memory: OpenAIImageUnit = ref.instantiate()
        yield ref

    return cm


def r(name, **kwargs):
    spec = dict(
        implementation=SimpleAgent.__name__, **kwargs,
        cpu=dict(
            implementation="APU",
            audio_unit="OpenAiSpeech"
        )
    )
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=name),
        spec=spec,
    )


resources = [
    r("simple", actions=[dict(allow_file_upload=True)]),
]


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    async with run_app(*resources) as ra:
        yield ra


async def test_image_to_text(server, open_ai_image_unit):
    pass
