import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata


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


async def test_text_file_include():
    process = await Agent.get("simple").create_process()
    file_handle = await process.upload_file("This is a sample text file".encode("utf-8"))
    resp = await process.action(
        "converse", body=dict(body="What is in the attached file?", attached_files=[file_handle])
    )
    assert "This is a sample text file" in resp.data


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
