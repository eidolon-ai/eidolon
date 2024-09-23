import pytest

from eidolon_ai_sdk.builtins.logic_units.vectara import VectaraSearch, VectaraSearchSpec


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
