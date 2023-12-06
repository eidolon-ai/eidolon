from __future__ import annotations

import inspect
import logging
import typing
from abc import ABC
from typing import Dict, Any, Callable, List

from bson import ObjectId
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage
from eidolon_sdk.cpu.llm_unit import LLMCallFunction
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.util.class_utils import get_function_details
from eidolon_sdk.util.logger import logger
from eidolon_sdk.util.schema_to_model import schema_to_model


class ToolDefType(LLMCallFunction):
    fn: Callable
    _logic_unit: LogicUnit

    def __init__(self, _logic_unit: LogicUnit, **data):
        super().__init__(**data)
        self._logic_unit = _logic_unit

    async def execute(self, call_context: CallContext, args: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("executing tool " + self.name)
        logger.debug("args: " + str(args) + " | fn: " + str(self.fn))
        return await self._logic_unit.execute(call_context, self.name, self.parameters, self.fn, args)


# todo, llm function should require annotations and error if they are not present
def llm_function(fn):
    sig = inspect.signature(fn).parameters
    hints = typing.get_type_hints(fn, include_extras=True)
    fields = {}
    for param, hint in filter(lambda tu: tu[0] != 'return', hints.items()):
        if hasattr(hint, '__metadata__') and isinstance(hint.__metadata__[0], FieldInfo):
            field: FieldInfo = hint.__metadata__[0]
            if sig[param].default is not inspect.Parameter.empty:
                field.default = sig[param].default
            else:
                field.default = None
            fields[param] = (hint.__origin__, field)
        else:
            # _empty default isn't being handled by create_model properly (still optional when it should be required)
            default = ... if getattr(sig[param].default, "__name__", None) == '_empty' else sig[param].default
            fields[param] = (hint, default)

    function_name, clazz = get_function_details(fn)
    logger.debug("creating model " + f'{clazz}_{function_name}InputModel' + " with fields " + str(fields))
    input_model = create_model(f'{clazz}_{function_name}InputModel', **fields)

    setattr(fn, 'llm_function', dict(
        name=function_name,
        description=fn.__doc__,
        input_model=input_model,
        fn=fn,
    ))
    return fn


class LogicUnit(ProcessingUnit, ABC):
    _base_tools: Dict[str, ToolDefType]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._base_tools = {}
        self._find_base_tools()

    def _find_base_tools(self):
        for name, llm_function_ in (
                (method_name, getattr(method, 'llm_function'))
                for method_name in dir(self) for method in [getattr(self, method_name)]
                if hasattr(method, 'llm_function')
        ):
            unique_name = name + "_" + str(ObjectId())
            fn = llm_function_['fn']
            logger.debug("registering tool " + unique_name + " with fn " + str(fn))
            schema = llm_function_['input_model'].model_json_schema()
            description_ = llm_function_['description']
            self._base_tools[unique_name] = ToolDefType(
                name=unique_name,
                description=description_,
                parameters=schema,
                fn=fn,
                _logic_unit=self
            )

    async def build_tools(self, conversation: List[LLMMessage]) -> Dict[str, ToolDefType]:
        return self._base_tools
        # return {k: v.model_copy(deep=True) for k, v in self._base_tools.items()}

    def is_sync(self):
        return True

    async def execute(self, call_context: CallContext, name, parameter_schema, fn: Callable, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # if this is a sync tool call just call execute, if it is not we need to store the state of the conversation and call in memory
            if self.is_sync():
                converted_input = schema_to_model(parameter_schema, name + "_input").model_validate(args)
                logging.getLogger("eidolon").info("calling tool " + name + " with args " + str(converted_input))
                result = await fn(self, **dict(converted_input))
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
        except Exception as e:
            logging.exception("error calling tool " + name)
            return dict(error=str(e))
