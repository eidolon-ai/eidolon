import pytest

from eidolon_ai_client.client import Agent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.builtins.logic_units.vectara import VectaraSearch, VectaraSearchSpec
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata
from eidolon_ai_sdk.util.class_utils import fqn


@pytest.fixture()
def vectara():
    return VectaraSearch(VectaraSearchSpec(corpus_key="black-holes-sample-data"))


@pytest.mark.vcr
async def test_query(vectara: VectaraSearch):
    resp = await vectara.query("what is a black hole?")
    assert "search_results" in resp
    assert len(resp["search_results"]) == 10
    assert {'blob': 'Black hole - Wikipedia'} == resp["documents"]


@pytest.mark.vcr
async def test_read_document(vectara: VectaraSearch):
    doc = await vectara.read_document("blob")
    to_check = doc['sections'][5]
    assert to_check.pop('content')[:40] == "On 11 February 2016, the LIGO Scientific"
    assert to_check == {'title': 'Observation', 'title_level': 4}


@pytest.fixture(scope="module")
async def server(run_app):
    async with run_app(
            Resource(
                apiVersion="eidolon/v1",
                kind="Agent",
                metadata=Metadata(name="vectara_agent"),
                spec=dict(
                    implementation="SimpleAgent",
                    apu=dict(
                        logic_units=[
                            dict(
                                implementation=fqn(VectaraSearch),
                                corpus_key="black-holes-sample-data"
                            ),
                        ]
                    )
                )
            ),
            Resource(
                apiVersion="eidolon/v1",
                kind="Agent",
                metadata=Metadata(name="vectara_agent_with_doc_read"),
                spec=dict(
                    implementation="SimpleAgent",
                    apu=dict(
                        logic_units=[
                            dict(
                                implementation=fqn(VectaraSearch),
                                corpus_key="black-holes-sample-data",
                                read_document_enabled=True
                            ),
                        ]
                    )
                )
            )
    ) as ra:
        yield ra


async def test_base_vectara_agent(server):
    process = await Agent.get("vectara_agent").create_process()
    response = await process.action("converse", body="what is a black hole?")
    assert response.state == "idle"


async def test_base_vectara_agent_with_read_doc(server):
    process = await Agent.get("vectara_agent_with_doc_read").create_process()
    response = await process.action("converse", body="what is a black hole? and quote an entire page from the document this information comes from")
    assert response.state == "idle"
