from fastapi import Body
from pydantic import BaseModel
from typing import Annotated

from eidos_sdk.agent.agent import AgentState, register_program, register_action
from eidos_sdk.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage
from eidos_sdk.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidos_sdk.cpu.llm_message import UserMessageText, UserMessage
from eidos_sdk.system.reference_model import Reference, Specable


class Statement(BaseModel):
    speaker: str
    text: str

    def format(self):
        return f"{self.speaker}: {self.text}\n\n"


class ConversationAgentSpec(BaseModel):
    cpu: Reference[ConversationalAgentCPU]
    agent_name: str
    system_prompt: str


class ConversationAgent(Specable[ConversationAgentSpec]):
    cpu: ConversationalAgentCPU
    system_prompt: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cpu = self.spec.cpu.instantiate()
        self.system_prompt = self.spec.system_prompt

    @register_program()
    async def start_conversation(self, process_id, topic: Annotated[str, Body(description="The topic of the new conversation", embed=True)]):
        """
        Called to start the conversation. Will return a new state dictating what the agent wants to do next.
        """
        t = await self.cpu.main_thread(process_id)
        await t.set_boot_messages(
            prompts=[SystemCPUMessage(prompt=self.spec.system_prompt),
                     UserTextCPUMessage(prompt=f"Your name is {self.spec.agent_name}. "
                                               f"People will address you by that name and you should interpret comments related to that person as you.\n\n"
                                               f"moderator: {topic}\n\n")],
        )

        return AgentState(name="idle", data='...waiting...')

    @register_action("idle")
    async def record_statement(self, process_id, statement: Annotated[Statement, Body(embed=True)]):
        """
        Called to record a statement from another agent. Will return a new state dictating what the agent wants to do next.
        """
        if statement.speaker != self.spec.agent_name:
            t = await self.cpu.main_thread(process_id)
            await self.cpu.memory_unit.storeMessages(t.call_context(), [UserMessage(content=UserMessageText(prompt=statement.format()))])

        return AgentState(name="idle", data="...recorded...")

    @register_action("idle")
    async def speak(self, process_id):
        """
        Called to allow the agent to speak
        """
        t = await self.cpu.main_thread(process_id)
        existing_messages = await self.cpu.memory_unit.getConversationHistory(t.call_context())
        if not isinstance(existing_messages[-1], UserMessage):
            await self.cpu.memory_unit.storeMessages(t.call_context(), [UserMessage(content=UserMessageText(text="Interesting...continue"))])

        response = await t.schedule_request(prompts=[])

        return AgentState(name="idle", data=response)
