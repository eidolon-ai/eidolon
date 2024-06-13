from typing import List, Optional, Tuple, Any, Dict, Callable

from aiostream.stream.create import AsyncCallable
from pydantic import BaseModel, Field

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.util.filter_json import filter_and_reconstruct_json
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class Operation(BaseModel):
    name: str
    description: Optional[str]
    path: str
    method: str
    result_filters: Optional[List[str]]

    def matches(self, path: str) -> bool:
        return self.path == path


class Action(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    title: str
    sub_title: str
    name: str
    schema: dict
    description: str
    tool_call: callable


def build_actions(operations_to_expose: List[Operation], schema: dict, title: str,
                  call_fn: Callable[[str, str, List[Tuple[str, Any]], Dict[str, Any], Dict[str, Any]], Dict[str, Any]]):
    actions = []
    for op_path, op in schema["paths"].items():
        for operation in operations_to_expose:
            if operation.matches(op_path):
                for method_name, method in op.items():
                    if method_name == operation.method:
                        name = operation.name
                        required = []
                        params = {}
                        methodParams = None
                        if "parameters" in method:
                            methodParams = method["parameters"]
                            for param in method["parameters"]:
                                if param["in"] == "query":
                                    params[param["name"]] = param["schema"]
                                    if param["required"]:
                                        required.append(param["name"])
                                elif param["in"] == "path":
                                    params[param["name"]] = param["schema"]
                                    required.append(param["name"])
                                elif param["in"] == "header":
                                    params[param["name"]] = param["schema"]
                                    required.append(param["name"])
                                else:
                                    logger.error(f"Unsupported parameter location {param['in']}")

                        print(">>>>", method)
                        if "requestBody" in method:
                            params["__body__"] = _body_model(method, name + "_Body").model_json_schema()
                            print(">>>>", params["__body__"])
                            required.append("__body__")
                        description = operation.description or _description(method, name)
                        actions.append(Action(
                            title=title,
                            sub_title=method.get("summary", name),
                            name=name,
                            schema=dict(type="object", properties=params, required=required),
                            description=description,
                            tool_call=_call_endpoint(operation.path, operation.result_filters, method_name, methodParams, call_fn)
                        ))
    return actions


def _description(endpoint_schema, name):
    description = endpoint_schema.get("description", "")
    if not description:
        logger.warning(f"Agent program at {name} does not have a description. LLM may not use it properly")
    return description


def _body_model(schema, endpoint_schema, name):
    body = endpoint_schema.get("requestBody")
    description = body.get("description", "")
    required = body.get("required", False)
    content = body["content"]

    if "application/json" in content:
        json_schema = content["application/json"]["schema"]
        if "$ref" in json_schema:
            json_schema = findRef(json_schema["$ref"], schema)
        return dict(type="object", properties=dict(body=dict(type="string")), required=required, description=description)
    elif "text/plain" in content:
        return dict(type="object", properties=dict(body=dict(type="string")))
    else:
        raise ValueError(f"Agent action at {name} does not support text/plain or application/json")


def _convert_runtime_value(query_params: List[Tuple[str, Any]], param: dict, value: Any):
    if isinstance(value, list):
        if "explode" in param and param["explode"]:
            for v in value:
                query_params.append((param["name"], v))
        else:
            query_params.append((param["name"], ",".join(value)))
    elif isinstance(value, dict):
        if param["explode"]:
            for k, v in value.items():
                query_params.append((k, v))
        else:
            values = []
            for k, v in value.items():
                values.append(k)
                values.append(v)
            query_params.append((param["name"], ",".join(values)))
    else:
        query_params.append((param["name"], str(value)))


def _call_endpoint(path: str, result_filters: Optional[List[str]], method: str, _method_params,
                   call_fn: Callable[[str, str, List[Tuple[str, Any]], Dict[str, Any], Dict[str, Any]], Dict[str, Any]]):
    method_params = _method_params.copy() if _method_params else None
    result_filters = result_filters.copy() if result_filters else None

    async def _fn(_self, **kwargs):
        path_to_call = path
        query_params: List[Tuple[str, Any]] = []

        headers = dict()
        if method_params:
            for param in method_params:
                if param["in"] == "query":
                    if param["name"] in kwargs and kwargs[param["name"]] is not None:
                        _convert_runtime_value(query_params, param, kwargs[param["name"]])
                elif param["in"] == "path":
                    path_to_call = path_to_call.replace(f"{{{param['name']}}}", str(kwargs[param["name"]]))
                elif param["in"] == "header":
                    headers[param["name"]] = str(kwargs[param["name"]])
                else:
                    logger.error(f"Unsupported parameter location {param['in']}")
        body = kwargs.pop("__body__", {})
        print(f"Calling {path_to_call} with {query_params} and {headers} and {body}")

        retValue = call_fn(path_to_call, method, query_params, headers, body)

        if result_filters:
            retValue = filter_and_reconstruct_json(retValue, result_filters)

        return retValue

    return _fn
