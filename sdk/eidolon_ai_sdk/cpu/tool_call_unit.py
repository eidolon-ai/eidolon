import json
from typing import List

from pydantic import BaseModel

from eidolon_ai_client.events import ToolCall
from eidolon_ai_sdk.cpu.llm_message import UserMessage, UserMessageText
from eidolon_ai_sdk.cpu.llm_unit import LLMCallFunction
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Specable


class ToolCallResponse(BaseModel):
    tools: List[ToolCall]


class ToolCallUnitSpec(BaseModel):
    tool_message_prompt: str = f"""You must follow these instructions:
Always select one or more of the above tools based on the user query
If a tool is found, you must respond in the JSON format matching the following schema:
{{
   "tools": [
   {{
        "tool_call_id": "<the id of the selected tool>",
        "name": "<name of the selected tool>",
        "arguments": <arguments for the selected tool, matching the tool's parameter JSON schema
   }}
   ]
}}
If there are multiple tools required, make sure a list of tools are returned in a JSON array.
If there is no tool that match the user request, you will respond with empty json.
Do not add any additional Notes or Explanations"""


class ToolCallUnit(ProcessingUnit, Specable[ToolCallUnitSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)

    def add_tools(self, message: UserMessage, tools: List[LLMCallFunction]):
        tool_schema = []
        for tool in tools:
            tool_schema.append(
                json.dumps({
                    "tool_call_id": tool.name,
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                })
            )

        prompt = "You have access to the following tools:\n" + "\n".join(tool_schema) + "\n" + self.spec.tool_message_prompt
        message.content.insert(0, UserMessageText(text = prompt))
