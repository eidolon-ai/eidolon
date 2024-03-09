from eidolon_ai_sdk.builtins.logic_units.web_search import WebSearchConfig, Search, Browser


async def test_go_to_url():
    browser = Browser(processing_unit_locator=None, spec=WebSearchConfig())
    found = await browser.go_to_url("https://httpbin.org/get")
    assert '"url": "https://httpbin.org/get"' in found


async def test_search():
    search = Search(processing_unit_locator=None, spec=WebSearchConfig())
    found = await search.search("test")
    assert len(found) == 10
    assert "test" in found[0].description
