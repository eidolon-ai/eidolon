import os
from typing import List, Optional, Any
from urllib.parse import urljoin, quote_plus

import jsonref
from httpx import AsyncClient, Timeout
from jsonpath_ng import parse
from pydantic import BaseModel, Field

from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class Operation(BaseModel):
    name: str
    description: Optional[str]
    path: str
    method: str
    result_filters: List[str]


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

    async def build_tools(self, call_context: CallContext) -> List[FnHandler]:
        # first fetch the openapi schema located at self.spec.open_api_location
        schema = await self.get_schema()

        tools = []
        for operation in self.spec.operations_to_expose:
            op = schema["paths"][operation.path]
            if not op:
                logger.error(f"No path found for operation {operation.path}")
            else:
                for method_name, method in op.items():
                    if method_name == operation.method:
                        name = operation.name
                        required = []
                        params = {}
                        if "parameters" in method:
                            for param in method["parameters"]:
                                if param["in"] == "query":
                                    params[param["name"]] = param["schema"]
                                    if param["required"]:
                                        required.append(param["name"])
                        if "request_body" in method:
                            params["__body__"] = self._body_model(method, name + "_Body")
                            required.append("__body__")
                        description = operation.description or self._description(method, name)
                        tools.append(self._build_tool_def(
                            agent=self.spec.title,
                            operation=method["summary"] or name,
                            name=name,
                            schema=dict(type="object", properties=params, required=required),
                            description=description,
                            tool_call=self._call_endpoint(operation, method_name, method["parameters"])
                        ))
        return tools

    def _build_tool_def(self, agent, operation, name, schema, description, tool_call):
        model = schema_to_model(schema, "InputModel")
        return FnHandler(
            name=name,
            description=lambda a, b: description,
            input_model_fn=lambda a, b: model,
            output_model_fn=lambda a, b: Any,
            fn=tool_call,
            extra={
                "title": agent,
                "sub_title": operation,
                "agent_call": True,
            },
        )

    def _call_endpoint(self, _operation: Operation, method: str, _method_params):
        path = _operation.path
        api_key = os.environ.get(self.spec.key_env_var, None) if self.spec.key_env_var else None
        headers = {
            "Content-Type": "application/json"
        }
        if self.spec.put_key_as_bearer_token:
            headers["Authorization"] = f"Bearer {api_key}"
        method_params = _method_params.copy()
        result_filters = _operation.result_filters.copy() if _operation.result_filters else None
        async def _fn(_self, **kwargs):
            path_to_call = path
            query_params = {}
            if api_key and self.spec.key_query_param:
                query_params[self.spec.key_query_param] = api_key

            if method_params:
                for param in method_params:
                    if param["in"] == "query":
                        if param["name"] in kwargs and kwargs[param["name"]] is not None:
                            query_params[param["name"]] = kwargs[param["name"]]
                    elif param["in"] == "path":
                        path_to_call = path_to_call.replace(f"{{{param['name']}}}", kwargs[param["name"]])
                    else:
                        logger.error(f"Unsupported parameter location {param['in']}")

            if query_params and len(query_params) > 0:
                path_to_call += "?" + "&".join([f"{quote_plus(k)}={quote_plus(str(v))}" for k, v in query_params.items() if v])
            body = kwargs.pop("__body__", {})
            url = urljoin(self.spec.root_call_url, path_to_call)
            if "headers" in body:
                body["headers"].update(headers)
            else:
                body["headers"] = headers
            retValue = {}
            if method == "get":
                retValue = await self.get_content(url, **body)
            elif method == "post":
                retValue = await self.post_content(url, **body)
            else:
                logger.error(f"Unsupported method {method}")
            if result_filters:
                filteredValue = {}
                for result_filter in result_filters:
                    filter = parse(result_filter)
                    filteredValue.update({str(match.full_path): match.value for match in filter.find(retValue)})
                retValue = filteredValue

            return retValue

        return _fn

    @staticmethod
    def _body_model(endpoint_schema, name):
        body = endpoint_schema.get("requestBody")
        if not body:
            json_schema = dict(type="object", properties={})
            return schema_to_model(dict(type="object", properties=dict(body=json_schema)), "Input")
        elif "application/json" in body["content"]:
            json_schema = body["content"]["application/json"]["schema"]
            return schema_to_model(dict(type="object", properties=dict(body=json_schema)), "Input")
        elif "text/plain" in body["content"]:
            return schema_to_model(dict(type="object", properties=dict(body=dict(type="string"))), "Input")
        else:
            raise ValueError(f"Agent action at {name} does not support text/plain or application/json")

    @staticmethod
    def _description(endpoint_schema, name):
        description = endpoint_schema.get("description", "")
        if not description:
            logger.warning(f"Agent program at {name} does not have a description. LLM may not use it properly")
        return description
