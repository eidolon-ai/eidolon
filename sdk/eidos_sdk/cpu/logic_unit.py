from __future__ import annotations

import logging
import typing
from abc import ABC
from dataclasses import dataclass
from pydantic import BaseModel, TypeAdapter
from typing import Dict, Any, List

from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.cpu.llm_message import LLMMessage, ToolResponseMessage
from eidos_sdk.cpu.llm_unit import LLMCallFunction
from eidos_sdk.cpu.processing_unit import ProcessingUnit
from eidos_sdk.system.eidos_handler import register_handler, EidosHandler, get_handlers
from eidos_sdk.util.logger import logger


@dataclass
class LLMToolWrapper:
    logic_unit: LogicUnit
    llm_message: LLMCallFunction
    eidos_handler: EidosHandler
    input_model: typing.Type[BaseModel]

    # todo we should support any type response, not just dict
    async def execute(self, call_context: CallContext, args: Dict[str, Any]) -> Any:
        logger.info("calling tool " + self.eidos_handler.name)
        logger.debug("args: " + str(args) + " | fn: " + str(self.eidos_handler.fn))
        try:
            # if this is a sync tool call just call execute, if it is not we need to store the state of the conversation and call in memory
            if self.logic_unit.is_sync():
                input_model = self.eidos_handler.input_model_fn(self.logic_unit, self.eidos_handler)

                result = await self.eidos_handler.fn(self.logic_unit, **dict(input_model.model_validate(args)))
                ret_type = self.eidos_handler.output_model_fn(self.logic_unit, self.eidos_handler)
                model = TypeAdapter(ret_type)
                result = model.dump_python(result)
                return result
            else:
                # todo -- store the conversation and args in memory
                raise NotImplementedError("Async tools are not yet supported.")
        except Exception as e:
            logging.exception("error calling tool " + self.eidos_handler.name)
            return dict(error=str(e))

    @classmethod
    async def from_logic_units(cls, logic_units: List[LogicUnit], conversation: List[LLMMessage]) -> Dict[str, LLMToolWrapper]:
        acc = {}
        for logic_unit in logic_units:
            # pull out the ToolResponseMessage from the conversation on for this logic unit
            response_messages = [m for m in conversation if isinstance(m, ToolResponseMessage) and m.logic_unit_name == logic_unit.__class__.__name__]

            for handler in await logic_unit.build_tools(response_messages):
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
                    eidos_handler=handler,
                    input_model=input_model,
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
    async def build_tools(self, conversation: List[ToolResponseMessage]) -> List[EidosHandler]:
        return get_handlers(self)

    def is_sync(self):
        return True
