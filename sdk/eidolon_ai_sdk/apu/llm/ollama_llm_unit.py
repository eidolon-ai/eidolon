import json
import logging
from typing import List, Optional, Union, Literal, Dict, Any, AsyncIterator, cast, Type

import yaml
from fastapi import HTTPException
from ollama import AsyncClient, ResponseError, Options
from pydantic import Field, create_model, BaseModel

from eidolon_ai_client.events import (
    StringOutputEvent,
    ObjectOutputEvent,
)
from eidolon_ai_client.util.logger import logger as eidolon_logger
from eidolon_ai_sdk.apu.llm_message import (
    LLMMessage,
    AssistantMessage,
    UserMessage,
    SystemMessage,
)
from eidolon_ai_sdk.apu.llm_unit import LLMUnit, LLMCallFunction, LLMModel, LLMUnitSpec
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from eidolon_ai_sdk.system.specable import Specable
from eidolon_ai_sdk.util.replay import replayable

logger = eidolon_logger.getChild("llm_unit")


async def convert_to_ollama(message: LLMMessage):
    if isinstance(message, SystemMessage):
        return {"role": "system", "content": message.content}
    elif isinstance(message, UserMessage):
        content = message.content
        if not isinstance(content, str):
            content = ""
            for part in message.content:
                if part.type == "text":
                    content += part.text
                else:
                    # not supported
                    pass
        return {"role": "user", "content": content}
    elif isinstance(message, AssistantMessage):
        return {"role": "assistant", "content": message.content}
    else:
        raise ValueError(f"Unknown message type {message.type}: {message}")


llama3 = "llama3"

OllamaOptions: Type[BaseModel] = create_model('OllamaOptions', **{
    field_name: (field_type, None) for field_name, field_type in Options.__annotations__.items()
})


class OllamaLLMUnitSpec(LLMUnitSpec):
    model: AnnotatedReference[LLMModel, llama3]
    temperature: float = 0.3
    force_json: bool = True
    max_tokens: Optional[int] = None
    host: Optional[str] = Field(default=None, description="Running Ollama location.\nDefaults to envar OLLAMA_HOST with fallback to 127.0.0.1:11434 if that is not set.")
    client_options: OllamaOptions = Field(default=OllamaOptions(), description="Additional arguments when calling ollama.AsyncClient.chat")


class OllamaLLMUnit(LLMUnit, Specable[OllamaLLMUnitSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        LLMUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)

    async def execute_llm(
        self,
        messages: List[LLMMessage],
        tools: List[LLMCallFunction],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[AssistantMessage]:
        can_stream_message, request = await self._build_request(messages, output_format)

        logger.info("executing ollama llm request")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("request content:\n" + yaml.dump(request))
        llm_request = replayable(fn=_ollama_client(self.spec.host), name_override="ollama_completion", parser=_raw_parser)
        complete_message = ""
        try:
            async for m_chunk in llm_request(**request):
                content = m_chunk["message"]["content"]
                logger.debug(
                    f"ollama ai llm response\ncontent:\n{content}",
                    extra=m_chunk,
                )

                if content:
                    if can_stream_message:
                        logger.debug(f"ollama llm stream response: {content}", extra=dict(content=content))
                        yield StringOutputEvent(content=content)
                    else:
                        complete_message += content

            if not can_stream_message:
                logger.debug(f"ollama llm object response: {complete_message}", extra=dict(content=complete_message))
                if not self.spec.force_json:
                    # message format looks like json```{...}```, parse content and pull out the json
                    complete_message = complete_message[complete_message.find("{") : complete_message.rfind("}") + 1]

                content = json.loads(complete_message) if complete_message else {}
                yield ObjectOutputEvent(content=content)
        except ResponseError as e:
            raise HTTPException(status_code=e.status_code, detail=e.error)

    async def _build_request(self, messages, output_format):
        messages = [await convert_to_ollama(message) for message in messages]
        request = {
            "messages": messages,
            "model": str(self.model.name),
        }
        if output_format == "str" or output_format["type"] == "string":
            is_string = True
        else:
            is_string = False
            force_json_msg = (
                f"Your response MUST be valid JSON satisfying the following JSON schema:\n{json.dumps(output_format)}"
            )

            # add response rules to original system message for this call only
            if messages[0]["role"] == "system":
                messages[0]["content"] += f"\n\n{force_json_msg}"
            else:
                messages.insert(0, {"role": "system", "content": force_json_msg})
        logger.debug(messages)
        options = cast(Options, cast(BaseModel, self.spec.client_options).model_dump(exclude_defaults=True))
        if self.spec.max_tokens:
            options["num_predict"] = self.spec.max_tokens
        if self.spec.temperature >= 0:
            options["temperature"] = self.spec.temperature
        request['options'] = options
        if not is_string:
            request["format"] = "json"
        return is_string, request


def _ollama_client(host: Optional[str]):
    async def fn(**kwargs):
        client: AsyncClient = AsyncClient(host=host)
        async for e in await client.chat(**kwargs, stream=True):
            yield e

    return fn


async def _raw_parser(resp):
    """
    Parses responses from mistral and yield strings to accumulate to a human-readable message.

    Makes assumptions around tool calls. These are currently true, but may change as mistral mutates their API
    1. Tool call functions names are always in a complete message
    2. Tool calls are ordered (No chunk for tool #2 until #1 is complete)
    """
    async for m_chunk in resp:
        message = dict(content=m_chunk)

        if message["message"]:
            yield message["chunk"]["message"]["content"]
