import json
from typing import List, Any, Dict

from pydantic import BaseModel, ValidationError

from eidos_sdk.agent.client import Machine, ProcessStatus, Agent, Process
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
    tool_prefix: str = "convo"
    agents: List[str]


class ConversationalLogicUnit(LogicUnit, Specable[ConversationalSpec]):
    _machine_schemas: Dict[str, dict]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self._machine_schemas = {}

    async def _get_schema(self, machine: str) -> dict:
        if machine not in self._machine_schemas:
            self._machine_schemas[machine] = await Machine(machine=machine).get_schema()
        return self._machine_schemas[machine]

    async def build_tools(self, conversation: List[LLMMessage]) -> List[EidosHandler]:
        tools = []

        for agent in self.spec.agents:
            agent_client = Agent.get(agent)
            agent = agent_client.agent

            prefix = f"/agents/{agent}/programs/"
            machine_schema = await self._get_schema(agent_client.machine)
            for path in filter(lambda p: p.startswith(prefix), machine_schema["paths"].keys()):
                try:
                    program = path.removeprefix(prefix)
                    name = self._name(agent, action=program)
                    tool = self._build_tool_def(
                        name, machine_schema["paths"][path]["post"], self._program_tool(agent_client, program)
                    )
                    tools.append(tool)
                except ValueError:
                    logger.warning(f"unable to build tool {path}", exc_info=True)

        # in case new spec removes ability to talk to agents, existing agents should not be able to continue talking to them
        allowed_agents = {(ac.machine, ac.agent) for ac in (Agent.get(a) for a in self.spec.agents)}
        processes: List[ProcessStatus] = []
        for message in conversation:
            if isinstance(message, ToolResponseMessage):
                try:
                    process = ProcessStatus.model_validate(json.loads(message.result))
                    if (process.machine, process.agent) in allowed_agents:
                        processes.append(process)
                except ValidationError:
                    logger.warning("unable to parse conversation response, skipping", exc_info=True)

        # newer process state should override older process state if there are multiple calls
        for action, process in ((a, r) for r in processes for a in r.available_actions):
            path = f"/agents/{process.agent}/processes/{{process_id}}/actions/{action}"
            machine_schema = await self._get_schema(process.machine)
            endpoint_schema = machine_schema["paths"][path]["post"]
            try:
                name = self._name(process.agent, action=action)
                tool = self._build_tool_def(name, endpoint_schema, self._process_tool(process, action))
                tools.append(tool)
            except ValueError:
                logger.warning(f"unable to build tool {path}", exc_info=True)

        return tools

    def _build_tool_def(self, name, endpoint_schema, tool_call):
        description = self._description(endpoint_schema, name)
        model = self._body_model(endpoint_schema, name)
        return EidosHandler(
            name=name,
            description=lambda a, b: description,
            input_model_fn=lambda a, b: model,
            output_model_fn=lambda a, b: Any,
            fn=tool_call,
            extra={},
        )

    @staticmethod
    def _body_model(endpoint_schema, name):
        body = endpoint_schema.get("requestBody")
        if body and "application/json" not in body["content"]:
            raise ValueError(f"Agent action at {name} does not support application/json")
        json_schema = body["content"]["application/json"]["schema"] if body else dict(type="object", properties={})
        return schema_to_model(dict(type="object", properties=dict(body=json_schema)), "Input")

    @staticmethod
    def _description(endpoint_schema, name):
        description = endpoint_schema.get("description", "")
        if not description:
            logger.warning(f"Agent program at {name} does not have a description. LLM may not use it properly")
        return description

    # needs to be under 64 characters
    def _name(self, agent, action="", process_id=""):
        agent = agent[:15]
        process_id = process_id[:25]
        process_id = "_" + process_id if process_id else ""
        action = action[:15]
        action = "_" + action if action else ""
        return self.spec.tool_prefix + "_" + agent + process_id + action

    def _program_tool(self, agent: Agent, program):
        return self._tool_call(lambda body: agent.program(program, body))

    def _process_tool(self, process: Process, action):
        return self._tool_call(lambda body: process.action(action, body))

    @staticmethod
    def _tool_call(fn):
        async def _fn(_self, body):
            resp = await fn(body)
            return resp.model_dump()

        return _fn
