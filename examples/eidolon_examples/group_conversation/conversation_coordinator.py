import asyncio
import random
from fastapi import Body
from pydantic import BaseModel, TypeAdapter, Field
from typing import Tuple, List, Annotated, TypeVar, Dict

from eidolon_examples.group_conversation.conversation_agent import (
    SpeakResult,
    ThoughtResult,
    CharacterThought,
    StatementsForAgent,
    Statement,
)
from eidos_sdk.agent.agent import register_program, AgentState, register_action
from eidos_sdk.agent.client import Machine
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.system.reference_model import Specable


class NextTurn(BaseModel):
    num_turns: int = Field(1, description="The number of turns to take.")


class StartConversation(BaseModel):
    topic: str
    num_concurrent_conversations: int = 1


class ConversationState(BaseModel):
    process_id: str
    agent_pids: List[Tuple[str, str]]
    topic: str
    num_concurrent_conversations: int


class ConversationCoordinatorSpec(BaseModel):
    agents: list[str]


T = TypeVar("T")


class InnerMonologue(BaseModel):
    agent_name: str
    statement: str


class ConversationCoordinator(Specable[ConversationCoordinatorSpec]):
    @register_program()
    async def start_conversation(
        self,
        process_id,
        topic: Annotated[StartConversation, Body(description="The topic of the new conversation", embed=True)],
    ) -> AgentState[str]:
        """
        Called to start the conversation. Every user will get a turn in each turn of the conversation.
        """
        # start conversation with every agent
        agent_pids = []
        for agent in self.spec.agents:
            response = await Machine().agent(agent).program("start_conversation", {"topic": topic.topic})
            agent_pid = response.process_id
            agent_pids.append((agent, agent_pid))
            await AgentOS.symbolic_memory.insert_one(
                "conversation_coordinator_messages",
                {"process_id": process_id, "agent_name": agent, "desire_to_speak": 0.5},
            )

        # record the pids of the agents with our process_id in memory
        await AgentOS.symbolic_memory.insert_one(
            "conversation_coordinator",
            ConversationState(
                process_id=process_id,
                agent_pids=agent_pids,
                topic=topic.topic,
                num_concurrent_conversations=topic.num_concurrent_conversations,
            ).model_dump(),
        )

        return AgentState(name="idle", data="Agents started. Waiting for first turn...")

    async def _restore_state(self, process_id) -> ConversationState:
        result = await AgentOS.symbolic_memory.find_one("conversation_coordinator", {"process_id": process_id})
        return ConversationState.model_validate(result)

    async def _record_single(self, agent_name, agent_pid, statements: List[Statement]):
        thought_response = (
            await Machine()
            .agent(agent_name)
            .process(agent_pid)
            .action("record_statement", {"statements": StatementsForAgent(statements=statements).model_dump()})
        )
        thought = ThoughtResult.model_validate(thought_response.data)
        await AgentOS.symbolic_memory.upsert_one(
            "conversation_coordinator_messages",
            {"desire_to_speak": thought.desire_to_speak},
            {"process_id": agent_pid, "agent_name": agent_name},
        )
        return agent_name, thought.desire_to_speak

    async def record_statements(self, conversation_state, statements_to_record: List[Statement]):
        acc = []
        for r_agent_name, r_agent_pid in conversation_state.agent_pids:
            acc.append(self._record_single(r_agent_name, r_agent_pid, statements_to_record))
        return await asyncio.gather(*acc)

    async def _restore_message(self, process_id, conversation_state: ConversationState):
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
        return agent_responses

    @register_action("idle")
    async def add_inner_monologue(
        self, process_id, monologue: Annotated[InnerMonologue, Body(description="The thought to add", embed=True)]
    ) -> AgentState[str]:
        conversation_state = await self._restore_state(process_id)
        for agent_name, state_agent_pid in conversation_state.agent_pids:
            if agent_name == monologue.agent_name:
                await self._record_single(
                    agent_name,
                    state_agent_pid,
                    [Statement(speaker=monologue.agent_name, text=monologue.statement, voice_level=0.5)],
                )

        return AgentState(name="idle", data="Thought recorded")

    @register_action("idle")
    async def get_thoughts(self, process_id) -> AgentState[Dict[str, List[CharacterThought]]]:
        conversation_state = await self._restore_state(process_id)
        all_characters = [agent_name for agent_name, _ in conversation_state.agent_pids]
        thoughts = {}
        acc = []
        for agent_name, state_agent_pid in conversation_state.agent_pids:
            acc.append(
                Machine()
                .agent(agent_name)
                .process(state_agent_pid)
                .action("describe_thoughts", {"people": all_characters})
            )

        results = await asyncio.gather(*acc)
        for agent_name, result in zip(all_characters, results):
            character_thoughts = TypeAdapter(List[CharacterThought]).validate_python(result.data)
            thoughts[agent_name] = character_thoughts

        return AgentState(name="idle", data=thoughts)

    @register_action("idle")
    async def next_turn(self, process_id, obj: NextTurn) -> AgentState[str]:
        """
        Called to start the next turn of the conversation.
        """
        # get the pids of the agents with our process_id in memory
        conversation_state = await self._restore_state(process_id)

        agent_responses = await self._restore_message(process_id, conversation_state)

        async def let_agent_speak(agent_name, agent_pid):
            response = await Machine().agent(agent_name).process(agent_pid).action("speak", {})
            agent_response = SpeakResult.model_validate(response.data)

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
            agent_responses[agent_name]["desire_to_speak"] = agent_response.desire_to_speak
            return output, Statement(
                speaker=agent_name, text=agent_response.response, voice_level=agent_response.voice_level
            )

        method_output = ""
        for _ in range(obj.num_turns):
            speaking = {}
            for _ in range(min(conversation_state.num_concurrent_conversations, len(conversation_state.agent_pids))):
                weighted_agents = [
                    ((a_name, agent_pid), agent_responses[a_name]["desire_to_speak"])
                    for a_name, agent_pid in conversation_state.agent_pids
                    if a_name not in speaking
                ]
                agent_name, agent_pid = self.weighted_random_choice(weighted_agents)
                speaking[agent_name] = agent_pid

            speeches = [let_agent_speak(agent_name, agent_pid) for agent_name, agent_pid in speaking.items()]
            statements = await asyncio.gather(*speeches)

            agents_desire = await self.record_statements(conversation_state, [statement for _, statement in statements])
            for agent_name, desire_to_speak in agents_desire:
                agent_responses[agent_name]["desire_to_speak"] = desire_to_speak
            for output, _ in statements:
                method_output += output

        return AgentState(name="idle", data=method_output)

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
