import inspect
import typing
from abc import ABC
from dataclasses import dataclass
from typing import List, Dict, Any, Callable

from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo

from eidolon_sdk.cpu.agent_bus import BusEvent, CallContext
from eidolon_sdk.cpu.bus_messages import READ_PORT
from eidolon_sdk.cpu.llm_message import LLMMessage, ToolResponseMessage
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.reference_model import Specable
from eidolon_sdk.util.class_utils import get_function_details, fqn


def llm_function(fn):
    setattr(fn, 'llm_function', True)
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
    output_model = typing.get_type_hints(fn, include_extras=True).get('return', typing.Any)
    setattr(fn, 'input_model', input_model)
    setattr(fn, 'output_model', output_model)
    return fn


@dataclass
class MethodInfo:
    name: str
    description: str
    input_model: BaseModel
    output_model: BaseModel
    fn: Callable


class LogicUnitConfig(BaseModel):
    lu_read: READ_PORT = Field(default=None, description="A port that, when bound to an event, will read the LLM tool call from the bus.")
    lu_write: READ_PORT = Field(default=None, description="A port that, when bound to an event, will write the tool call response to the bus.")


class LogicUnit(ProcessingUnit, Specable[LogicUnitConfig], ABC):
    def __init__(self, spec: LogicUnitConfig = None):
        self.spec = spec
        self._tool_functions = self.discover()

    def discover(self):
        return {
            method_name: MethodInfo(
                name=method_name,
                description=method.__doc__,
                input_model=method.input_model,
                output_model=method.output_model,
                fn=method
            )
            for method_name in dir(self)
            for method in [getattr(self, method_name)]
            if hasattr(method, 'llm_function')
        }

    def is_sync(self):
        return True

    def write_response(self, call_context: CallContext, tool_name: str, response: Dict[str, Any]):
        self.request_write(BusEvent(
            call_context,
            self.spec.lu_write,
            [ToolResponseMessage(tool_name=tool_name, response=response)]
        ))

    async def bus_read(self, event: BusEvent):
        if event.event_type == self.spec.lu_read:
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
