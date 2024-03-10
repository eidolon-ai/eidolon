from __future__ import annotations

import logging
import typing
from abc import ABC
from dataclasses import dataclass
from pydantic import BaseModel, TypeAdapter
from typing import Dict, List, AsyncIterator, Coroutine

from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_unit import LLMCallFunction
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_ai_client.events import (
    SuccessEvent,
    ObjectOutputEvent,
    ErrorEvent,
    BaseStreamEvent,
    StringOutputEvent,
    ToolCall,
)
from eidolon_ai_sdk.system.fn_handler import register_handler, FnHandler, get_handlers
from eidolon_ai_client.util.logger import logger


@dataclass
class LLMToolWrapper:
    logic_unit: LogicUnit
    llm_message: LLMCallFunction
    eidolon_handler: FnHandler
    input_model: typing.Type[BaseModel]

    async def execute(self, tool_call: ToolCall) -> AsyncIterator[BaseStreamEvent]:
        logger.info("calling tool " + self.eidolon_handler.name)
        logger.debug("args: " + str(tool_call.arguments) + " | fn: " + str(self.eidolon_handler.fn))
        try:
            # if this is a sync tool call just call execute, if it is not we need to store the state of the conversation and call in memory
            input_model = self.eidolon_handler.input_model_fn(self.logic_unit, self.eidolon_handler)
            result = self.eidolon_handler.fn(self.logic_unit, **dict(input_model.model_validate(tool_call.arguments)))
            if isinstance(result, Coroutine):
                result = await result

            if isinstance(result, typing.AsyncIterable):
                async for event in result:
                    yield event
            else:
                ret_type = self.eidolon_handler.output_model_fn(self.logic_unit, self.eidolon_handler)
                model = TypeAdapter(ret_type)
                result = model.dump_python(result)
                if isinstance(result, str):
                    yield StringOutputEvent(content=result)
                else:
                    yield ObjectOutputEvent(content=result)
                yield SuccessEvent()
        except Exception as e:
            logging.exception("error calling tool " + self.eidolon_handler.name)
            yield ErrorEvent(reason=str(e))

    @classmethod
    async def from_logic_units(
        cls, call_context: CallContext, logic_units: List[LogicUnit]
    ) -> Dict[str, LLMToolWrapper]:
        acc = {}
        for logic_unit in logic_units:
            for handler in await logic_unit.build_tools(call_context):
                new_name = logic_unit.__class__.__name__ + "_" + handler.name
                i = 0
                while new_name in acc:
                    new_name = logic_unit.__class__.__name__ + "_" + handler.name + "_" + str(i)
                    i += 1
                input_model = handler.input_model_fn(logic_unit, handler)
                acc[new_name] = LLMToolWrapper(
                    logic_unit=logic_unit,
                    llm_message=LLMCallFunction(
                        name=new_name,
                        description=handler.description(logic_unit, handler),
                        parameters=input_model.model_json_schema(),
                    ),
                    eidolon_handler=handler,
                    input_model=input_model,
                )
        return acc


def llm_function(
    name: str = None,
    description: typing.Optional[typing.Callable[[object, FnHandler], str]] = None,
    input_model: typing.Optional[typing.Callable[[object, FnHandler], BaseModel]] = None,
    output_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Any]] = None,
):
    return register_handler(name=name, description=description, input_model=input_model, output_model=output_model)


class LogicUnit(ProcessingUnit, ABC):
    async def build_tools(self, call_context: CallContext) -> List[FnHandler]:
        handlers = get_handlers(self)
        for handler in handlers:
            handler.extra["title"] = self.__class__.__name__
            handler.extra["sub_title"] = handler.fn.__name__
            handler.extra["agent_call"] = False

            return handlers
