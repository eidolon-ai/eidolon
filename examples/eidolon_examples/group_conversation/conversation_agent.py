from textwrap import dedent
from typing import Annotated, List, Optional

from fastapi import Body
from jinja2 import StrictUndefined, Environment
from pydantic import BaseModel, Field

from eidolon_ai_client.events import AgentStateEvent
from eidolon_ai_sdk.agent.agent import register_program, register_action
from eidolon_ai_sdk.apu.agent_io import SystemAPUMessage, UserTextAPUMessage
from eidolon_ai_sdk.apu.conversational_apu import ConversationalAPU
from eidolon_ai_sdk.apu.llm_message import UserMessage, UserMessageText, SystemMessage
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.specable import Specable


class AgentThought(BaseModel):
    thought: str = Field(
        default="", description="The thought you want to express or an empty string if you don't have a thought."
    )
    desire_to_speak: bool = Field(description="If true, you want to speak. If false, you do not want to speak.")
    emotion: Optional[str] = Field(
        default=None,
        description="The emotion you want to express or leave empty if you do not want to express an emotion."
        "The emotion must be a single word and an emojis that represent the emotion. Include both",
    )


class Thought(BaseModel):
    is_inner_voice: bool = Field(
        description="If true, the thought will be added as the agent's inner monologue. If false, the thought will be a user message."
    )
    agent_name: Optional[str] = Field(
        default=None, description="The name of the agent that the thought is about or leave empty if an inner thought."
    )
    thought: str = Field(description="The thought to add to the agent's inner monologue.")


class ConversationAgentSpec(BaseModel):
    apu: Reference[ConversationalAPU]
    agent_name: str
    system_prompt: Optional[str] = Field(
        default=None, description="The prompt to show the agent when the conversation starts."
    )
    personality: str
    think_prompt: Optional[str] = Field(
        default=None, description="The prompt to show the agent when they are pinged to think."
    )
    speak_prompt: Optional[str] = Field(default=None, description="The prompt to show the agent when they are to speak.")


class ConversationAgent(Specable[ConversationAgentSpec]):
    apu: ConversationalAPU
    system_prompt: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.env = Environment(undefined=StrictUndefined)
        self.apu = self.spec.apu.instantiate()
        self.system_prompt = self.spec.system_prompt
        if not self.system_prompt:
            self.system_prompt = "You are an agent mimicking a human. You will be given a topic and you should respond to it as if you were a human."
        self.think_prompt = self.spec.think_prompt
        if not self.think_prompt:
            self.think_prompt = dedent(
                """
                You have been pinged. You can do one or all of the following:
                - Express a thought
                - Show an emotion
                - Express a desire to speak
                
                You can and should include markdown in each section of the response.
                
                Remember, you don't need to respond to every ping. You can choose to ignore them, but if you want to express your thoughts or emotions, you should respond to the ping.
            """
            ).strip()
        self.speak_prompt = self.spec.speak_prompt
        if not self.speak_prompt:
            self.speak_prompt = dedent(
                """
                You have been pinged to speak. Respond with what you want to say or an empty string if you do not want to say anything.
            """
            ).strip()

    @register_program()
    async def start_conversation(self, process_id):
        """
        Called to start the conversation. Will return a new state dictating what the agent wants to do next.
        """
        t = self.apu.main_thread(process_id)
        await t.set_boot_messages(
            prompts=[
                SystemAPUMessage(prompt=self.system_prompt),
                SystemAPUMessage(prompt="Your personality is:\n" + self.spec.personality),
            ],
        )
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def add_thoughts(
        self,
        process_id,
        thoughts: Annotated[List[Thought], Body(embed=True), "The thoughts to add to the agent's inner monologue."],
    ):
        """
        Called to record a thought either from another agent or from the coordinator.
        """
        t = self.apu.main_thread(process_id)
        messages = []
        for thought in thoughts:
            if thought.is_inner_voice:
                messages.append(SystemMessage(content=f"I have a thought: {thought.thought}"))
            else:
                messages.append(
                    UserMessage(content=[UserMessageText(text=f"{thought.agent_name} said: {thought.thought}")])
                )

        await self.apu.memory_unit.storeMessages(
            call_context=t.call_context(),
            messages=messages,
        )
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def think(self, process_id):
        """
        Called to allow the agent to do one or all of the following:
        - Express a thought
        - Express a desire to speak
        - Show an emotion
        """

        prompt = UserTextAPUMessage(prompt=self.env.from_string(self.think_prompt).render())
        t = self.apu.main_thread(process_id)
        async for event in t.stream_request(prompts=[prompt], output_format=AgentThought):
            yield event
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def speak(self, process_id):
        """
        Called to allow the agent to speak
        """
        prompt = UserTextAPUMessage(prompt=self.speak_prompt)
        t = self.apu.main_thread(process_id)
        async for event in t.stream_request(prompts=[prompt], output_format=str):
            yield event
        yield AgentStateEvent(state="idle")
