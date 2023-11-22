from __future__ import annotations

import inspect
import logging
import typing
from abc import ABC
from dataclasses import dataclass
from typing import Dict, Any, Callable, List

from bson import ObjectId
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

from eidolon_sdk.cpu.agent_bus import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage
from eidolon_sdk.cpu.llm_unit import LLMCallFunction
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.util.class_utils import get_function_details


# todo, this can be collapsed with MethodInfo, but surgery for now
@dataclass
class ToolDefType:
    logic_unit: LogicUnit
    method_info: MethodInfo
    llm_call_function: LLMCallFunction


# todo, llm function should require annotations and error if they are not present
def llm_function(fn):
    sig = inspect.signature(fn).parameters
    hints = typing.get_type_hints(fn, include_extras=True)
    fields = {}
    for param, hint in filter(lambda tu: tu[0] != 'return', hints.items()):
        if hasattr(hint, '__metadata__') and isinstance(hint.__metadata__[0], FieldInfo):
            field: FieldInfo = hint.__metadata__[0]
            field.default = sig[param].default
            fields[param] = (hint.__origin__, field)
        else:
            # _empty default isn't being handled by create_model properly (still optional when it should be required)
            default = ... if getattr(sig[param].default, "__name__", None) == '_empty' else sig[param].default
            fields[param] = (hint, default)

    function_name, clazz = get_function_details(fn)
    input_model = create_model(f'{clazz}_{function_name}InputModel', **fields)

    setattr(fn, 'llm_function', MethodInfo(
        name=function_name,
        description=fn.__doc__,
        input_model=input_model,
        fn=fn
    ))
    return fn


class MethodInfo(BaseModel):
    name: str
    description: str
    input_model: typing.Type[BaseModel]
    fn: Callable


class LogicUnit(ProcessingUnit, ABC):
    _tool_functions: Dict[str, MethodInfo]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tool_functions = self._find_base_tools()

    def _find_base_tools(self):
        return {
            method_name: getattr(method, 'llm_function')
            for method_name in dir(self)
            for method in [getattr(self, method_name)]
            if hasattr(method, 'llm_function')
        }

    async def build_tools(self, conversation: List[LLMMessage]) -> Dict[str, ToolDefType]:
        tools = {}
        for fn_name, t in self._tool_functions.items():
            unique_method_name = fn_name + "_" + str(ObjectId())
            tools[unique_method_name] = ToolDefType(self, t, LLMCallFunction(
                name=unique_method_name,
                description=t.description,
                parameters=t.input_model.model_json_schema()
            ))
        return tools

    def is_sync(self):
        return True

    async def _execute(self, call_context: CallContext, method_info: MethodInfo, args: Dict[str, Any]) -> Dict[str, Any]:
        # if this is a sync tool call just call execute, if it is not we need to store the state of the conversation and call in memory
        if self.is_sync():
            converted_input = method_info.input_model.model_validate(args)
            logging.info("calling tool " + method_info.name + " with args " + str(converted_input))
            result = await method_info.fn(self, **dict(converted_input))
            # if result is a base model, call model_dump on it. If it is a string wrap it in an object with a "text" key
            if isinstance(result, BaseModel):
                result = result.model_dump()
            elif isinstance(result, str):
                result = {"text": result}
            elif result is None:
                result = {}
            return result
        else:
            # todo -- store the conversation and args in memory
            raise NotImplementedError("Async tools are not yet supported.")
