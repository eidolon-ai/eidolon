from typing import List, Optional, Any

import jsonref
from pydantic import BaseModel, Field

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.logic_unit import LogicUnit
from eidolon_ai_sdk.builtins.logic_units.api_helper import get_content, build_call
from eidolon_ai_sdk.builtins.logic_units.openapi_helper import Operation, build_actions, Action
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class ApiLogicUnitSpec(BaseModel):
    title: str
    root_call_url: str
    open_api_location: str
    operations_to_expose: List[Operation]  # map of tool name to openapi path
    key_env_var: str
    key_query_param: Optional[str]
    put_key_as_bearer_token: bool = Field(default=False)


class ApiLogicUnit(LogicUnit, Specable[ApiLogicUnitSpec]):
    def __init__(self, **kwargs):
        LogicUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)
        self.open_api_schema = None

    async def get_schema(self) -> dict:
        if not self.open_api_schema:
            try:
                json_ = await get_content(self.spec.open_api_location)
                self.open_api_schema = jsonref.replace_refs(json_)
            except Exception as e:
                logger.error(f"Error fetching schema from {self.spec.open_api_location}: {e}")
                return {}

        return self.open_api_schema

    async def build_tools(self, call_context: CallContext) -> List[FnHandler]:
        # first fetch the openapi schema located at self.spec.open_api_location
        schema = await self.get_schema()

        tools = []
        operations_to_expose = self.spec.operations_to_expose
        title = self.spec.title
        actions = build_actions(operations_to_expose, schema, title,
                                build_call(self.spec.key_env_var, self.spec.key_query_param, self.spec.put_key_as_bearer_token, self.spec.root_call_url))
        for action in actions:
            tools.append(self._build_tool_def(action))

        return tools

    def _build_tool_def(self, action: Action):
        model = schema_to_model(action.action_schema, "InputModel")
        return FnHandler(
            name=action.name,
            description=lambda a, b: action.description,
            input_model_fn=lambda a, b: model,
            output_model_fn=lambda a, b: Any,
            fn=action.tool_call,
            extra={
                "title": action.title,
                "sub_title": action.sub_title,
                "agent_call": True,
            },
        )
