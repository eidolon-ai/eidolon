import certifi
import pytest
from eidos_sdk.builtins.logic_units.web_search import WebSearch, WebSearchConfig

@pytest.fixture
def websearch():
    return WebSearch(processing_unit_locator=None, spec=WebSearchConfig())


async def test_go_to_url(websearch):
    found = await websearch.go_to_url("https://httpbin.org/get")
    assert found


async def test_search(websearch):
    found = await websearch.search("test")
    assert len(found) == 10
    assert "test" in found[0].description
