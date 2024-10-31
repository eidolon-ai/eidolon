import os
from typing import Optional
from urllib.parse import urljoin
from toolhouse import Toolhouse as TH

from httpx import AsyncClient
from pydantic import BaseModel, Field

from eidolon_ai_sdk.apu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.system.reference_model import Specable
from sdk.eidolon_ai_sdk.system.tool_builder import ToolUnit

class Toolhouse(ToolUnit):
    """A configurable tool backed by Toolhouse.ai that can be added to Eidolon Agents"""
    ## At a high level, here's what we need:
    ## 2. Toolhouse API_KEY
    ## 3. Toolhouse bundle 
    ## 4. Function argument to be passed into toolhouse call
    api_key: str = Field(default_factory=lambda:os.environ['TOOLHOUSE_API_KEY'])
    bundle: str = "default"
    base_url: Optional[str] = None



@Toolhouse.dynamic_contract
def tool_build(spec: Toolhouse):
    th = TH(api_key=spec.api_key, provider="openai")
    if spec.base_url:
        th.set_base_url(spec.base_url)

    tools = th.get_tools()
    breakpoint()

    ## Loop through tools (prob array of tools) Register it on toolhouse class @Toolhouse.tool (name, desc, json), function that i register, is supposed to run the tool w/ proper arguments 
    ## Get pytest running and debugger 

   


    



