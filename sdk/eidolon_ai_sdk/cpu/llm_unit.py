from abc import ABC, abstractmethod
from typing import List, Any, Dict, Literal, Union, AsyncIterator

from pydantic import BaseModel, Field

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import LLMMessage
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Specable

LLM_MAX_TOKENS = {
    "DEFAULT": 8192,
    # OpenAI models: https://platform.openai.com/docs/models/overview
    # gpt-4
    "gpt-4-1106-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-0613": 8192,
    "gpt-4-32k-0613": 32768,
    "gpt-4-0314": 8192,  # legacy
    "gpt-4-32k-0314": 32768,  # legacy
    # gpt-3.5
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-0613": 4096,  # legacy
    "gpt-3.5-turbo-16k-0613": 16385,  # legacy
    "gpt-3.5-turbo-0301": 4096,  # legacy
}


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
    model: str = Field(description="The model to use for the LLM.")
    supported_models: List[LLMModel] = Field(default=[], description="The list of supported models or leave empty for defaults.")


class LLMUnit(ProcessingUnit, Specable[LLMUnitSpec], ABC):
    model: LLMModel

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)

        for model in self.get_models():
            if model.name == self.spec.model:
                self.model = model
                break

        if not hasattr(self, "model"):
            raise ValueError(f"Model {self.spec.model} not found in {self.get_models()}")

    def get_llm_capabilities(self) -> LLMCapabilities:
        return LLMCapabilities(
            input_context_limit=self.model.input_context_limit,
            output_context_limit=self.model.output_context_limit,
            supports_tools=self.model.supports_tools,
            supports_image_input=self.model.supports_image_input,
            supports_audio_input=self.model.supports_audio_input,
        )

    @abstractmethod
    def get_models(self) -> List[LLMModel]:
        pass

    @abstractmethod
    async def execute_llm(
        self,
        call_context: CallContext,
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[StreamEvent]:
        pass
