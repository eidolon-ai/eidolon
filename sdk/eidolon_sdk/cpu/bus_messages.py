from typing import List, Union, Any, Dict

from pydantic import BaseModel

from eidolon_sdk.cpu.llm_message import SystemMessage, UserMessage, LLMMessage, AssistantMessage


class BusMessage(BaseModel):
    event_type: str


class InputRequest(BusMessage):
    event_type: str = "input_request"
    messages: List[Union[UserMessage, SystemMessage]]
    output_format: dict[str, Any]


class AddConversationHistory(BusMessage):
    event_type: str = "add_conversation_history"
    messages: List[Union[UserMessage, SystemMessage]]
    output_format: dict[str, Any]


class LLMEvent(BusMessage):
    event_type: str = "llm_event"
    messages: List[LLMMessage]
    output_format: dict[str, Any]


class LLMResponse(BusMessage):
    event_type: str = "llm_response"
    message: AssistantMessage


class OutputResponse(BusMessage):
    event_type: str = "output_response"
    response: Dict[str, Any]


# A new type that is used to bind a read port to an event
READ_PORT = str

# A new type that is used to bind a write port to an event
WRITE_PORT = str
