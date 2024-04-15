from typing import Optional, cast, List

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from fastapi import HTTPException
from openai import AsyncOpenAI, AsyncStream, APIConnectionError, RateLimitError, APIStatusError
from openai.lib.azure import AsyncAzureOpenAI
from openai.types import ImagesResponse
from openai.types.chat import ChatCompletionChunk, ChatCompletion
from pydantic import BaseModel

from eidolon_ai_sdk.system.reference_model import Specable, Reference
from eidolon_ai_sdk.util.replay import replayable


class OpenAIConnectionHandlerSpec(BaseModel, extra='allow'):
    pass


class OpenAIConnectionHandler(Specable[OpenAIConnectionHandlerSpec]):
    def makeClient(self) -> AsyncOpenAI:
        return AsyncOpenAI(**self.spec.model_extra)

    async def completion(self, kwargs: dict) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        return await self._do_request(self.makeClient().chat.completions.create, kwargs)

    async def generate_image(self, kwargs: dict) -> ImagesResponse:
        return await self._do_request(self.makeClient().images.generate, kwargs)

    async def _do_request(self, open_ai_fn, kwargs: dict):
        async def _send_request():
            try:
                async for e in await self.makeClient().chat.completions.create(**kwargs):
                    yield e
            except APIConnectionError as e:
                raise HTTPException(502, f"OpenAI Error: {e.message}") from e
            except RateLimitError as e:
                raise HTTPException(429, "OpenAI Rate Limit Exceeded") from e
            except APIStatusError as e:
                raise HTTPException(502, f"OpenAI Status Error: {e.message}") from e

        async def _send_request_no_gen() -> ChatCompletion:
            return await open_ai_fn(**kwargs)

        if kwargs.get("stream"):
            print("here")
            llm_request = replayable(
                fn=_send_request, name_override="openai_completion", parser=_open_ai_replay_parser
            )

            return llm_request()
        else:
            llm_request = replayable(
                fn=_send_request_no_gen, name_override="openai_completion", parser=_open_ai_replay_parser_no_stream
            )
            return await llm_request()


class AzureOpenAIConnectionHandlerSpec(OpenAIConnectionHandlerSpec):
    """
    Automatically infers the values from environment variables for:
        - `api_key` from `AZURE_OPENAI_API_KEY` (IFF `api_key` AND 'azure_ad_token_provider' is not provided)
        - `organization` from `OPENAI_ORG_ID`
        - `azure_ad_token` from `AZURE_OPENAI_AD_TOKEN`
        - `api_version` from `OPENAI_API_VERSION`
        - `azure_endpoint` from `AZURE_OPENAI_ENDPOINT`
        """
    token_provider: Optional[Reference[DefaultAzureCredential]] = None
    token_provider_scopes: List[str] = ["https://cognitiveservices.azure.com/.default"]


class AzureOpenAIConnectionHandler(OpenAIConnectionHandler, Specable[AzureOpenAIConnectionHandlerSpec]):
    def makeClient(self):
        params = self.spec.model_extra
        if self.spec.token_provider:
            provider = self.spec.token_provider.instantiate()
            token_provider = get_bearer_token_provider(provider, *self.spec.token_provider_scopes)
            params["token_provider"] = token_provider
        return AsyncAzureOpenAI(**params)


async def _open_ai_replay_parser(resp):
    """
    Parses responses from openai and yield strings to accumulate to a human-readable message.

    Makes assumptions around tool calls. These are currently true, but may change as openai mutates their API
    1. Tool call functions names are always in a complete message
    2. Tool calls are ordered (No chunk for tool #2 until #1 is complete)
    """
    calling_tools = False
    prefix = ""
    async for m_chunk in resp:
        chunk = cast(ChatCompletionChunk, m_chunk)
        if not chunk.choices:
            continue
        message = chunk.choices[0].delta

        if message.tool_calls:
            calling_tools = True
            for i, tool_call in enumerate(message.tool_calls):
                if tool_call.function.name:
                    yield prefix + f"Tool Call: {tool_call.function.name}\nArguments: "
                    prefix = "\n"
                if tool_call.function.arguments:
                    yield tool_call.function.arguments
        elif calling_tools:
            yield "\n"
        if message.content:
            yield message.content
            prefix = "\n"


async def _open_ai_replay_parser_no_stream(resp: ChatCompletion):
    """
    Parses responses from openai and yield strings to accumulate to a human-readable message.

    Makes assumptions around tool calls. These are currently true, but may change as openai mutates their API
    1. Tool call functions names are always in a complete message
    2. Tool calls are ordered (No chunk for tool #2 until #1 is complete)
    """
    message = resp.choices[0].message

    if message.tool_calls:
        for i, tool_call in enumerate(message.tool_calls):
            if tool_call.function.name:
                yield f"Tool Call: {tool_call.function.name}\nArguments: "
            if tool_call.function.arguments:
                yield tool_call.function.arguments
            yield "\n"
    if message.content:
        yield message.content
