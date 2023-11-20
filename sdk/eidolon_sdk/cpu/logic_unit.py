from abc import ABC
from dataclasses import dataclass
from typing import List, Dict, Any, Callable

from pydantic import BaseModel, Field

from eidolon_sdk.cpu.agent_bus import BusEvent, CallContext
from eidolon_sdk.cpu.bus_messages import READ_PORT
from eidolon_sdk.cpu.llm_message import LLMMessage, ToolResponseMessage
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.reference_model import Specable


def llm_function(fn):
    return fn


@dataclass
class MethodInfo:
    name: str
    description: str
    input_model: BaseModel
    output_model: BaseModel
    fn: Callable


class LogicUnitConfig:
    le_read: READ_PORT = Field(description="A port that, when bound to an event, will read the LLM tool call from the bus.")
    lr_write: READ_PORT = Field(description="A port that, when bound to an event, will write the tool call response to the bus.")


class LogicUnit(ProcessingUnit, Specable[LogicUnitConfig], ABC):
    def __init__(self, spec: LogicUnitConfig = None):
        self.spec = spec
        self._tool_functions = self.discover()

    def discover(self):
        return {
            method_name: MethodInfo(
                name=method_name,
                description=method.llm_function.__doc__,
                input_model=method.input_model(),
                output_model=method.output_model(),
                fn=method
            )
            for method_name in dir(self)
            for method in [getattr(self, method_name)]
            if hasattr(method, 'llm_function') and isinstance(method.llm_function, dict)
        }

    def is_sync(self):
        return True

    def write_response(self, call_context: CallContext, tool_name: str, response: Dict[str, Any]):
        self.request_write(BusEvent(
            call_context,
            self.spec.lr_write,
            [ToolResponseMessage(tool_name=tool_name, response=response)]
        ))

    async def bus_read(self, event: BusEvent):
        if event.event_type == self.spec.le_read:
            # first clone the event.messages, so we can pop the last item
            messages = event.messages.copy()
            # now remove the last item of the list, make sure it is a ToolCallMessage and check if the tool name matches our name
            message = messages.pop()
            if message.type == "tool_call" and self._tool_functions.get(message.tool_call.tool_name):
                await self._execute(event.call_context, messages, message.tool_call.tool_name,
                                    self._tool_functions.get(message.tool_call.tool_name).fn, message.tool_call.args)

    async def _execute(self, call_context: CallContext, conversation: List[LLMMessage], fn_name: str, fn: Callable, args: Dict[str, Any]):
        # if this is a sync tool call just call execute, if it is not we need to store the state of the conversation and call in memory
        if self.is_sync():
            result = await fn(**args)
            # if result is a base model, call model_dump on it. If it is a string wrap it in an object with a "text" key
            if isinstance(result, BaseModel):
                result = result.model_dump()
            elif isinstance(result, str):
                result = {"text": result}
            elif result is None:
                result = {}
            self.write_response(call_context, fn_name, result)
        else:
            # todo -- store the conversation and args in memory
            raise NotImplementedError("Async tools are not yet supported.")
