import pytest
from eidolon_ai_sdk.builtins.logic_units.toolhouse_logic_unit import Toolhouse, tool_build
from eidolon_ai_sdk.system.resources.resources_base import Metadata, Resource
from eidolon_ai_sdk.system.tool_builder import ToolBuilder
from eidolon_ai_sdk.util.class_utils import fqn
from eidolon_ai_client import client


## Build Agent to do testing: 


@pytest.fixture(scope="module", autouse=True)
async def server(run_app):
    resource_toolhouse = Resource(
            apiVersion="eidolon/v1",
            kind="Agent",
            metadata=Metadata(
                name="toolhouse_agent"
            ), 
            spec=dict(
                implementation="SimpleAgent",
                apu=dict(logic_units=[dict(implementation=fqn(Toolhouse))])
            )
    )
    
    async with run_app(
        resource_toolhouse
         ) as ra:
        yield ra


## Building them
async def test_tool_registration():
    tools = await Toolhouse().build_tools(None)
    assert len(tools)==3

    tool_names = [t.name for t in tools]
    assert tool_names==['code_interpreter', 'exa_web_search', 'scraper']



# Check if they can use tools
async def test_build_tools():
    process = await client.Agent.get("toolhouse_agent").create_process()
    resp = await process.action("converse", body="Use the web search tool to check the price of NVIDIA Stock") ## Set up debugger lah to see if this thing actually works. 
    assert "148.73" in resp.data




#async def test_tool_run():
    #pass

    


