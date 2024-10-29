from typing import Tuple, List, Annotated, TypeVar, Dict

from fastapi import Body
from pydantic import BaseModel

from eidolon_ai_client.client import ProcessStatus
from eidolon_ai_client.events import AgentStateEvent, StringOutputEvent, ObjectOutputEvent
from eidolon_ai_client.group_conversation import GroupConversation
from eidolon_ai_sdk.agent.agent import register_program, AgentState, register_action
from eidolon_ai_sdk.apu.agent_call_history import AgentCallHistory
from eidolon_ai_sdk.system.specable import Specable
from eidolon_examples.group_conversation.conversation_agent import Thought, AgentThought


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

        await group.action(
            "add_thoughts",
            {
                "thoughts": [
                    Thought(
                        is_inner_voice=False,
                        agent_name="Coordinator",
                        thought=f"Your are in a conversation with agents {', '.join(self.spec.agents)}.\n"
                        f"You are all discussing the topic of {topic}.\n",
                    ).model_dump()
                ]
            },
        )

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
        thoughts: Annotated[List[Thought], Body(embed=True), "The thoughts to add to the agent's inner monologue."],
    ) -> AgentState[str]:
        """
        Called to record a thought either from another agent or from the coordinator.
        """
        group = await self._restore_state(process_id)
        await group.action("add_thoughts", {"thoughts": thoughts})

        yield AgentStateEvent(state="idle")

    async def _ping_agents(self, group: GroupConversation):
        yield StringOutputEvent(content="### Gathering agent thoughts and emotions.\n")
        thought_responses: Dict[str, AgentThought] = {}
        async for event in group.stream_action("think"):
            if event.stream_context in self.spec.agents and isinstance(event, ObjectOutputEvent):
                thought_responses[event.stream_context] = event.content
            yield event

        yield StringOutputEvent(content="### Allowing agents to speak.\n")
        conversations_per_agent = {}
        async for event in group.stream_action("speak"):
            if event.stream_context in self.spec.agents and isinstance(event, StringOutputEvent):
                if event.stream_context not in conversations_per_agent:
                    conversations_per_agent[event.stream_context] = ""
                conversations_per_agent[event.stream_context] += event.content
            yield event

        yield StringOutputEvent(content="### Recording thoughts with other agents.\n")
        for agent_process in group.agents:
            local_conversations = []
            for agent, conversation in conversations_per_agent.items():
                if agent != agent_process.agent:
                    local_conversations.append(Thought(is_inner_voice=False, agent_name=agent, thought=conversation))
            await agent_process.action("add_thoughts", {"thoughts": local_conversations})

        for agent_process in group.agents:
            agent = agent_process.agent
            thought = thought_responses[agent]
            emotions = (
                thought["emotion"]
                if thought["emotion"] and len(thought["emotion"].strip()) > 0
                else "*agent showed no emotion*"
            )
            thoughts = (
                thought["thought"]
                if thought["thought"] and len(thought["thought"].strip()) > 0
                else "*agent had no thoughts*"
            )
            speak = (
                conversations_per_agent[agent]
                if conversations_per_agent[agent] and len(conversations_per_agent[agent].strip()) > 0
                else "*agent said nothing*"
            )
            yield StringOutputEvent(content=f"##### Agent: {agent}\n")
            yield StringOutputEvent(content="<span style='color:#6677aa'>Emotion: ")
            yield StringOutputEvent(content=emotions)
            yield StringOutputEvent(content="</span>\n\n")
            yield StringOutputEvent(content="<span style='color:#66aa44'>Thoughts: ")
            yield StringOutputEvent(content=thoughts)
            yield StringOutputEvent(content="</span>\n\n")
            yield StringOutputEvent(content=speak)
            yield StringOutputEvent(content="\n\n---\n")

    async def _restore_state(self, process_id) -> GroupConversation:
        processes = []
        for process in await AgentCallHistory.get_agent_state(parent_process_id=process_id):
            processes.append(
                ProcessStatus(
                    machine=process.machine,
                    agent=process.agent,
                    process_id=process.remote_process_id,
                    state=process.state,
                    available_actions=process.available_actions,
                )
            )
        return await GroupConversation.restore(processes)

    async def _store_state(self, process_id: str, group: GroupConversation):
        for agent in group.agents:
            history = AgentCallHistory(
                parent_process_id=process_id,
                parent_thread_id=None,
                machine=agent.machine,
                agent=agent.agent,
                remote_process_id=agent.process_id,
                state=agent.state,
                available_actions=agent.available_actions,
            )
            await history.upsert()
