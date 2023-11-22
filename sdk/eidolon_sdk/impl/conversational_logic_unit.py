import json
from typing import Dict, List, Optional
from urllib.parse import urljoin

import aiohttp
import jsonref as jsonref
from pydantic import BaseModel

from eidolon_sdk.agent_program import SyncStateResponse
from eidolon_sdk.cpu.llm_message import LLMMessage, ToolResponseMessage
from eidolon_sdk.cpu.llm_unit import LLMCallFunction
from eidolon_sdk.cpu.logic_unit import LogicUnit, ToolDefType, MethodInfo
from eidolon_sdk.reference_model import Specable
from eidolon_sdk.util.schema_to_model import schema_to_model


class ConversationalResponse(SyncStateResponse):
    program: str


class ConversationalSpec(BaseModel):
    location: str = 'http://localhost:8080'
    tool_prefix: str = "eidolon_conversation"
    agents: List[str]


class ConversationalLogicUnit(LogicUnit, Specable[ConversationalSpec]):
    def __init__(self, spec: ConversationalSpec, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    _openapi_json: Optional[dict] = None

    def set_openapi_json(self, openapi_json):
        self._openapi_json = jsonref.replace_refs(openapi_json)

    async def build_tools(self, conversation: List[LLMMessage]) -> Dict[str, ToolDefType]:
        if not self._openapi_json:
            async with aiohttp.ClientSession() as session:
                async with session.get(urljoin(self.spec.location, "openapi.json")) as resp:
                    self.set_openapi_json(await resp.json())

        tools = {}

        for agent in self.spec.agents:
            path = f'/programs/{agent}'
            tools[path] = await self._build_tool_def(path, agent)

        # in case new spec removes ability to talk to agents, existing agents should not be able to continue talking to them
        allowed_agent_prefix = tuple(self.spec.tool_prefix + "_programs_" + agent for agent in self.spec.agents)
        processes = {}
        for message in conversation:
            if isinstance(message, ToolResponseMessage) and message.name.startswith(allowed_agent_prefix):
                last = ConversationalResponse.model_validate(json.loads(message.result))  # todo, perhaps we should be converting these to strings when calling the model rather than saving them this way?
                processes[last.process_id] = last

        # newer process state should override older process state if there are multiple calls
        for action, response in ((a, r) for r in processes.values() for a in r.available_actions):
            path = f'/programs/{response.program}/processes/{{process_id}}/actions/{action}'
            tools[path] = await self._build_tool_def(path, response.program)

        return {self._name(k): v for k, v in tools.items()}

    async def _build_tool_def(self, path, agent_program):
        json_schema = self._openapi_json['paths'][path]['post']['requestBody']['content']['application/json']['schema']
        description = "Create a conversation with the given agent"  # todo, derive this from openapi
        tool_def_type = ToolDefType(
            self,
            MethodInfo(
                name=self._name(path),
                description=description,
                input_model=schema_to_model(json_schema, self._name(path) + "_input_model"),
                fn=_build_fn(path, agent_program)
            ),
            LLMCallFunction(
                name=self._name(path),
                description=description,
                parameters=json_schema
            )
        )
        return tool_def_type

    def _name(self, path):
        return self.spec.tool_prefix + path.replace("/", "_")


def _build_fn(path, agent_program):
    async def fn(self: ConversationalLogicUnit, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.post(urljoin(self.spec.location, path), json=kwargs) as resp:
                json_ = await resp.json()
                json_['program'] = agent_program
                ConversationalResponse.model_validate(json_)
                return json_
    return fn
