import re

import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_client.events import FileHandle
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata


def r(name, **kwargs):
    spec = dict(
        implementation=SimpleAgent.__name__,
        **kwargs,
        apu=dict(implementation="APU", audio_unit="OpenAiSpeech", image_unit="OpenAIImageUnit"),
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


async def test_text_file_include():
    process = await Agent.get("simple").create_process()
    file_handle = await process.upload_file("This is a sample text file".encode("utf-8"))
    resp = await process.action(
        "converse", body=dict(body="What is in the attached file?", attached_files=[file_handle])
    )
    assert "This is a sample text file" in resp.data


async def test_text_file_include_and_follow_up_messages():
    process = await Agent.get("simple").create_process()
    file_handle = await process.upload_file("This is a sample text file".encode("utf-8"))
    await process.action("converse", body=dict(body="What is in the attached file?", attached_files=[file_handle]))
    resp = await process.action("converse", body=dict(body="how many words are in the file?"))
    assert "6" in resp.data


async def test_pdf_file_include(test_dir):
    docs_loc = test_dir / "cpu" / "apu_docs"
    process = await Agent.get("simple").create_process()
    with open(docs_loc / "Brand New Love Affair - Part I & II.pdf", "rb") as f:
        file_handle = await process.upload_file(f.read())
    file_handle2 = await process.set_metadata(
        file_handle.file_id, dict(mime_type="application/pdf", filename="Brand New Love Affair - Part I & II.pdf")
    )
    assert file_handle2.file_id == file_handle.file_id
    resp = await process.action(
        "converse", body=dict(body="What is in the attached file?", attached_files=[file_handle])
    )
    assert "Chicago" in resp.data


async def test_image_file_include(test_dir):
    process = await Agent.get("simple").create_process()
    docs_loc = test_dir / "cpu" / "llm" / "files"
    with open(docs_loc / "logo.png", "rb") as f:
        file_handle = await process.upload_file(f.read())
        result = await process.action("converse", body=dict(body="What is in the image?", attached_files=[file_handle]))
        print(result)
        assert "logo" in result.data


async def test_produce_image_from_text(test_dir):
    process = await Agent.get("simple").create_process()
    await process.action(
        "converse",
        body=dict(
            body="Create an image of a logo for a new startup called AugustData. The logo should be simple and elegant."
        ),
    )


async def test_audio_file_include_and_produce(test_dir):
    process = await Agent.get("simple").create_process()
    result = await process.action(
        "converse", body=dict(body="Create an audio file of the text 'Hello world, how are you today?'")
    )
    pattern = r"(https?://[^/]+)/processes/([^/]+)/files/([^/\)\s]+)"
    match = re.search(pattern, result.data)
    assert match is not None
    machine_url, process_id, file_id = match.groups()
    assert machine_url == process.machine
    assert process_id == process.process_id
    file = await process.download_file(file_id)
    assert file is not None
    result = await process.action(
        "converse",
        body=dict(
            body="What is in the audio clip?",
            attached_files=[FileHandle(machineURL=machine_url, process_id=process_id, file_id=file_id)],
        ),
    )
    assert "Hello world, how are you today?" in result.data
