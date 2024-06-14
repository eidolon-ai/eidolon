from typing import List, Optional, Any, cast

import jsonref
from pydantic import BaseModel, Field

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.builtins.logic_units.api_helper import build_call, get_content
from eidolon_ai_sdk.builtins.logic_units.openapi_helper import build_actions, Action, Operation
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class APIAgentSpec(BaseModel):
    title: str
    root_call_url: str
    open_api_location: str
    operations_to_expose: List[Operation]  # map of tool name to openapi path
    key_env_var: Optional[str] = None
    key_query_param: Optional[str] = None
    put_key_as_bearer_token: bool = Field(default=False)


class APIAgent(Specable[APIAgentSpec]):
    def __init__(self, **kwargs):
        Specable.__init__(self, **kwargs)
        self.open_api_schema = None

    async def start(self):
        await self._build_actions()

    async def get_schema(self) -> dict:
        if not self.open_api_schema:
            try:
                json_ = await get_content(self.spec.open_api_location)
                self.open_api_schema = jsonref.replace_refs(json_)
            except Exception as e:
                logger.error(f"Error fetching schema from {self.spec.open_api_location}: {e}")
                return {}

        return self.open_api_schema

    async def _build_actions(self):
        # first fetch the openapi schema located at self.spec.open_api_location
        schema = await self.get_schema()

        operations_to_expose = self.spec.operations_to_expose
        title = self.spec.title
        actions = build_actions(operations_to_expose, schema, title,
                                build_call(self.spec.key_env_var, self.spec.key_query_param, self.spec.put_key_as_bearer_token, self.spec.root_call_url))
        for action in actions:
            self._add_action(action)

    def _add_action(self, action: Action):
        wrapped_schema = dict(type="object", properties=dict(body=action.action_schema), required=["body"])
        model = schema_to_model(wrapped_schema, "InputModel")
        extra = {
            "title": action.title,
            "sub_title": action.sub_title,
            "agent_call": True,
        }

        async def unwrap_body(_self, **kwargs):
            body = cast(BaseModel, kwargs.pop("body"))
            return await action.tool_call(_self, **body.model_dump())

        setattr(
            self,
            action.name,
            register_action(
                'initialized',
                name=action.name,
                input_model=lambda a, b: model,
                output_model=lambda a, b: Any,
                description=lambda a, b: action.description,
                **extra,
            )(unwrap_body),
        )
