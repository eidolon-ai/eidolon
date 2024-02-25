from textwrap import dedent
from typing import Annotated, List, Optional

from fastapi import Body
from jinja2 import StrictUndefined, Environment
from pydantic import BaseModel, Field

from eidolon_ai_client.events import AgentStateEvent
from eidolon_ai_sdk.agent.agent import register_program, register_action
from eidolon_ai_sdk.cpu.agent_io import SystemCPUMessage, UserTextCPUMessage
from eidolon_ai_sdk.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidolon_ai_sdk.cpu.llm_message import UserMessage, UserMessageText, SystemMessage
from eidolon_ai_sdk.system.reference_model import Reference, Specable


class Thought(BaseModel):
    is_inner_voice: bool = Field(
        description="If true, the thought will be added as the agent's inner monologue. If false, the thought will be a user message."
    )
    agent_name: Optional[str] = Field(default=None, description="The name of the agent that the thought is about or leave empty if an inner thought.")
    thought: str = Field(description="The thought to add to the agent's inner monologue.")


class ConversationAgentSpec(BaseModel):
    cpu: Reference[ConversationalAgentCPU]
    agent_name: str
    system_prompt: Optional[str] = Field(default=None, description="The prompt to show the agent when the conversation starts.")
    personality: str
    ping_prompt: Optional[str] = Field(default=None, description="The prompt to show the agent when they are pinged.")


class ConversationAgent(Specable[ConversationAgentSpec]):
    cpu: ConversationalAgentCPU
    system_prompt: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.env = Environment(undefined=StrictUndefined)
        self.cpu = self.spec.cpu.instantiate()
        self.system_prompt = self.spec.system_prompt
        if not self.system_prompt:
            self.system_prompt = "You are an agent mimicking a human. You will be given a topic and you should respond to it as if you were a human."
        self.ping_prompt = self.spec.ping_prompt
        if not self.ping_prompt:
            self.ping_prompt = dedent("""
                You have been pinged. You can do one or all of the following:
                - Respond to the last thing said
                - Express a thought
                - Show an emotion
                
                The people who have spoken since you last spoke are: {{agents_spoke_since_me}}
                
                You must format your response like this:
                '''thought
                I wish John would stop talking so much.
                '''
                '''emotion
                I'm feeling really happy right now.
                '''
                '''speak
                I think we should talk about the weather.
                '''
                
                If you don't want to do any of the above, just respond with empty text.
                
                You can and should include markdown in each section of the response. Separate each section with a newline.
                
                Remember, you don't need to respond to every ping. You can choose to ignore them, but if you want to speak or you want to express your thoughts or emotions, you should respond to the ping.
            """).strip()

    @register_program()
    async def start_conversation(
            self, process_id
    ):
        """
        Called to start the conversation. Will return a new state dictating what the agent wants to do next.
        """
        t = await self.cpu.main_thread(process_id)
        await t.set_boot_messages(
            prompts=[
                SystemCPUMessage(prompt=self.system_prompt),
                SystemCPUMessage(prompt="Your personality is:\n" + self.spec.personality)
            ],
        )
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def add_thoughts(
            self, process_id, thoughts: Annotated[List[Thought], Body(embed=True), "The thoughts to add to the agent's inner monologue."]
    ):
        """
        Called to record a thought either from another agent or from the coordinator.
        """
        t = await self.cpu.main_thread(process_id)
        messages = []
        for thought in thoughts:
            if thought.is_inner_voice:
                messages.append(SystemMessage(content=f"I have a thought: {thought.thought}"))
            else:
                messages.append(UserMessage(content=[UserMessageText(text=f"{thought.agent_name} said: {thought.thought}")]))

        await self.cpu.memory_unit.storeMessages(
            call_context=t.call_context(),
            messages=messages,
        )
        yield AgentStateEvent(state="idle")

    @register_action("idle")
    async def ping(self, process_id):
        """
        Called to allow the agent to do one or all of the following:
        - Respond to the last thing said
        - Express a thought
        - Express a desire to speak
        - Show an emotion
        """
        # todo -- get the agents that have spoken since the last time this agent spoke
        agents_spoke_since_me = []
        agents = ", ".join(agents_spoke_since_me)
        if len(agents_spoke_since_me) == 0:
            agents = "[No one has spoken]"

        prompt = UserTextCPUMessage(prompt=self.env.from_string(self.ping_prompt).render(agents_spoke_since_me=agents))
        t = await self.cpu.main_thread(process_id)
        async for event in t.stream_request(prompts=[prompt], output_format=str):
            yield event
        yield AgentStateEvent(state="idle")
