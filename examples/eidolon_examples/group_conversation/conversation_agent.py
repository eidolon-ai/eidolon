from fastapi import Body
from pydantic import BaseModel, Field
from typing import Annotated, List

from eidos_sdk.agent.agent import AgentState, register_program, register_action
from eidos_sdk.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage
from eidos_sdk.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidos_sdk.cpu.llm_message import AssistantMessage
from eidos_sdk.system.reference_model import Reference, Specable


class Statement(BaseModel):
    speaker: str
    text: str
    voice_level: float

    def mood(self):
        if self.voice_level < 0.25:
            mood = "passive"
        elif self.voice_level < 0.5:
            mood = "vocal"
        elif self.voice_level < 0.75:
            mood = "leaning in"
        else:
            mood = "aggressive"

        return mood

    def format(self, agent_name: str):
        speaker = self.speaker
        if self.speaker == agent_name:
            speaker = "<your inner voice>"
        return f"{speaker} (mood:{self.mood()}): {self.text}\n\n"


class ThoughtResult(BaseModel):
    desire_to_speak: float = Field(description="The desire to speak. A value between 0 and 1. The higher the value, the more the agent wants to speak.")


class SpeakResult(BaseModel):
    inner_dialog: str = Field(
        description="The inner dialog of the agent. This isn't spoken out loud, but is used to help the agent decide what to say next and how they really feel.")
    desire_to_speak: float = Field(description="The desire to speak. A value between 0 and 1. The higher the value, the more the agent wants to speak.")
    voice_level: float = Field(...,
                               description="The voice level. A value between 0 and 1. The higher the value, the louder the agent is speaking and leaning into the conversation.")
    emoji: str = Field(..., description="An emoji that describes your tone and/or mood.")
    response: str = Field(..., description="The response the agent wants to say to others in the group.")

    def mood(self):
        if self.voice_level < 0.25:
            mood = "passive"
        elif self.voice_level < 0.5:
            mood = "vocal"
        elif self.voice_level < 0.75:
            mood = "leaning in"
        else:
            mood = "aggressive"

        return mood


class CharacterThought(BaseModel):
    agent_name: str = Field(description="The name of the agent")
    thought: str = Field(description="The thought about the agent")


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
        system_prompt_prelude = "You are an agent mimicking a human. You will be given a topic and you should respond to it as if you were a human. Your personality is:\n"
        await t.set_boot_messages(
            prompts=[SystemCPUMessage(prompt=system_prompt_prelude + self.spec.system_prompt),
                     UserTextCPUMessage(prompt=f"Your name is {self.spec.agent_name}. "
                                               f"People will address you by that name and you should interpret comments related to that person as you.\n\n"
                                               f"moderator: {topic}\n\n")],
        )

        return AgentState(name="idle", data='...waiting...')

    @register_action("idle")
    async def record_statement(self, process_id, statement: Annotated[Statement, Body(embed=True)]) -> AgentState[ThoughtResult]:
        """
        Called to record a statement from another agent. Will return a new state dictating what the agent wants to do next.
        Also called to add to your inner monologue.
        """
        t = await self.cpu.main_thread(process_id)
        if statement.speaker == self.spec.agent_name:
            # record the statement as your inner monologue
            prompt = (f"moderator: You are recording a new thought for yourself. "
                      f"Keep this though internal but use it to change the conversation or your perception of someone else. Thought:\n{statement.text}")
            await self.cpu.memory_unit.storeMessages(t.call_context(), [AssistantMessage(content=prompt, tool_calls=[])])
            return AgentState(name="idle", data=(ThoughtResult(desire_to_speak=1)))
        else:
            prompt = f"moderator: You are not speaking right now. Respond with ONLY your desire to speak.\n\n{statement.format(self.spec.agent_name)}"
            return AgentState(name="idle", data=await t.schedule_request_with_model(prompts=[UserTextCPUMessage(prompt=prompt)], output_format=ThoughtResult))

    @register_action("idle")
    async def speak(self, process_id) -> AgentState[SpeakResult]:
        """
        Called to allow the agent to speak
        """
        message = UserTextCPUMessage(prompt="moderator: It is your turn to speak\n")
        t = await self.cpu.main_thread(process_id)
        resp = await t.schedule_request_with_model(prompts=[message], output_format=SpeakResult)
        resp.desire_to_speak = 0
        return AgentState(name="idle", data=resp)

    @register_action("idle")
    async def describe_thoughts(self, process_id, people: Annotated[List[str], Body(embed=True)]) -> AgentState[List[CharacterThought]]:
        """
        Called to allow the agent to speak
        """
        instructions = ""
        if len(people) == 0 or self.spec.agent_name in people:
            instructions += (f"{self.spec.agent_name}: You are thinking about your own thoughts. "
                             f"Respond with your inner thoughts about the conversation and record that as your name, {self.spec.agent_name}.\n")

        for person in people:
            if person != self.spec.agent_name:
                instructions += f"{person}: You are thinking about {self.spec.agent_name}. Respond with your inner thoughts about {person}.\n"

        message = UserTextCPUMessage(prompt=f"{self.spec.agent_name}: {instructions}\n")
        t = await self.cpu.main_thread(process_id)
        resp = await t.schedule_request_with_model(prompts=[message], output_format=List[CharacterThought])
        return AgentState(name="idle", data=resp)
