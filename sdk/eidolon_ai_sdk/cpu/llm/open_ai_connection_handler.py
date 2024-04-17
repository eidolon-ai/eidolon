import os
from typing import Optional, cast, List

from azure.identity import get_bearer_token_provider, EnvironmentCredential
from openai import AsyncOpenAI, AsyncStream
from openai.lib.azure import AsyncAzureOpenAI
from openai.types import ImagesResponse
from openai.types.chat import ChatCompletionChunk, ChatCompletion
from pydantic import BaseModel, Field

from eidolon_ai_sdk.system.reference_model import Specable, Reference
from eidolon_ai_sdk.util.replay import replayable


class OpenAIConnectionHandlerSpec(BaseModel, extra="allow"):
    pass


class OpenAIConnectionHandler(Specable[OpenAIConnectionHandlerSpec]):
    def makeClient(self) -> AsyncOpenAI:
        return AsyncOpenAI(**self.spec.model_extra)

    async def completion(self, **kwargs) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        return await replayable(
            fn=lambda **_kwargs: self.makeClient().chat.completions.create(**_kwargs),
            parser=_replay_parser,
            name_override="openai_completion",
        )(**kwargs)

    async def generate_image(self, **kwargs) -> ImagesResponse:
        # todo, image generation should be repayable, but needs custom parser
        return await self.makeClient().images.generate(**kwargs)


def get_default_token_provider():
    if os.environ.get("AZURE_CLIENT_ID") and os.environ.get("AZURE_CLIENT_SECRET") and os.environ.get("AZURE_TENANT_ID"):
        return Reference[EnvironmentCredential]()
    return None


class AzureOpenAIConnectionHandlerSpec(OpenAIConnectionHandlerSpec):
    """
    Automatically infers the values from environment variables for:
        - `api_key` from `AZURE_OPENAI_API_KEY` (IFF `api_key` AND 'azure_ad_token_provider' is not provided)
        - `organization` from `OPENAI_ORG_ID`
        - `azure_ad_token` from `AZURE_OPENAI_AD_TOKEN`
        - `api_version` from `OPENAI_API_VERSION`
        - `azure_endpoint` from `AZURE_OPENAI_ENDPOINT`
    """

    azure_ad_token_provider: Optional[Reference] = Field(default_factory=get_default_token_provider)
    token_provider_scopes: List[str] = ["https://cognitiveservices.azure.com/.default"]
    api_version: str = os.environ.get("OPENAI_API_VERSION") or "2024-02-01"


class AzureOpenAIConnectionHandler(OpenAIConnectionHandler, Specable[AzureOpenAIConnectionHandlerSpec]):
    def makeClient(self):
        params = self.spec.model_extra
        if self.spec.azure_ad_token_provider:
            provider = self.spec.azure_ad_token_provider.instantiate()
            token_provider = get_bearer_token_provider(provider, *self.spec.token_provider_scopes)
            params["azure_ad_token_provider"] = token_provider
        params["api_version"] = self.spec.api_version
        return AsyncAzureOpenAI(**params)


async def _replay_parser(resp):
    """
    Parses responses from openai and yield strings to accumulate to a human-readable message.

    Makes assumptions around tool calls. These are currently true, but may change as openai mutates their API
    1. Tool call functions names are always in a complete message
    2. Tool calls are ordered (No chunk for tool #2 until #1 is complete)
    """
    calling_tools = False
    prefix = ""
    await_resp = await resp
    if hasattr(await_resp, "__aiter__"):
        async for m_chunk in await_resp:
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
    else:
        message = await_resp.choices[0].message
        if message.tool_calls:
            for i, tool_call in enumerate(message.tool_calls):
                if tool_call.function.name:
                    yield f"Tool Call: {tool_call.function.name}\nArguments: "
                if tool_call.function.arguments:
                    yield tool_call.function.arguments
                yield "\n"
        if message.content:
            yield message.content
