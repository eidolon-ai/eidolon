import copy
import json
import logging
import os
from typing import List, Optional, Union, Literal, Dict, Any, AsyncIterator, cast

import google.generativeai as genai
import yaml
from fastapi import HTTPException
from google.generativeai import GenerativeModel
from google.generativeai.types import GenerateContentResponse

from eidolon_ai_client.events import (
    StringOutputEvent,
    ObjectOutputEvent,
    LLMToolCallRequestEvent,
)
from eidolon_ai_client.util.logger import logger as eidolon_logger
from eidolon_ai_sdk.apu.llm_message import (
    LLMMessage,
    AssistantMessage,
    ToolResponseMessage,
    UserMessage,
    SystemMessage,
)
from eidolon_ai_sdk.apu.llm_unit import LLMUnit, LLMCallFunction, LLMModel, LLMUnitSpec
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
from eidolon_ai_sdk.util.replay import replayable

logger = eidolon_logger.getChild("llm_unit")


async def convert_to_gemini(message: LLMMessage):
    if isinstance(message, SystemMessage):
        return {"role": "user", "parts": [message.content]}
    elif isinstance(message, UserMessage):
        content = message.content
        if not isinstance(content, str):
            content = []
            for part in message.content:
                if part.type == "text":
                    if part.text:
                        content.append(part.text)
                else:
                    logger.warn(f"Unhandled message content part type: {part.type}")

        else:
            content = [content]

        return {"role": "user", "parts": content}
    elif isinstance(message, AssistantMessage):
        content = [message.content]
        if message.tool_calls and len(message.tool_calls) > 0:
            logger.debug(f"Gemini instructed tool calls: {message.tool_calls}")
            for tool_call in message.tool_calls:
                pass
                # content.append(ToolUseBlockParam(type="tool_use", id=tool_call.tool_call_id, name=tool_call.name, input=tool_call.arguments))
        return {"role": "model", "parts": content}
    elif isinstance(message, ToolResponseMessage):
        # tool_call_id, content
        data = json.dumps(message.result)
        content = [data]
        return {"role": "user", "parts": [{
            "type": "tool_result",
            "tool_use_id": message.tool_call_id,
            "content": content
        }
        ]}
    else:
        raise ValueError(f"Unknown message type {message.type}")


gemini = "gemini-1.5-flash"


class GeminiLLMUnitSpec(LLMUnitSpec):
    model: AnnotatedReference[LLMModel, gemini]
    temperature: float = 0.3
    max_tokens: Optional[int] = None


class GeminiLLMUnit(LLMUnit, Specable[GeminiLLMUnitSpec]):
    temperature: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        LLMUnit.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)

        self.temperature = self.spec.temperature
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    async def execute_llm(
            self,
            messages: List[LLMMessage],
            tools: List[LLMCallFunction],
            output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> AsyncIterator[AssistantMessage]:
        can_stream_message, request = await self._build_request(messages, tools, output_format)

        logger.info("Executing Gemini LLM request", extra=request)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("request content:\n" + yaml.dump(request))
        llm_request = replayable(fn=_llm_request(), name_override="gemini_completion", parser=_raw_parser)
        complete_message = ""
        tools_to_call = []
        generative_args = {
            "model_name": self.model.name,
            "generation_config": {
                "max_output_tokens": self.spec.max_tokens or 4000,
                "temperature": self.temperature,
                "candidate_count": 1,
            },
        }
        if "systemInstruction" in request:
            generative_args["system_instruction"] = request["systemInstruction"]
            del request["systemInstruction"]
        try:
            async for in_message in llm_request(client_args=generative_args, **request):
                message = cast(GenerateContentResponse, in_message).text

                if message:
                    if can_stream_message:
                        logger.debug(
                            f"gemini llm stream response: {message}", extra=dict(content=message)
                        )
                        yield StringOutputEvent(content=message)
                    else:
                        complete_message += message

            if len(tools_to_call) > 0:
                logger.info(f"gemini llm tool calls: {tools_to_call}", extra=dict(tool_calls=tools_to_call))
                for tool in tools_to_call:
                    yield LLMToolCallRequestEvent(tool_call=tool)

            if not can_stream_message:
                logger.debug(f"gemini llm object response: {complete_message}", extra=dict(content=complete_message))
                # message format looks like json```{...}```, parse content and pull out the json
                complete_message = complete_message[complete_message.find("{"): complete_message.rfind("}") + 1]

                content = json.loads(complete_message) if complete_message else {}
                yield ObjectOutputEvent(content=content)
        except Exception as e:
            logger.exception(e)
            raise HTTPException(502, f"Gemini Error: {e}") from e

    async def _build_request(self, inMessages, inTools, output_format):
        tools = await self._build_tools(inTools)
        system_prompt = "\n".join([message.content for message in inMessages if isinstance(message, SystemMessage)])
        messages = [await convert_to_gemini(message) for message in inMessages if not isinstance(message, SystemMessage)]
        if output_format == "str" or output_format["type"] == "string":
            is_string = True
        else:
            is_string = False
            force_json_msg = (
                f"Your response MUST be valid JSON satisfying the following JSON schema:\n{json.dumps(output_format)}"
            )
            force_json_msg += "\nThe response will be wrapped in a json section json```{...}```\nRemember to use double quotes for strings and properties."

            # add response rules to original system message for this call only
            messages.insert(0, {"role": "user", "parts": [force_json_msg]})

        # combine messages such that no two user messages are consecutive
        last_message = None
        new_messages = []
        for message in messages:
            if message["role"] == "user":
                if last_message and last_message["role"] == "user":
                    content = message["parts"]
                    last_message["parts"].extend(content)
                else:
                    new_messages.append(message)
            else:
                new_messages.append(message)
            last_message = message

        request = {"contents": new_messages}
        if system_prompt:
            request["systemInstruction"] = {"role": "user", "parts": [system_prompt]}

        if len(tools) > 0:
            request["tools"] = tools
        return is_string, request

    async def _build_tools(self, inTools):
        tools = []
        for tool in inTools:
            params = JsonSchemaToGoogleProtobufSchemaConverter().convert_to_protobuf(tool.parameters)

            tools.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": params,
                }
            )
        return tools


class JsonSchemaToGoogleProtobufSchemaConverter:
    def convert_to_protobuf(self, json_schema: dict) -> dict:
        # The Gemini tool spec only supports a subset of OpenAPI schemas:
        # https://github.com/googleapis/google-cloud-python/blob/main/packages/google-ai-generativelanguage/google/ai/generativelanguage_v1beta/types/content.py#L641

        params = copy.deepcopy(json_schema)

        self._remove_key_from_dict(params, '$defs')
        self._remove_key_from_dict(params, 'title')
        self._remove_key_from_dict(params, 'default')

        self._remove_object_types_without_properties(params)

        self._replace_anyOf_values(params)
        self._rename_type_values(params)

        return params

    def _remove_key_from_dict(self, d, key_to_remove):
        if isinstance(d, dict):
            if key_to_remove in d:
                del d[key_to_remove]
            for value in d.values():
                self._remove_key_from_dict(value, key_to_remove)
        elif isinstance(d, list):
            for item in d:
                self._remove_key_from_dict(item, key_to_remove)

    def _replace_anyOf_values(self, d: dict):
        if isinstance(d, dict):
            if 'anyOf' in d:
                values = d['anyOf']
                if not isinstance(values, list):
                    raise ValueError(f"Unexpected 'anyOf' value type: {type(values)}")

                d['type'] = values[0]['type']
                del d['anyOf']
            for value in d.values():
                self._replace_anyOf_values(value)
        elif isinstance(d, list):
            for item in d:
                self._replace_anyOf_values(item)

    def _remove_object_types_without_properties(self, d: dict):
        if isinstance(d, dict):
            keys_to_del = []

            for key, value in d.items():
                self._remove_object_types_without_properties(value)

                if isinstance(value, dict):
                    if 'type' in value and value['type'] == 'object' and 'properties' not in value:
                        keys_to_del.append(key)

            for k in keys_to_del:
                del d[k]

        elif isinstance(d, list):
            for item in d:
                self._remove_object_types_without_properties(item)

    def _rename_type_values(self, d: dict):
        if isinstance(d, dict):
            # The field name "type" is not supported in the Protobuf serialization; it must be renamed to "type_".
            # See: google.ai.generativelanguage_v1beta.types.content.Schema

            if 'type' in d:
                # The type values are uppercased, per the ENUM definitions:
                # See: google.ai.generativelanguage_v1beta.types.content.Type
                d['type_'] = d['type'].upper()
                del d['type']
            for value in d.values():
                self._rename_type_values(value)
        elif isinstance(d, list):
            for item in d:
                self._rename_type_values(item)


def _llm_request():
    async def fn(client_args: dict = None, **kwargs):
        client = GenerativeModel(**(client_args or {}))
        async for e in await client.generate_content_async(**kwargs, stream=True):
            logger.debug(e)
            yield e

    return fn


async def _raw_parser(resp):
    async for in_message in resp:
        message = cast(GenerateContentResponse, in_message)
        yield message.text
