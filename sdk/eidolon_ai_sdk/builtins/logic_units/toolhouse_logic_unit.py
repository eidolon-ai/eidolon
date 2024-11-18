import json
import os
from typing import Optional
from toolhouse import Toolhouse as TH
from pydantic import Field
from eidolon_ai_sdk.system.tool_builder import ToolBuilder
from toolhouse.models.RunToolsRequest import RunToolsRequest


class Toolhouse(ToolBuilder):
    """
    A configurable tool backed by Toolhouse.ai that can be added to Eidolon Agents.
    Toolhouse is the complete cloud infrastructure to equip LLMs with actions and knowledge.
    """
    api_key: str = Field(default_factory=lambda:os.environ['TOOLHOUSE_API_KEY'], description="Toolhouse API_KEY to connect toolhouse.")
    bundle: str = Field(default="default", description="groups of tools you want to pass to the LLM based on specific contextual need of each LLM call or agent.")
    base_url: Optional[str] = None


## Building Tool
@Toolhouse.dynamic_contract
def tool_build(spec: Toolhouse):
    th = TH(api_key=spec.api_key, provider="openai")
    if spec.base_url:
        th.set_base_url(spec.base_url)

    tools = th.get_tools(bundle=th.bundle)

    ## Running Tool
    for tool in tools:

        @Toolhouse.tool(
            description=tool["function"]["description"],
            name=tool["function"]["name"],
            parameters=tool["function"]["parameters"],
            partials=dict(tool=tool),
        )
        async def tool_register(tool, **kwargs):
            toolcall_args = {k: v for k, v in kwargs.items() if k != "spec"}
            run_tool_request = RunToolsRequest(
                dict(
                    type="function",
                    function=dict(name=tool["function"]["name"], arguments=json.dumps(toolcall_args)),
                    id="foo",
                ),
                th.provider,
                th.metadata,
                th.bundle,
            )
            run_response = th.tools.run_tools(run_tool_request)
            return run_response.content["content"]
