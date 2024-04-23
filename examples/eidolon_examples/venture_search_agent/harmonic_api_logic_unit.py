import os
from contextlib import asynccontextmanager
from typing import List, Optional, Literal, Any, Dict
from urllib.parse import urljoin

# from aiohttp import ClientSession
from bs4 import BeautifulSoup
from httpx import AsyncClient, Timeout
from pydantic import BaseModel, Field, model_validator

from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.schema_to_model import schema_to_model
import jsonref


class ApiLogicUnitSpec(BaseModel):
    root_call_url: str
    open_api_location: str
    operations_to_expose: Dict[str, str] # map of tool name to openapi path
    key_env_var: str
    key_query_param: Optional[str]
    put_key_as_bearer_token: bool = Field(default=False)


class ApiLogicUnit(LogicUnit, Specable[ApiLogicUnitSpec]):
    def __init__(self, **kwargs):
        LogicUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)

    def _headers(self):
        return {
            "Content-Type": "application/json",
        }

    async def get_content(self, url: str, **kwargs):
        params = {"url": url, "headers": self._headers()}
        async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
            response = await client.get(**params, **kwargs)
            await AgentError.check(response)
            return response.json()

    async def post_content(self, url: str, **kwargs):
        params = {"url": url, "headers": self._headers()}
        async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
            response = await client.post(**params, **kwargs)
            await AgentError.check(response)
            return response.json()

    async def get_schema(self) -> dict:
        json_ = await self.get_content(self.spec.open_api_location)
        return jsonref.replace_refs(json_)

    async def build_tools(self, call_context: CallContext) -> List[FnHandler]:
        # first fetch the openapi schema located at self.spec.open_api_location
        schema = await self.get_schema()

        tools = []
        for operation in self.spec.operations_to_expose:
            op = schema["paths"][operation]
            if not op:
                logger.error(f"No path found for operation {operation}")
            else:
                for method_name, method in op:
                    name = method["operationId"]
                    required = []
                    params = {}
                    if "parameters" in method:
                        for param in method["parameters"]:
                            if param["in"] == "query":
                                model = schema_to_model(param["schema"], param["name"] + "_query")
                                params[param["name"]] = model
                                if param["required"]:
                                    required.append(param["name"])
                    if "request_body" in method:
                        params["__body__"] = self._body_model(method, name + "_Body")
                        required.append("__body__")
                    description = self._description(method, name)
                    tools.append(FnHandler(
                        name=name,
                        description=lambda a, b: description,
                        input_model_fn=lambda a, b: model,
                        output_model_fn=lambda a, b: Any,
                        fn=self._call_endpoint(operation, method_name),
                        extra={
                            "title": method["summary"] or name,
                            "sub_title": operation,
                            "agent_call": True,
                        },
                    ))
            return tools

    def _call_endpoint(self, path, method):
        async def _fn(_self, **kwargs):
            # todo -- need to convert params to query params
            # todo -- need to add security key
            
            url = urljoin(self.spec.root_call_url, path)
            if method == "get":
                return await self.get_content(url, **kwargs)
            elif method == "post":
                return await self.post_content(url, **kwargs)
            else:
                logger.error(f"Unsupported method {method}")
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
