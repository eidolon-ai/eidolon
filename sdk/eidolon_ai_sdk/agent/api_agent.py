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
    title: str = Field(description="Title of the API")
    root_call_url: str = Field(description="Root URL of the API to call")
    open_api_location: str = Field(description="Location of the OpenAPI schema")
    operations_to_expose: List[Operation] = Field(description="Operations to expose")
    key_env_var: Optional[str] = Field(description="Environment variable to use as the API key to send to the API. Only needed if the API has security needs.", default=None)
    key_query_param: Optional[str] = Field(description="The name of the query parameter to use to send the API key to the API. Only needed if the API has security and that is passed as a query param", default=None)
    key_header_param: Optional[str] = Field(description="The name of the header parameter to use to send the API key to the API. Only needed if the API has security and that is passed as a non-standard (Authorization Bearer) header", default=None)
    put_api_key_as_bearer_token: Optional[bool] = Field(description="Whether to put the API key as a bearer token in the Authorization header", default=False)


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
                                build_call(self.spec.key_env_var, self.spec.key_query_param, self.spec.key_header_param, self.spec.put_api_key_as_bearer_token, self.spec.root_call_url))
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
