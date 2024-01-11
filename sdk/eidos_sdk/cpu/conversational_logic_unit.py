import json
from typing import List, Optional, Any
from urllib.parse import urljoin

import jsonref as jsonref
from pydantic import BaseModel, ValidationError

from eidos_sdk.agent.client import Machine, ProcessStatus
from eidos_sdk.cpu.llm_message import LLMMessage, ToolResponseMessage
from eidos_sdk.cpu.logic_unit import LogicUnit
from eidos_sdk.system.agent_contract import SyncStateResponse
from eidos_sdk.system.eidos_handler import EidosHandler
from eidos_sdk.system.reference_model import Specable
from eidos_sdk.util.aiohttp import ContextualClientSession
from eidos_sdk.util.logger import logger
from eidos_sdk.util.schema_to_model import schema_to_model


class ConversationalResponse(SyncStateResponse):
    program: str


class ConversationalSpec(BaseModel):
    location: str = "localhost:8080"
    tool_prefix: str = "convo"
    agents: List[str]


class ConversationalLogicUnit(LogicUnit, Specable[ConversationalSpec]):
    _openapi_json: Optional[dict]
    _machine: Machine

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self._machine = Machine(machine=self.spec.location)
        self._openapi_json = None

    async def build_tools(self, conversation: List[LLMMessage]) -> List[EidosHandler]:
        if not self._openapi_json:
            schema = await self._machine.get_schema()
            self._openapi_json = jsonref.replace_refs(schema)

        tools = []

        for agent in self.spec.agents:
            prefix = f"/agents/{agent}/programs/"
            for path in filter(lambda p: p.startswith(prefix), self._openapi_json["paths"].keys()):
                try:
                    program = path.removeprefix(prefix)
                    name = self._name(agent, action=program)
                    tool = self._build_tool_def(name, path, self._program_tool(agent, program))
                    tools.append(tool)
                except ValueError:
                    logger.warning(f"unable to build tool {path}", exc_info=True)

        # in case new spec removes ability to talk to agents, existing agents should not be able to continue talking to them
        allowed_agent_prefix = tuple(self._name(agent) for agent in self.spec.agents)
        processes: List[ProcessStatus] = []
        for message in conversation:
            if isinstance(message, ToolResponseMessage) and message.name.startswith(allowed_agent_prefix):
                try:
                    processes.append(ProcessStatus.model_validate(json.loads(message.result)))
                except ValidationError:
                    logger.warning("unable to parse conversation response, skipping", exc_info=True)

        # newer process state should override older process state if there are multiple calls
        for action, response in ((a, r) for r in processes.values() for a in r.available_actions):
            path = f"/agents/{response.program}/processes/{{process_id}}/actions/{action}"
            try:
                name = self._name(response.agent, action=program)
                tool = self._build_tool_def(name, path, self._program_tool(agent, program))
                tools.append(tool)
            except ValueError:
                logger.warning(f"unable to build tool {path}", exc_info=True)

        return tools

    def _build_tool_def(self, name, path, tool_call):
        return EidosHandler(
            name=name,
            description=lambda a, b: self._description(path),
            input_model_fn=lambda a, b: self._body_model(path),
            output_model_fn=lambda a, b: Any,
            fn=tool_call,
            extra={},
        )

    def _body_model(self, path):
        body = self._openapi_json["paths"][path]["post"]['requestBody']
        if body and "application/json" not in body["content"]:
            raise ValueError(f"Agent action at {path} does not support application/json")
        json_schema = body["content"]["application/json"]["schema"] if body else dict(type="object", properties={})
        return schema_to_model(dict(type="object", properties=dict(body=json_schema)), "Input")

    def _description(self, path):
        description = self._openapi_json["paths"][path]["post"].get("description", "")
        if not description:
            self.logger.warning(f"Agent program at {path} does not have a description. LLM may not use it properly")
        return description

    # needs to be under 64 characters
    def _name(self, agent, action="", process_id=""):
        agent = agent[:15]
        process_id = process_id[:25]
        process_id = "_" + process_id if process_id else ""
        action = action[:15]
        action = "_" + action if action else ""
        return self.spec.tool_prefix + "_" + agent + process_id + action

    def _program_tool(self, agent, program):
        return self._tool_call(lambda body: self._machine.agent(agent).program(program, body))

    def _process_tool(self, agent, process_id, action):
        return self._tool_call(lambda body: self._machine.agent(agent).process(process_id).action(action, body))

    @staticmethod
    def _tool_call(fn):
        async def _fn(_self, body):
            resp = await fn(body)
            return resp.model_dump()

        return _fn

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
    async with ContextualClientSession() as session:
        async with session.post(url, json=args) as resp:
            return await resp.json()


async def _get_openapi_schema(url):
    async with ContextualClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()
