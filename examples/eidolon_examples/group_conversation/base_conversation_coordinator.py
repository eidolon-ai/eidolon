import random
from abc import ABC
from aiostream import stream
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Tuple, List, TypeVar, Dict, Any, AsyncIterator

from eidolon_examples.group_conversation.conversation_agent import (
    SpeakResult,
    ThoughtResult,
)
from eidos_sdk.agent.client import Machine
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.io.events import ObjectOutputEvent, AgentContextStartEvent, AgentContextEndEvent, StartAgentCallEvent, StreamEvent
from eidos_sdk.system.reference_model import Specable
from eidos_sdk.util.stream_collector import StringStreamCollector


class StartConversation(BaseModel):
    message: str
    max_num_concurrent_conversations: int = 1


class ConversationState(BaseModel):
    process_id: str
    agent_pids: List[Tuple[str, str]]  # agent_name, agent_pid
    start_conv_message: str
    max_num_concurrent_conversations: int


class InnerMonologue(BaseModel):
    agent_name: str
    statement: str


@dataclass
class Action:
    action_name: str
    args: Dict[str, Any]


T = TypeVar("T", bound=Any)


class BaseConversationCoordinatorSpec(BaseModel):
    agents: list[str]


class BaseConversationCoordinator(ABC, Specable[BaseConversationCoordinatorSpec]):
    def __init__(self, semantic_memory_prefix: str, **kwargs):
        super().__init__(**kwargs)
        self.semantic_memory_prefix = semantic_memory_prefix

    async def start_conversations(self, process_id, topic: StartConversation) -> AsyncIterator[StreamEvent]:
        """
        Called to start the conversations. Initializes the remote agents and starts the first turn.
        """

        # start conversation with every agent
        async for event in self._run_program_in_all_agents(process_id, "start_conversation", {"topic": topic.message}):
            yield event

    def add_inner_monologue(self, process_id, monologue: InnerMonologue) -> AsyncIterator[StreamEvent]:
        return self._run_action_in_agents(process_id, [monologue.agent_name], Action("add_inner_monologue", {"monologue": monologue}))

    def get_all_thoughts(self, process_id) -> AsyncIterator[StreamEvent]:
        return self._run_action_in_all_agents(process_id, Action("describe_thoughts", {"people": self.spec.agents}))

    async def speak_to_agents(self, process_id, statement: str, agents: List[str] = None, should_record=True) -> AsyncIterator[StreamEvent]:
        if not agents:
            agents = self.spec.agents

        collectors = {agent: StringStreamCollector() for agent in agents}
        async for event in self._run_action_in_agents(process_id, agents, Action("speak", {"message": statement})):
            if should_record and collectors.get(event.stream_context):
                collectors[event.stream_context].process_event(event)
            yield event

        if should_record:
            statements = ""
            for agent_name, collector in collectors.items():
                statement = collector.contents or "<no response>"
                statements += "**" + agent_name + "**: " + statement + "\n\n"
            async for event in self.record_statements(process_id, statements, agents=agents):
                yield event

    async def record_statements(self, process_id, statements: str, agents: List[str] = None):
        if not agents:
            agents = self.spec.agents

        conversation_state = await self._restore_state(process_id)
        agent_pids = {agent_name: agent_pid for agent_name, agent_pid in conversation_state.agent_pids if agent_name in agents}
        async for event in self._run_action_in_agents(process_id=process_id, agents=agents, action=Action("record_statement", {"statements": statements})):
            if isinstance(event, ObjectOutputEvent) and event.stream_context in agents:
                thought = ThoughtResult.model_validate(event.content)
                agent_pid = agent_pids[event.stream_context]
                await AgentOS.symbolic_memory.upsert_one(
                    "conversation_coordinator_messages",
                    {"desire_to_speak": thought.desire_to_speak},
                    {"process_id": agent_pid, "agent_name": event.stream_context},
                )
            yield event

    # Helper functions

    def _run_program_in_all_agents(self, our_process_id, program_name: str, args: Dict[str, Any]):
        return self._run_program_in_agents(our_process_id, program_name, self.spec.agents, args)

    async def _run_program_in_agents(
            self,
            our_process_id,
            program_name: str,
            agents: List[str],
            args: Dict[str, Any],
    ):
        async def run_one(agent_name):
            yield AgentContextStartEvent(context_id=agent_name)
            try:
                async for a_event in Machine().agent(agent_name).stream_program(program_name, args):
                    a_event.stream_context = agent_name
                    yield a_event
            finally:
                yield AgentContextEndEvent(context_id=agent_name)

        tasks = [run_one(agent) for agent in agents]
        combined_calls = stream.merge(tasks[0], *tasks[1:])
        agent_pids = []
        async for event in combined_calls:
            if isinstance(event, StartAgentCallEvent) and event.stream_context in agents:
                agent_pids.append((event.agent_name, event.process_id))
            yield event

        conv_state = ConversationState(
            process_id=our_process_id,
            agent_pids=agent_pids,
            start_conv_message="",
            max_num_concurrent_conversations=len(self.spec.agents),
        )
        # record the pids of the agents with our process_id in memory
        await AgentOS.symbolic_memory.insert_one("conversation_coordinator", conv_state.model_dump())

    def _run_action_in_all_agents(self, process_id, action: Action):
        return self._run_action_in_agents(process_id, self.spec.agents, action)

    async def _run_action_in_agents(self, process_id, agents: List[str], action: Action):
        async def run_one(agent_name: str, agent_pid: str) -> T:
            yield AgentContextStartEvent(context_id=agent_name)
            try:
                async for a_event in (Machine().agent(agent_name).stream_action(action.action_name, agent_pid, action.args)):
                    a_event.stream_context = agent_name
                    yield a_event
            finally:
                yield AgentContextEndEvent(context_id=agent_name)

        conversation_state = await self._restore_state(process_id)
        tasks = []
        for name, pid in conversation_state.agent_pids:
            if name in agents:
                tasks.append(run_one(name, pid))

        combined_calls = stream.merge(tasks[0], *tasks[1:])
        async for event in combined_calls:
            yield event

    async def _restore_state(self, process_id) -> ConversationState:
        result = await AgentOS.symbolic_memory.find_one("conversation_coordinator", {"process_id": process_id})
        return ConversationState.model_validate(result)

    async def _restore_message(self, process_id, agents: List[str]) -> Dict[str, float]:
        results = AgentOS.symbolic_memory.find("conversation_coordinator_messages", {"process_id": process_id})
        agent_responses = {}
        for agent_name in agents:
            async for result in results:
                if result["agent_name"] == agent_name:
                    agent_responses[agent_name] = result["desire_to_speak"]
                    break
            if agent_name not in agent_responses:
                agent_responses[agent_name] = (0.5,)
        return agent_responses

    def format_response(self, agent_name: str, agent_response: SpeakResult):
        if agent_response.voice_level < 0.25:
            color = "green"
        elif agent_response.voice_level < 0.5:
            color = "yellow"
        elif agent_response.voice_level < 0.75:
            color = "orange"
        else:
            color = "red"

        output = f"**{agent_name}**💭💭💭: <span color='gray'>{agent_response.inner_dialog}</span>\n\n"
        output += f"**{agent_name}**{agent_response.emoji}: <span color='{color}'>{agent_response.response}</span>\n\n"
        return output

    def choose_agents_to_speak(self, num_concurrent_conversations: int, desire_to_speak: Dict[str, float]) -> List[str]:
        agents_to_speak = []
        for _ in range(min(num_concurrent_conversations, len(self.spec.agents))):
            weighted_agents = [
                (a_name, desire_to_speak[a_name]) for a_name in self.spec.agents if a_name not in agents_to_speak
            ]

            total_weight = sum(weight for item, weight in weighted_agents)
            random_num = random.uniform(0, total_weight)
            print(f"items: {weighted_agents}")
            print(f"total_weight: {total_weight}, random_num: {random_num}")

            current_sum = 0
            for item, weight in weighted_agents:
                current_sum += weight
                if current_sum >= random_num:
                    print(f"selecting {item}")
                    agents_to_speak.append(item)
                    break
        return agents_to_speak
