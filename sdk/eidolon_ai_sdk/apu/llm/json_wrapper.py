import copy
import json
from typing import List, Union, Literal, Dict, Any, AsyncIterator, cast, Optional

from pydantic import BaseModel

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.apu.llm_message import LLMMessage, SystemMessage, UserMessage, UserMessageText
from eidolon_ai_sdk.apu.llm_unit import LLMUnit, LLMCallFunction, LLMUnitSpec
from eidolon_ai_sdk.apu.processing_unit import ProcessingUnit
from eidolon_ai_sdk.system.reference_model import Reference, Specable
from eidolon_ai_sdk.util.stream_collector import StreamCollector


class JsonWrapperSpec(LLMUnitSpec):
    model: Optional[Reference[LLMUnit]] = None
    transformer: Reference[LLMUnit]
    wrapped: Reference[LLMUnit]


class JsonWrapperLLMUnit(LLMUnit, Specable[JsonWrapperSpec]):
    def __init__(self, **kwargs):
        ProcessingUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)
        self._wrapped = self.spec.wrapped.instantiate(processing_unit_locator=self.processing_unit_locator)
        self._transformer = self.spec.transformer.instantiate(processing_unit_locator=self.processing_unit_locator)

    def __getattr__(self, item):
        if item == "execute_llm":
            return self.execute_llm
        elif item.startswith("_"):
            return object.__getattribute__(self, item)
        else:
            return getattr(self._wrapped, item)

    async def execute_llm(self, messages: List[LLMMessage], tools: List[LLMCallFunction], output_format: Union[Literal["str"], Dict[str, Any]]) -> AsyncIterator[StreamEvent]:
        if output_format == "str":
            async for e in self.wrapped.execute_llm(messages, tools, "str"):
                yield e
        else:
            messages = copy.deepcopy(messages)
            if messages[0].type != "system":
                raise ValueError("First message must be a system message to translate to JSON.")
            desired_schema = json.dumps(output_format)
            cast(SystemMessage, messages[0]).content = messages[0].content + f"Your response MUST be valid JSON satisfying the following JSON schema:\n{desired_schema}"
            stream_collector = StreamCollector(self._wrapped.execute_llm(messages, tools, "str"))
            async for e in stream_collector:
                logger.debug(f"received {e}")
            translation_messages = [
                SystemMessage(content="You are a helpful assistant who translates strings to JSON. Take the following message and translate the relevant portions to properly formatted json."),
                UserMessage(content=UserMessageText(text=(stream_collector.get_content())))
            ]
            async for e in self._transformer.execute_llm(translation_messages, tools, output_format):
                yield e
