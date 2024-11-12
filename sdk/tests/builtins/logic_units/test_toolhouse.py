from eidolon_ai_sdk.builtins.logic_units.toolhouse_logic_unit import Toolhouse, tool_build
from eidolon_ai_sdk.system.resources.resources_base import Metadata, Resource
from eidolon_ai_sdk.system.tool_builder import ToolBuilder

## Build Agent to do testing: 
def r(tool: ToolBuilder, agent_name: str = None):
    return Resource(
        apiVersion="eidolon/v1",
        kind="Agent",
        metadata=Metadata(name=agent_name or type(tool).__name__),
        spec=dict(
            implementation="SimpleAgent",
            apu=dict(logic_units=[dict(implementation=fqn(type(tool)), **tool.model_dump())])
        ),
    )



async def test_tool_registration():
    tools = await Toolhouse().build_tools(None)
    assert len(tools)==3

    tool_names = [t.name for t in tools]
    assert tool_names==['code_interpreter', 'exa_web_search', 'scraper']

async def test_tool_run():
    


