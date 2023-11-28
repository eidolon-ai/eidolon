from abc import ABC
from typing import List, Dict, Any
from urllib.parse import urljoin

import httpx
from fastapi import HTTPException
from httpx import Timeout, ReadTimeout
from pydantic import Field

from eidolon_sdk.agent import Agent, initializer
from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage, AssistantMessage, LLMMessageTypes
from eidolon_sdk.cpu.llm_unit import LLMUnitConfig, LLMUnit, LLMCallFunction
from eidolon_sdk.reference_model import Specable


class AgentLLMConfig(LLMUnitConfig):
    model: str = "unneeded, remove"  #todo, remove this field
    machine: str = "http://localhost:8080"
    agent: str = Field(description="The agent to use for the LLM. Agent must conform to the llm interface.")


class AgentLLMUnit(LLMUnit, Specable[AgentLLMConfig]):
    async def execute_llm(self, call_context: CallContext, messages: List[LLMMessage], tools: List[LLMCallFunction], output_format: Dict[str, Any]) -> AssistantMessage:
        # todo, should use callbacks here since these requests take a long time
        async with httpx.AsyncClient(timeout=Timeout(120)) as client:
            try:
                req = await client.post(urljoin(self.spec.machine, f"/programs/{self.spec.agent}"), json=dict(
                    call_context=call_context.model_dump(),
                    messages=[m.model_dump() for m in messages],
                    tools=[t.model_dump(exclude={'fn'}) for t in tools],
                    output_format=output_format
                ))
            except ReadTimeout:
                raise HTTPException(status_code=408, detail="The request timed out")
            if 299 < req.status_code < 500:
                raise HTTPException(status_code=req.status_code, detail=req.json())
            req.raise_for_status()
            return AssistantMessage(**req.json()['data'])


class LLMAgent(Agent, ABC):
    @initializer
    async def __initializer(self, call_context: CallContext, messages: List[LLMMessageTypes], tools: List[LLMCallFunction] = None, output_format: Dict[str, Any] = None) -> AssistantMessage:
        return await self.execute_llm(call_context, messages, tools or [], output_format or dict(type="string"))

    async def execute_llm(self, call_context: CallContext, messages: List[LLMMessageTypes], tools: List[LLMCallFunction], output_format: Dict[str, Any]) -> AssistantMessage:
        ...
