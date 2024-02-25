import random
import re
from typing import Tuple, List, Annotated, TypeVar

from fastapi import Body
from pydantic import BaseModel

from eidolon_ai_client.client import Agent, ProcessStatus
from eidolon_ai_client.events import AgentStateEvent, StringOutputEvent
from eidolon_ai_client.group_conversation import GroupConversation
from eidolon_ai_sdk.agent.agent import register_program, AgentState, register_action
from eidolon_ai_sdk.cpu.agent_call_history import AgentCallHistory
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_examples.group_conversation.conversation_agent import Thought


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
            topic: Annotated[str, Body(description="The topic of the new conversation", embed=True)],
    ) -> AgentState[str]:
        """
        Called to start the conversation. Every user will get a turn in each turn of the conversation.
        """
        # start conversation with every agent
        group = await GroupConversation.create(self.spec.agents)
        await self._store_state(process_id, group)
        await group.action("start_conversation")

        await group.action("add_thoughts", {"thoughts": [Thought(
            is_inner_voice=False,
            agent_name="Coordinator",
            thought=f"Your are in a conversation with agents {', '.join(self.spec.agents)}.\n"
                    f"You are all discussing the topic of {topic}.\n"
        ).model_dump()]})

        async for event in self._ping_agents(group):
            yield event

        await self._store_state(process_id, group)

        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def ping_agents(self, process_id):
        group = await self._restore_state(process_id)
        async for event in self._ping_agents(group):
            yield event

        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def add_thoughts(
            self,
            process_id,
            thoughts: Annotated[List[Thought], Body(embed=True), "The thoughts to add to the agent's inner monologue."]
    ) -> AgentState[str]:
        """
        Called to record a thought either from another agent or from the coordinator.
        """
        group = await self._restore_state(process_id)
        await group.action("add_thoughts", {"thoughts": thoughts})

        yield AgentStateEvent(state="idle")

    async def _ping_agents(self, group: GroupConversation):
        def parse_response(response: str):
            pattern = r"'''(thought|emotion|speak)\n(.*?)\n'''"
            matches = re.findall(pattern, response, re.DOTALL)

            # Dictionary to store the parsed data
            parsed_data = {key: "" for key in ["thought", "emotion", "speak"]}
            for match in matches:
                key, content = match
                parsed_data[key] = content.strip()

            emotion = parsed_data['emotion'] if parsed_data['emotion'] else "<agent showed no emotion>"
            spoken = parsed_data['speak'] if parsed_data['speak'] else "<agent said nothing>"
            parsed_data["outer_voice"] = f"Agent {agent} emotions appear to be \"{emotion} and they said:\n{spoken}\n\n"

            return parsed_data

        conversations_per_agent = {}
        async for event in group.stream_action("ping"):
            if event.stream_context in self.spec.agents and isinstance(event, StringOutputEvent):
                if event.stream_context not in conversations_per_agent:
                    conversations_per_agent[event.stream_context] = ""
                conversations_per_agent[event.stream_context] += event.content
            yield event

        conversation_responses = {}
        for agent, conversation in conversations_per_agent.items():
            conversation_responses[agent] = parse_response(conversation)

        for agent_process in group.agents:
            local_conversations = []
            for agent, conversation in conversation_responses.items():
                if agent != agent_process.agent:
                    local_conversations.append(Thought(is_inner_voice=False, agent_name=agent, thought=conversation["outer_voice"]))
            await Agent.get(agent_process.agent).process(agent_process.process_id).action("add_thoughts", {"thoughts": local_conversations})

        for agent, conversation in conversation_responses.items():
            emotions = conversation["emotion"] if conversation["emotion"] and len(conversation["emotion"].strip()) > 0 else "*agent showed no emotion*"
            thoughts = conversation["thought"] if conversation["thought"] and len(conversation["thought"].strip()) > 0 else "*agent had no thoughts*"
            speak = conversation["speak"] if conversation["speak"] and len(conversation["speak"].strip()) > 0 else "*agent said nothing*"
            yield StringOutputEvent(content=f"##### Agent: {agent}\n")
            yield StringOutputEvent(content=f"<span style='color:#6677aa'>Emotions: ")
            yield StringOutputEvent(content=emotions)
            yield StringOutputEvent(content="</span>\n\n")
            yield StringOutputEvent(content=f"<span style='color:#66aa44'>Thoughts: ")
            yield StringOutputEvent(content=thoughts)
            yield StringOutputEvent(content="</span>\n\n")
            yield StringOutputEvent(content=speak)
            yield StringOutputEvent(content="\n\n---\n")

    async def _restore_state(self, process_id) -> GroupConversation:
        processes = []
        for process in await AgentCallHistory.get_agent_state(parent_process_id=process_id):
            processes.append(
                ProcessStatus(machine=process.machine, agent=process.agent, process_id=process.remote_process_id, state=process.state, available_actions=process.available_actions))
        return await GroupConversation.restore(processes)

    async def _store_state(self, process_id: str, group: GroupConversation):
        for agent in group.agents:
            history = AgentCallHistory(parent_process_id=process_id, parent_thread_id=None, machine=agent.machine, agent=agent.agent,
                                       remote_process_id=agent.process_id, state=agent.state, available_actions=agent.available_actions)
            await history.upsert()

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
