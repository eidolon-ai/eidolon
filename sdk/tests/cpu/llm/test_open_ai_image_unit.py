from contextlib import asynccontextmanager

import pytest

from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm.open_ai_image_unit import OpenAIImageUnit
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture(scope="module")
def open_ai_image_unit():
    @asynccontextmanager
    async def cm() -> OpenAIImageUnit:
        ref = Reference(
            implementation=fqn(OpenAIImageUnit),
        )
        memory: OpenAIImageUnit = ref.instantiate(processing_unit_locator=None)
        yield memory

    return cm


def r(name, **kwargs):
    spec = dict(implementation=SimpleAgent.__name__, **kwargs, cpu=dict(implementation="APU", audio_unit="OpenAiSpeech"))
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


async def test_image_to_text(server, open_ai_image_unit, test_dir):
    async with open_ai_image_unit() as iu:
        docs_loc = test_dir / "cpu" / "llm" / "files"
        with open(docs_loc / "logo.png", "rb") as f:
            result = await iu._image_to_text("What is in the image?", f.read())
            assert "logo" in result


async def test_text_to_image(server, open_ai_image_unit, test_dir):
    call_context = CallContext(process_id="test")
    async with open_ai_image_unit() as iu:
        result = await iu._text_to_image(call_context, "Generate an image of a whale", size=(256, 256))
        assert len(result) == 1
        assert result[0].metadata["mimetype"] == "image/webp"
        assert result[0].file_id is not None
