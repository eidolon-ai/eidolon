from abc import ABC, abstractmethod
from typing import List, Dict, Any

from pydantic import BaseModel, Field

from eidolon_sdk.cpu.agent_bus import BusEvent, CallContext
from eidolon_sdk.cpu.bus_messages import READ_PORT
from eidolon_sdk.cpu.llm_message import LLMMessage, ToolResponseMessage
from eidolon_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_sdk.reference_model import Specable


class LogicUnitConfig:
    le_read: READ_PORT = Field(description="A port that, when bound to an event, will read the LLM tool call from the bus.")
    lr_write: READ_PORT = Field(description="A port that, when bound to an event, will write the tool call response to the bus.")
    name: str = Field(description="The name of this tool.")


class LogicUnit(ProcessingUnit, Specable[LogicUnitConfig], ABC):
    def __init__(self, spec: LogicUnitConfig = None):
        self.spec = spec

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def input_model(self) -> BaseModel:
        pass

    @abstractmethod
    def output_model(self) -> BaseModel:
        pass

    @abstractmethod
    def is_sync(self):
        return True

    @abstractmethod
    async def execute(self, conversation: List[LLMMessage], args: Dict[str, Any]) -> Dict[str, Any]:
        pass

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
            if message.type == "tool_call" and message.tool_call.tool_name == self.spec.name:
                await self._execute(event.call_context, messages, message.tool_call.args)

    async def _execute(self, call_context: CallContext, conversation: List[LLMMessage], args: Dict[str, Any]):
        # if this is a sync tool call just call execute, if it is not we need to store the state of the conversation and call in memory
        if self.is_sync():
            result = await self.execute(conversation, args)
            self.write_response(call_context, self.spec.name, result)
        else:
            # todo -- store the conversation and args in memory
            raise NotImplementedError("Async tools are not yet supported.")
