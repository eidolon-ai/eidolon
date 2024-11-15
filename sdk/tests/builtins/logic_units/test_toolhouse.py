import pytest
from eidolon_ai_sdk.builtins.logic_units.toolhouse_logic_unit import Toolhouse
from eidolon_ai_sdk.system.resources.resources_base import Metadata, Resource
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


## Building the tools and seeing if they show up as expected
async def test_tool_registration():
    tools = await Toolhouse().build_tools(None)
    assert len(tools)==3

    tool_names = [t.name for t in tools]
    assert tool_names==['code_interpreter', 'exa_web_search', 'scraper']



# Check if the tools work and are useable
async def test_build_tools():
    process = await client.Agent.get("toolhouse_agent").create_process()
    resp = await process.action("converse", body="Use the web search tool to check the capital of France. Respond 'correct' if the web tool returns 'Paris' and 'incorrect' otherwise.") 
    assert "correct" in resp.data.lower()





    


