from fastapi import Body
from pydantic import BaseModel
from typing import Tuple, List, Annotated

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

        # record the pids of the agents with our process_id in memory
        await AgentOS.symbolic_memory.insert_one("conversation_coordinator", ConversationState(process_id=process_id, agent_pids=agent_pids, topic=topic).model_dump())

        return AgentState(name="idle", data="Agents started. Waiting for first turn...")

    @register_action("idle")
    async def next_turn(self, process_id) -> AgentState[str]:
        """
        Called to start the next turn of the conversation.
        """
        # get the pids of the agents with our process_id in memory
        result = await AgentOS.symbolic_memory.find_one("conversation_coordinator", {"process_id": process_id})
        conversation_state = ConversationState.model_validate(result)
        print(conversation_state.model_dump())

        async def record_statements(speaker, statement):
            for state_agent_name, state_agent_pid in conversation_state.agent_pids:
                if state_agent_name != speaker:
                    await Machine().agent(state_agent_name).process(state_agent_pid).action("record_statement", {"statement": {"speaker": speaker, "text": statement}})

        output = ""
        for agent_name, agent_pid in conversation_state.agent_pids:
            response = await Machine().agent(agent_name).process(agent_pid).action("speak", {})
            agent_response = response.data
            await record_statements(agent_name, agent_response)
            output += f"{agent_name}: {agent_response}\n\n"

        return AgentState(name="idle", data=output)
