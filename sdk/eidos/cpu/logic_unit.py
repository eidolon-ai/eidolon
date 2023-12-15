from __future__ import annotations

import inspect
import logging
import typing
from abc import ABC
from typing import Dict, Any, Callable, List

from bson import ObjectId
from pydantic import BaseModel, create_model
from pydantic.dataclasses import dataclass
from pydantic.fields import FieldInfo

from eidos.cpu.call_context import CallContext
from eidos.cpu.llm_message import LLMMessage
from eidos.cpu.llm_unit import LLMCallFunction
from eidos.cpu.processing_unit import ProcessingUnit
from eidos.system.eidos_handler import register_handler, EidosHandler, get_handlers
from eidos.util.class_utils import get_function_details
from eidos.util.logger import logger
from eidos.util.schema_to_model import schema_to_model


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

    @classmethod
    async def from_logic_units(cls, logic_units: List[LogicUnit], conversation) -> Dict[str, ToolDefType]:
        acc = {}
        for logic_unit in logic_units:
            for handler in await logic_unit.build_tools(conversation):
                new_name = logic_unit.__class__.__name__ + "_" + handler.name
                i = 0
                while new_name in acc:
                    new_name = new_name + logic_unit.__class__.__name__ + "_" + handler.name + "_" + str(i)
                    i += 1
                acc[new_name] = ToolDefType(
                    _logic_unit=logic_unit,
                    fn=handler.fn,
                    name=new_name,
                    description=handler.description(logic_unit, handler),
                    parameters=handler.input_model_fn(logic_unit, handler).model_json_schema(),
                )
        return acc


def llm_function(
        name: str = None,
        description: typing.Optional[typing.Callable[[object, EidosHandler], str]] = None,
        input_model: typing.Optional[typing.Callable[[object, EidosHandler], BaseModel]] = None,
        output_model: typing.Optional[typing.Callable[[object, EidosHandler], typing.Any]] = None,
):
    return register_handler(name=name, description=description, input_model=input_model, output_model=output_model)


class LogicUnit(ProcessingUnit, ABC):
    async def build_tools(self, conversation: List[LLMMessage]) -> List[EidosHandler]:
        return get_handlers(self)

    def is_sync(self):
        return True

    # todo, response type here should not be limited to dict
    async def execute(
        self,
        call_context: CallContext,
        name,
        parameter_schema,
        fn: Callable,
        args: Dict[str, Any],
    ) -> Dict[str, Any]:
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
