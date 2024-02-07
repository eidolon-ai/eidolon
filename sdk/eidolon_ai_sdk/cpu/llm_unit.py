from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import List, Any, Dict, Literal, Union, AsyncIterator

from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.llm_message import LLMMessage
from eidolon_ai_sdk.cpu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.io.events import StreamEvent

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


class LLMUnit(ProcessingUnit, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    async def execute_llm(
        self,
        call_context: CallContext,
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[StreamEvent]:
        pass
