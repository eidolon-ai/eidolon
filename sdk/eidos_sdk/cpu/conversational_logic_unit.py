import json
from typing import List, Optional, Any
from urllib.parse import urljoin

import aiohttp
import jsonref as jsonref
from pydantic import BaseModel, ValidationError

from eidos_sdk.cpu.llm_message import LLMMessage, ToolResponseMessage
from eidos_sdk.cpu.logic_unit import LogicUnit
from eidos_sdk.system.agent_contract import SyncStateResponse
from eidos_sdk.system.eidos_handler import EidosHandler
from eidos_sdk.system.reference_model import Specable
from eidos_sdk.util.logger import logger
from eidos_sdk.util.schema_to_model import schema_to_model


class ConversationalResponse(SyncStateResponse):
    program: str


class ConversationalSpec(BaseModel):
    location: str = "http://localhost:8080"
    tool_prefix: str = "convo"
    agents: List[str]


class ConversationalLogicUnit(LogicUnit, Specable[ConversationalSpec]):
    _openapi_json: Optional[dict]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self._openapi_json = None

    def set_openapi_json(self, openapi_json):
        self._openapi_json = jsonref.replace_refs(openapi_json)

    async def build_tools(self, conversation: List[LLMMessage]) -> List[EidosHandler]:
        if not self._openapi_json:
            self.set_openapi_json(await _get_openapi_schema(urljoin(self.spec.location, "openapi.json")))

        tools = []

        for agent in self.spec.agents:
            prefix = f"/agents/{agent}/programs/"
            for path in filter(lambda p: p.startswith(prefix), self._openapi_json["paths"].keys()):
                try:
                    action = path.removeprefix(prefix)
                    name = self._name(agent, action=action)
                    tools.append(await self._build_tool_def(name, path, agent))
                except ValueError:
                    logger.warning(f"unable to build tool {path}", exc_info=True)

        # in case new spec removes ability to talk to agents, existing agents should not be able to continue talking to them
        allowed_agent_prefix = tuple(self._name(agent) for agent in self.spec.agents)
        processes = {}
        for message in conversation:
            if isinstance(message, ToolResponseMessage) and message.name.startswith(allowed_agent_prefix):
                try:
                    last = ConversationalResponse.model_validate(json.loads(message.result))
                    processes[last.process_id] = last
                except ValidationError:
                    logger.warning("unable to parse conversation response", exc_info=True)

        # newer process state should override older process state if there are multiple calls
        for action, response in ((a, r) for r in processes.values() for a in r.available_actions):
            path = f"/agents/{response.program}/processes/{{process_id}}/actions/{action}"
            try:
                name = self._name(response.program, action, response.process_id)
                tools.append(await self._build_tool_def(name, path, response.program, process_id=response.process_id))
            except ValueError:
                logger.warning(f"unable to build tool {path}", exc_info=True)

        return tools

    async def _build_tool_def(self, name, path, agent_program, process_id="") -> EidosHandler:
        path = path.format(process_id="{process_id}")
        body = self._openapi_json["paths"][path]["post"].get("requestBody")
        if body and "application/json" not in body["content"]:
            raise ValueError(f"Agent action at {path} does not support application/json")
        json_schema = body["content"]["application/json"]["schema"] if body else dict(type="object", properties={})
        description = self._openapi_json["paths"][path]["post"].get("description", "")
        if not description:
            self.logger.warning(f"Agent action at {path} does not have a description. LLM may not use it properly")
        return EidosHandler(
            name=name,
            description=lambda a, b: description,
            input_model_fn=lambda a, b: schema_to_model(
                dict(type="object", properties=dict(body=json_schema)),
                name + "Input",
            ),
            output_model_fn=lambda a, b: Any,
            fn=self._make_tool_fn(
                path=path.replace("{process_id}", process_id),
                agent_program=agent_program,
            ),
            extra={},
        )

    # needs to be under 64 characters
    def _name(self, agent_program, action="", process_id=""):
        agent_program = agent_program[:15]
        process_id = process_id[:25]
        process_id = "_" + process_id if process_id else ""
        action = action[:15]
        action = "_" + action if action else ""
        return self.spec.tool_prefix + "_" + agent_program + process_id + action

    def _make_tool_fn(self, path, agent_program):
        async def fn(_self, body):
            url = urljoin(self.spec.location, path)
            if isinstance(body, BaseModel):
                body = body.model_dump()
            response = await _agent_request(url, body)
            response["program"] = agent_program
            return ConversationalResponse.model_validate(response).model_dump()

        return fn


async def _agent_request(url, args):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=args) as resp:
            return await resp.json()


async def _get_openapi_schema(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()
