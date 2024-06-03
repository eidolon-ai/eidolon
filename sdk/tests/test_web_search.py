import pytest

from eidolon_ai_sdk.builtins.logic_units.web_search import WebSearchConfig, Search, Browser, SearchSpec


@pytest.mark.vcr
async def test_go_to_url():
    browser = Browser(processing_unit_locator=None, spec=WebSearchConfig(cse_id="testcx", cse_token="testtoken"))
    found = await browser.go_to_url("https://httpbin.org/get")
    assert '"url": "https://httpbin.org/get"' in found


# note when recording the cse_id and cse_token need to be replaced with real values. They are placed in envar so cassette needs to be edited.
# if we ever need to touch this again we can manually manipulate the url with the cassette context manager
@pytest.mark.vcr
async def test_search():
    search = Search(processing_unit_locator=None, spec=SearchSpec(cse_id="testcx", cse_token="testtoken"))
    found = await search.search(search, "test")
    assert len(found) == 10
    assert "test" in found[0].description
