import os
from typing import List, Optional, Any
from urllib.parse import urljoin, quote_plus

import jsonref
from httpx import AsyncClient, Timeout
from pydantic import BaseModel, Field

from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.builtins.logic_units.openapi_helper import build_actions, Action
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class Operation(BaseModel):
    name: str
    description: Optional[str]
    path: str
    method: str
    result_filters: List[str]


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

    async def get_content(self, url: str, **kwargs):
        params = {"url": url}
        async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
            response = await client.get(**params, **kwargs)
            await AgentError.check(response)
            return response.json()

    async def post_content(self, url: str, **kwargs):
        params = {"url": url}
        async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
            response = await client.post(**params, **kwargs)
            await AgentError.check(response)
            return response.json()

    async def get_schema(self) -> dict:
        if not self.open_api_schema:
            json_ = await self.get_content(self.spec.open_api_location)
            self.open_api_schema = jsonref.replace_refs(json_)

        return self.open_api_schema

    async def _build_actions(self):
        # first fetch the openapi schema located at self.spec.open_api_location
        schema = await self.get_schema()

        operations_to_expose = self.spec.operations_to_expose
        title = self.spec.title
        actions = build_actions(operations_to_expose, schema, title, self.do_call)
        for action in actions:
            self._add_action(action)

    def _add_action(self, action: Action):
        model = schema_to_model(action.schema, "InputModel")
        extra = {
            "title": action.title,
            "sub_title": action.sub_title,
            "agent_call": True,
        }

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
            )(action.tool_call),
        )

    def do_call(self, path_to_call, method, query_params, headers, body):
        path_to_call = path_to_call.lstrip('/')
        api_key = os.environ.get(self.spec.key_env_var, None) if self.spec.key_env_var else None
        headers = headers or {}
        headers["Content-Type"] = "application/json"
        if self.spec.put_key_as_bearer_token and api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        if api_key and self.spec.key_query_param:
            query_params.append((self.spec.key_query_param, api_key))

        if query_params and len(query_params) > 0:
            path_to_call += "?" + "&".join([f"{quote_plus(k)}={quote_plus(str(v))}" for k, v in query_params if v])

        if "headers" in body:
            body["headers"].update(headers)
        else:
            body["headers"] = headers

        url = urljoin(self.spec.root_call_url + "/", path_to_call)
        if method == "get":
            return self.get_content(url, **body)
        elif method == "post":
            return self.post_content(url, **body)
        else:
            logger.error(f"Unsupported method {method}")
            return {}
