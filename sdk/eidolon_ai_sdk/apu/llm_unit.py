from abc import ABC, abstractmethod
from typing import List, Any, Dict, Literal, Union, AsyncIterator

from pydantic import BaseModel, Field

from eidolon_ai_client.events import StreamEvent, ToolCall
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.apu.llm_message import LLMMessage, AssistantMessage, ToolResponseMessage
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.specable import Specable


class LLMModel(BaseModel):
    human_name: str
    name: str
    input_context_limit: int
    output_context_limit: int
    supports_tools: bool
    supports_image_input: bool
    supports_audio_input: bool


class LLMCapabilities(BaseModel):
    input_context_limit: int
    output_context_limit: int
    supports_tools: bool
    supports_image_input: bool
    supports_audio_input: bool


class CompletionUsage(BaseModel):
    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""


class LLMCallFunction(BaseModel):
    name: str = Field(..., description="The name of the function to call.")
    description: str = Field(..., description="The description of the function to call.")
    parameters: Dict[str, object] = Field(..., description="The json schema for the function parameters.")


class LLMUnitSpec(BaseModel):
    """
    The LLMUnit is a processing unit that is used to interact with a language model.
    """

    model: Reference[LLMModel]


class LLMUnit(ProcessingUnit, Specable[LLMUnitSpec], ABC):
    model: LLMModel

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.model = self.spec.model.instantiate() if self.spec.model else None

    def get_llm_capabilities(self) -> LLMCapabilities:
        return LLMCapabilities(
            input_context_limit=self.model.input_context_limit,
            output_context_limit=self.model.output_context_limit,
            supports_tools=self.model.supports_tools,
            supports_image_input=self.model.supports_image_input,
            supports_audio_input=self.model.supports_audio_input,
        )

    def create_assistant_message(self, call_context: CallContext, contents: str, tool_call_events) -> LLMMessage:
        return AssistantMessage(
            type="assistant",
            content=contents,
            tool_calls=[tce.tool_call for tce in tool_call_events],
        )

    def create_tool_response_message(self, logic_unit_name: str, tc: ToolCall, content: str) -> LLMMessage:
        return ToolResponseMessage(
            logic_unit_name=logic_unit_name,
            tool_call_id=tc.tool_call_id,
            result=content,
            name=tc.name,
        )

    @abstractmethod
    def execute_llm(
        self,
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[StreamEvent]:
        pass
