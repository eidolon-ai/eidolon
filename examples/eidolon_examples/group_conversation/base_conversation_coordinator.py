import asyncio
import random
from abc import ABC
from dataclasses import dataclass
from pydantic import BaseModel, TypeAdapter
from typing import Tuple, List, TypeVar, Dict, Callable, Any, AsyncGenerator, Union

from eidolon_examples.group_conversation.conversation_agent import SpeakResult, ThoughtResult, CharacterThought, StatementsForAgent, Statement
from eidos_sdk.agent.client import Machine
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.system.reference_model import Specable


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

    async def start_conversations(
            self, process_id, topic: StartConversation
    ) -> str:
        """
        Called to start the conversations. Initializes the remote agents and starts the first turn.
        """

        # start conversation with every agent
        async def fn(_agent_name):
            yield {"topic": topic.message}

        messages = await self._run_program_in_all_agents(process_id, "start_conversation", fn)

        return "\n".join(messages)

    async def add_inner_monologue(self, process_id, monologue: InnerMonologue):
        async def fn(_agent_name, _agent_pid):
            yield Action("add_inner_monologue", {"monologue": monologue})

        await self._run_action_in_agents(process_id, [monologue.agent_name], fn)

    async def get_all_thoughts(self, process_id) -> List[Tuple[str, List[CharacterThought]]]:
        async def fn(agent_name, _agent_pid):
            result = yield Action("describe_thoughts", {"people": self.spec.agents})
            character_thoughts = TypeAdapter(List[CharacterThought]).validate_python(result.data)
            yield agent_name, character_thoughts

        return await self._run_action_in_all_agents(process_id, fn=fn)

    async def speak_to_agents(self, process_id, statement: str, agents: List[str] = None, parallel=True, should_record=True) -> List[Tuple[str, SpeakResult]]:
        if not agents:
            agents = self.spec.agents

        agent_responses = await self._restore_message(process_id, self.spec.agents)

        async def let_agent_speak(a_name: str, _agent_pid: str):
            response = yield Action("speak", {"message": statement})
            agent_response = SpeakResult.model_validate(response)
            yield a_name, agent_response

        agents_to_speak = agents
        statements = await self._run_action_in_agents(process_id, agents_to_speak, let_agent_speak)

        if should_record:
            agents_desire = await self.record_speak_results(process_id, statements, agents=agents)
            for agent_name, desire_to_speak in agents_desire:
                agent_responses[agent_name] = desire_to_speak

        return statements

    async def group_speak(self, process_id, statement: str, agents: List[str] = None, parallel=True, should_record=True) -> List[Tuple[str, SpeakResult]]:
        if not agents:
            agents = self.spec.agents

        agent_responses = await self._restore_message(process_id, self.spec.agents)

        async def let_agent_speak(a_name: str, _agent_pid: str):
            response = yield Action("speak_amongst_group", {"message": {"message": statement, "group": agents}})
            agent_response = SpeakResult.model_validate(response)
            yield a_name, agent_response

        agents_to_speak = agents
        statements = await self._run_action_in_agents(process_id, agents_to_speak, let_agent_speak)

        if should_record:
            agents_desire = await self.record_speak_results(process_id, statements)
            for agent_name, desire_to_speak in agents_desire:
                agent_responses[agent_name] = desire_to_speak

        return statements

    async def let_agents_speak(self, process_id, statement: str, num_turns: int, num_concurrent_conversations: int) -> List[List[Tuple[str, SpeakResult]]]:
        conversation_state = await self._restore_state(process_id)

        agent_responses = await self._restore_message(process_id, self.spec.agents)

        async def let_agent_speak(a_name: str, _agent_pid: str):
            response = yield Action("speak", {"message": statement})
            agent_response = SpeakResult.model_validate(response.data)
            yield a_name, agent_response

        speeches = []
        for _ in range(num_turns):
            agents_to_speak = self.choose_agents_to_speak(num_concurrent_conversations, agent_responses)
            statements = await self._run_action_in_agents(process_id, agents_to_speak, let_agent_speak)

            agents_desire = await self.record_speak_results(conversation_state, statements)
            for agent_name, desire_to_speak in agents_desire:
                agent_responses[agent_name] = desire_to_speak

            speeches.append(statements)

        return speeches

    async def record_speak_results(self, process_id, speak_results: List[Tuple[str, SpeakResult]], agents: List[str] = None) -> List[Tuple[str, float]]:
        statements_to_record = []
        for speaker_name, speak_result in speak_results:
            statements_to_record.append(Statement(speaker=speaker_name, text=self.format_response(speaker_name, speak_result), voice_level=speak_result.voice_level))

        return await self.record_statements(process_id, statements_to_record, agents=agents)

    async def record_statements(self, process_id, statements_to_record: List[Statement], agents: List[str] = None):
        async def fn(agent_name, agent_pid):
            thought_response = yield Action("record_statement", {"statements": StatementsForAgent(statements=statements_to_record).model_dump()})
            thought = ThoughtResult.model_validate(thought_response)
            await AgentOS.symbolic_memory.upsert_one(
                "conversation_coordinator_messages",
                {"desire_to_speak": thought.desire_to_speak},
                {"process_id": agent_pid, "agent_name": agent_name},
            )
            yield agent_name, thought.desire_to_speak

        if not agents:
            agents = self.spec.agents

        return await self._run_action_in_agents(process_id=process_id, agents=agents, fn=fn)

    # Helper functions

    async def _run_program_in_all_agents(self, our_process_id, program_name: str, fn: Callable[[str], AsyncGenerator[Dict[str, Any], Any]]) -> List[T]:
        return await self._run_program_in_agents(our_process_id, program_name, self.spec.agents, fn)

    async def _run_program_in_agents(self, our_process_id, program_name: str, agents: List[str], fn: Callable[[str], AsyncGenerator[Dict[str, Any], Any]]) -> List[T]:
        async def run_one(agent_name):
            generator = fn(agent_name)
            retValue = None
            already_called = False
            async for args in generator:
                if already_called:
                    raise Exception("Function should only yield once")
                result = await Machine().agent(agent_name).program(program_name, args)
                try:
                    await generator.asend(result.data)
                except StopAsyncIteration:
                    pass
                retValue = agent_name, result.process_id

            return retValue

        tasks = [run_one(agent) for agent in agents]

        task_results = await asyncio.gather(*tasks)

        conv_state = ConversationState(process_id=our_process_id, agent_pids=task_results, start_conv_message="", max_num_concurrent_conversations=len(self.spec.agents))
        # record the pids of the agents with our process_id in memory
        await AgentOS.symbolic_memory.insert_one("conversation_coordinator", conv_state.model_dump())

        return [result for _, result in task_results]

    async def _run_action_in_all_agents(self, process_id, fn: Callable[[str, str], AsyncGenerator[Union[Action, T], Any]]) -> List[T]:
        return await self._run_action_in_agents(process_id, self.spec.agents, fn)

    async def _run_action_in_agents(self, process_id, agents: List[str], fn: Callable[[str, str], AsyncGenerator[Union[Action, T], Any]]) -> List[T]:
        async def run_one(agent_name: str, agent_pid: str) -> T:
            generator = fn(agent_name, agent_pid)
            retValue = None
            last_result_data = None
            while True:
                try:
                    action = await generator.asend(last_result_data)
                except StopAsyncIteration:
                    break
                if isinstance(action, Action):
                    result = await Machine().agent(agent_name).process(agent_pid).action(action.action_name, action.args)
                    last_result_data = result.data
                else:
                    retValue = action
                    break

            return retValue

        conversation_state = await self._restore_state(process_id)
        tasks = []
        for name, pid in conversation_state.agent_pids:
            if name in agents:
                tasks.append(run_one(name, pid))

        # noinspection PyTypeChecker
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                raise result
        return results

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
                agent_responses[agent_name] = 0.5,
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
        output += (
            f"**{agent_name}**{agent_response.emoji}: <span color='{color}'>{agent_response.response}</span>\n\n"
        )
        return output

    def choose_agents_to_speak(self, num_concurrent_conversations: int, desire_to_speak: Dict[str, float]) -> List[str]:
        agents_to_speak = []
        for _ in range(min(num_concurrent_conversations, len(self.spec.agents))):
            weighted_agents = [(a_name, desire_to_speak[a_name]) for a_name in self.spec.agents if a_name not in agents_to_speak]

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
