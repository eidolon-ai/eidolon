from eidolon_ai_sdk.builtins.logic_units.toolhouse_logic_unit import Toolhouse, tool_build


async def test_tool_registration():
    tools = await Toolhouse().build_tools(None)
    assert len(tools)==3

    tool_names = [t.name for t in tools]
    assert tool_names==['code_interpreter', 'exa_web_search', 'scraper']



