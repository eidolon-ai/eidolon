import asyncio
import random
from fastapi import Body
from pydantic import BaseModel, TypeAdapter
from typing import Tuple, List, Annotated, TypeVar, Dict

from eidolon_examples.group_conversation.conversation_agent import SpeakResult, ThoughtResult, CharacterThought
from eidos_sdk.agent.agent import register_program, AgentState, register_action
from eidos_sdk.agent.client import Machine
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.system.reference_model import Specable


class ConversationState(BaseModel):
    process_id: str
    agent_pids: List[Tuple[str, str]]
    topic: str


class ConversationCoordinatorSpec(BaseModel):
    agents: list[str]


T = TypeVar("T")


class InnerMonologue(BaseModel):
    agent_name: str
    statement: str


class ConversationCoordinator(Specable[ConversationCoordinatorSpec]):
    @register_program()
    async def start_conversation(self, process_id, topic: Annotated[str, Body(description="The topic of the new conversation", embed=True)]) -> AgentState[str]:
        """
        Called to start the conversation. Every user will get a turn in each turn of the conversation.
        """
        # start conversation with every agent
        agent_pids = []
        for agent in self.spec.agents:
            response = await Machine().agent(agent).program("start_conversation", {"topic": topic})
            agent_pid = response.process_id
            agent_pids.append((agent, agent_pid))
            await AgentOS.symbolic_memory.insert_one("conversation_coordinator_messages",
                                                     {"process_id": process_id, "agent_name": agent, "desire_to_speak": 0.5})

        # record the pids of the agents with our process_id in memory
        await AgentOS.symbolic_memory.insert_one("conversation_coordinator", ConversationState(process_id=process_id, agent_pids=agent_pids, topic=topic).model_dump())

        return AgentState(name="idle", data="Agents started. Waiting for first turn...")

    @register_action("idle")
    async def add_inner_monologue(self, process_id, monologue: Annotated[InnerMonologue, Body(description="The thought to add", embed=True)]) -> AgentState[str]:
        result = await AgentOS.symbolic_memory.find_one("conversation_coordinator", {"process_id": process_id})
        conversation_state = ConversationState.model_validate(result)
        for agent_name, state_agent_pid in conversation_state.agent_pids:
            if agent_name == monologue.agent_name:
                thought_response = await Machine().agent(agent_name).process(state_agent_pid).action(
                    "record_statement", {"statement": {"speaker": agent_name, "text": monologue.statement, "voice_level": 0.5}}
                )
                thought = ThoughtResult.model_validate(thought_response.data)
                await AgentOS.symbolic_memory.upsert_one("conversation_coordinator_messages",
                                                         {"desire_to_speak": thought.desire_to_speak},
                                                         {"process_id": process_id, "agent_name": agent_name})

        return AgentState(name="idle", data="Thought recorded")

    @register_action("idle")
    async def get_thoughts(self, process_id) -> AgentState[Dict[str, List[CharacterThought]]]:
        result = await AgentOS.symbolic_memory.find_one("conversation_coordinator", {"process_id": process_id})
        conversation_state = ConversationState.model_validate(result)
        all_characters = [agent_name for agent_name, _ in conversation_state.agent_pids]
        thoughts = {}
        acc = []
        for agent_name, state_agent_pid in conversation_state.agent_pids:
            acc.append(Machine().agent(agent_name).process(state_agent_pid).action("describe_thoughts", {"people": all_characters}))

        results = await asyncio.gather(*acc)
        for agent_name, result in zip(all_characters, results):
            character_thoughts = TypeAdapter(List[CharacterThought]).validate_python(result.data)
            thoughts[agent_name] = character_thoughts

        return AgentState(name="idle", data=thoughts)

    @register_action("idle")
    async def next_turn(self, process_id, num_turns: Annotated[int, Body(description="The number of turns to take", embed=True)]) -> AgentState[str]:
        """
        Called to start the next turn of the conversation.
        """
        # get the pids of the agents with our process_id in memory
        result = await AgentOS.symbolic_memory.find_one("conversation_coordinator", {"process_id": process_id})
        conversation_state = ConversationState.model_validate(result)

        results = AgentOS.symbolic_memory.find("conversation_coordinator_messages", {"process_id": process_id})

        agent_responses = {}
        for agent_name, _ in conversation_state.agent_pids:
            async for result in results:
                if result["agent_name"] == agent_name:
                    agent_responses[agent_name] = {
                        "desire_to_speak": result["desire_to_speak"],
                    }
                    break
            if agent_name not in agent_responses:
                agent_responses[agent_name] = {
                    "desire_to_speak": 0.5,
                }

        async def record_single(state_agent_name, state_agent_pid, speaker, statement, volume_level):
            thought_response = await Machine().agent(state_agent_name).process(state_agent_pid).action(
                "record_statement", {"statement": {"speaker": speaker, "text": statement, "voice_level": volume_level}}
            )
            thought = ThoughtResult.model_validate(thought_response.data)
            agent_responses[state_agent_name]["desire_to_speak"] = thought.desire_to_speak

        async def record_statements(speaker, volume_level, statement):
            acc = []
            for state_agent_name, state_agent_pid in conversation_state.agent_pids:
                if state_agent_name != speaker:
                    acc.append(record_single(state_agent_name, state_agent_pid, speaker, statement, volume_level))
            await asyncio.gather(*acc)

        output = ""
        for _ in range(num_turns):
            weighted_agents = [((agent_name, agent_pid), agent_responses[agent_name]["desire_to_speak"]) for agent_name, agent_pid in conversation_state.agent_pids]
            agent_name, agent_pid = self.weighted_random_choice(weighted_agents)
            response = await Machine().agent(agent_name).process(agent_pid).action("speak", {})
            agent_response = SpeakResult.model_validate(response.data)
            agent_responses[agent_name]["desire_to_speak"] = agent_response.desire_to_speak
            await record_statements(agent_name, agent_response.desire_to_speak, agent_response.response)
            if agent_response.voice_level < 0.25:
                color = "green"
            elif agent_response.voice_level < 0.5:
                color = "yellow"
            elif agent_response.voice_level < 0.75:
                color = "orange"
            else:
                color = "red"

            output += f"**{agent_name}**({agent_response.mood()}){agent_response.emoji}: <span color='{color}'>{agent_response.response}</span>\n\n"

            for agent_name, _ in conversation_state.agent_pids:
                await AgentOS.symbolic_memory.upsert_one("conversation_coordinator_messages",
                                                         {"desire_to_speak": agent_responses[agent_name]["desire_to_speak"]},
                                                         {"process_id": process_id, "agent_name": agent_name})

        return AgentState(name="idle", data=output)

    @staticmethod
    def weighted_random_choice(items: List[Tuple[T, float]]) -> T:
        total_weight = sum(weight for item, weight in items)
        random_num = random.uniform(0, total_weight)
        print(f"items: {items}")
        print(f"total_weight: {total_weight}, random_num: {random_num}")

        current_sum = 0
        for item, weight in items:
            current_sum += weight
            if current_sum >= random_num:
                print(f"selecting {item}")
                return item
