from pydantic import BaseModel
from typing import List, Any, Dict, AsyncIterator

from eidolon_ai_client.client import Machine, Agent, AgentResponseIterator
from eidolon_ai_sdk.cpu.agent_call_history import AgentCallHistory
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit
from eidolon_ai_client.events import StreamEvent
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class AgentsLogicUnitSpec(BaseModel):
    tool_prefix: str = "convo"
    agents: List[str]


class AgentsLogicUnit(Specable[AgentsLogicUnitSpec], LogicUnit):
    _machine_schemas: Dict[str, dict]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._machine_schemas = {}

    async def build_tools(self, call_context: CallContext) -> List[FnHandler]:
        tools = await self.build_program_tools(call_context)
        call_history = await AgentCallHistory.get_agent_state(call_context.process_id, call_context.thread_id)
        for call in call_history:
            for action in call.available_actions:
                context_ = await self.build_action_tool(
                    call.machine, call.agent, action, call.remote_process_id, call_context
                )
                if context_:
                    tools.append(context_)

        return tools

    async def clone_thread(self, old_context: CallContext, new_context: CallContext):
        call_history = await AgentCallHistory.get_agent_state(old_context.process_id, old_context.thread_id)
        for call in call_history:
            await AgentCallHistory(
                parent_process_id=new_context.process_id,
                parent_thread_id=new_context.thread_id,
                machine=call.machine,
                agent=call.agent,
                remote_process_id=call.remote_process_id,
                state=call.state,
                available_actions=call.available_actions,
            ).upsert()

    async def _get_schema(self, machine: str) -> dict:
        if machine not in self._machine_schemas:
            self._machine_schemas[machine] = await Machine(machine=machine).get_schema()
        return self._machine_schemas[machine]

    async def build_action_tool(
        self, machine: str, agent: str, action: str, remote_process_id: str, call_context: CallContext
    ):
        agent_client = Agent.get(agent)
        path = f"/processes/{{process_id}}/agent/{agent}/actions/{action}"
        machine_schema = await self._get_schema(machine)
        endpoint_schema = machine_schema["paths"][path]["post"]
        try:
            name = self._name(agent, action=action)
            tool = self._build_tool_def(
                agent,
                action,
                name,
                endpoint_schema,
                self._process_tool(agent_client, action, remote_process_id, call_context),
            )
            return tool
        except ValueError:
            logger.warning(f"unable to build tool {path}", exc_info=True)

    async def build_program_tools(self, call_context: CallContext):
        tools = []
        for agent in self.spec.agents:
            agent_client = Agent.get(agent)
            machine_schema = await self._get_schema(agent_client.machine)
            for action in await agent_client.programs():
                path = f"/processes/{{process_id}}/agent/{agent}/actions/{action}"
                try:
                    name = self._name(agent, action=action)
                    tool = self._build_tool_def(
                        agent,
                        action,
                        name,
                        machine_schema["paths"][path]["post"],
                        self._program_tool(agent_client, action, call_context),
                    )
                    tools.append(tool)
                except ValueError:
                    logger.warning(f"unable to build tool {path}", exc_info=True)
        return tools

    def _build_tool_def(self, agent, operation, name, endpoint_schema, tool_call):
        description = self._description(endpoint_schema, name)
        model = self._body_model(endpoint_schema, name)
        return FnHandler(
            name=name,
            description=lambda a, b: description,
            input_model_fn=lambda a, b: model,
            output_model_fn=lambda a, b: Any,
            fn=tool_call,
            extra={
                "title": agent,
                "sub_title": operation,
                "agent_call": True,
            },
        )

    @staticmethod
    def _body_model(endpoint_schema, name):
        body = endpoint_schema.get("requestBody")
        if not body:
            json_schema = dict(type="object", properties={})
            return schema_to_model(dict(type="object", properties=dict(body=json_schema)), "Input")
        elif "application/json" in body["content"]:
            json_schema = body["content"]["application/json"]["schema"]
            return schema_to_model(dict(type="object", properties=dict(body=json_schema)), "Input")
        elif "text/plain" in body["content"]:
            return schema_to_model(dict(type="object", properties=dict(body=dict(type="string"))), "Input")
        else:
            raise ValueError(f"Agent action at {name} does not support text/plain or application/json")

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

    # todo, this needs to create history record before iterating
    def _program_tool(self, agent: Agent, program: str, call_context: CallContext):
        async def fn(_self, body):
            async for event in RecordAgentResponseIterator(
                (await agent.create_process()).stream_action(program, body),
                call_context.process_id,
                call_context.thread_id,
            ):
                yield event

        return fn

    # todo, this needs to create history record before iterating
    def _process_tool(self, agent: Agent, action: str, process_id: str, call_context: CallContext):
        def fn(_self, body):
            return RecordAgentResponseIterator(
                agent.process(process_id).stream_action(action, body), call_context.process_id, call_context.thread_id
            )

        return fn


# todo, it would be nice to work this into the client automatically
class RecordAgentResponseIterator(AgentResponseIterator):
    parent_process_id: str
    parent_thread_id: str

    def __init__(self, data: AsyncIterator[StreamEvent], parent_process_id: str, parent_thread_id: str):
        super().__init__(data)
        self.parent_process_id = parent_process_id
        self.parent_thread_id = parent_thread_id

    async def iteration_complete(self):
        call_data = AgentCallHistory(
            parent_process_id=self.parent_process_id,
            parent_thread_id=self.parent_thread_id,
            machine=self.machine,
            agent=self.agent,
            remote_process_id=self.process_id,
            state=self.state,
            available_actions=self.available_actions,
        )
        await call_data.upsert()

        return await super().iteration_complete()
