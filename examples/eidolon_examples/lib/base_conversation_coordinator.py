import asyncio

import random
from abc import ABC
from aiostream import stream
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Tuple, List, TypeVar, Dict, Any, cast

from eidolon_ai_client.client import Machine
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_client.events import (
    EndStreamContextEvent, StartStreamContextEvent,
)
from eidolon_ai_sdk.system.reference_model import Specable


class ConversationState(BaseModel):
    process_id: str
    agent_pids: List[Tuple[str, str]]  # agent_name, agent_pid
    start_conv_message: str
    max_num_concurrent_conversations: int


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

    def start_conversation(self, process_id: str):
        return self._start_all_agent_processes(process_id)

    def speak_to_all_agents(self, process_id: str, message: str):
        return self._run_action_in_all_agents_stream(process_id, Action(action_name="speak", args={"message": message}))

    def speak_to_agents(self, process_id: str, agents: List[str], message: str):
        # todo -- this needs to record the response from each agent and send it to all other agents
        return self._run_action_in_agents_stream(process_id, agents, Action(action_name="speak", args={"message": message}))

    def get_all_agent_thoughts(self, process_id: str, message: str):
        return self._run_action_in_all_agents(process_id, Action(action_name="get_thoughts", args={"message": message}))

    def ping_all_agents(self, process_id: str):
        return self._run_action_in_all_agents(process_id, Action(action_name="ping", args={}))

    # Helper methods #
    def _start_all_agent_processes(self, our_process_id):
        return self._start_agent_processes(our_process_id, self.spec.agents)

    async def _start_agent_processes(
        self,
        our_process_id,
        agents: List[str],
    ):
        async def run_one(agent_name):
            return await Machine().agent(agent_name).create_process()

        tasks = [await run_one(agent) for agent in agents]
        agent_pids = [(task.agent, task.process_id) for task in tasks]
        conv_state = ConversationState(
            process_id=our_process_id,
            agent_pids=agent_pids,
            start_conv_message="",
            max_num_concurrent_conversations=len(self.spec.agents),
        )
        # record the pids of the agents with our process_id in memory
        await AgentOS.symbolic_memory.insert_one("conversation_coordinator", conv_state.model_dump())

    def _run_action_in_all_agents_stream(self, process_id, action: Action):
        return self._run_action_in_agents_stream(process_id, self.spec.agents, action)

    async def _run_action_in_agents_stream(self, process_id, agents: List[str], action: Action):
        async def run_one(agent_name: str, agent_pid: str) -> T:
            yield StartStreamContextEvent(context_id=agent_name)
            try:
                async for a_event in (
                    Machine().agent(agent_name).stream_action(action.action_name, agent_pid, action.args)
                ):
                    a_event.stream_context = agent_name
                    yield a_event
            finally:
                yield EndStreamContextEvent(context_id=agent_name)

        conversation_state = await self._restore_state(process_id)
        tasks = []
        for name, pid in conversation_state.agent_pids:
            if name in agents:
                tasks.append(run_one(name, pid))

        combined_calls = stream.merge(tasks[0], *tasks[1:])
        async for event in combined_calls:
            yield event

    def _run_action_in_all_agents(self, process_id, action: Action):
        return self._run_action_in_agents(process_id, self.spec.agents, action)

    async def _run_action_in_agents(self, process_id, agents: List[str], action: Action) -> List[Tuple[str, T]]:
        async def run_one(agent_name: str, agent_pid: str) -> Tuple[str, T]:
            return agent_name, await Machine().agent(agent_name).process(agent_pid).action(action.action_name, action.args)

        conversation_state = await self._restore_state(process_id)
        tasks = []
        for name, pid in conversation_state.agent_pids:
            if name in agents:
                tasks.append(run_one(name, pid))

        return cast(List[Tuple[str, T]], await asyncio.gather(*tasks))

    async def _restore_state(self, process_id) -> ConversationState:
        result = await AgentOS.symbolic_memory.find_one("conversation_coordinator", {"process_id": process_id})
        return ConversationState.model_validate(result)


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
