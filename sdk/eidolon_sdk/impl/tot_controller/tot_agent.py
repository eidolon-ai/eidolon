import logging
from textwrap import indent
from typing import List, Dict, Any, Literal

from fastapi import HTTPException
from pydantic import Field, BaseModel

from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage, AssistantMessage, UserMessage, UserMessageText, LLMMessageTypes
from eidolon_sdk.cpu.llm_unit import LLMCallFunction
from eidolon_sdk.impl.agent_llm_unit import LLMAgent
from eidolon_sdk.impl.tot_controller.checker import ToTChecker
from eidolon_sdk.impl.tot_controller.controller import ToTController
from eidolon_sdk.impl.tot_controller.memory import ToTDFSMemory
from eidolon_sdk.impl.tot_controller.thought import Thought, ThoughtValidity
from eidolon_sdk.impl.tot_controller.thought_generators import BaseThoughtGenerationStrategy, ProposePromptStrategy
from eidolon_sdk.reference_model import Specable, Reference
from eidolon_sdk.util.class_utils import fqn


class ToTAgentConfig(BaseModel):
    num_iterations: int = Field(10, description="The maximum number of iterations to run the tree of thoughts algorithm.")
    num_children: int = Field(10, description="The maximum number of children to generate for each node in the tree of thoughts algorithm.")
    thought_generator: Reference[BaseThoughtGenerationStrategy] = Field(
        default=Reference(implementation=fqn(ProposePromptStrategy)),
        description="The thought generator to use."
    )
    checker: Reference[ToTChecker] = Field(default=Reference(implementation=fqn(ToTChecker)), description="The checker to use.")
    fallback: Literal["ERROR", "LLM"] = "ERROR"


class TreeOfThoughtsAgent(LLMAgent, Specable[ToTAgentConfig]):
    logger = logging.getLogger("eidolon")
    thought_generator: BaseThoughtGenerationStrategy
    tot_memory: ToTDFSMemory
    tot_controller: ToTController
    checker: ToTChecker

    def __init__(self, spec: ToTAgentConfig, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
        self.thought_generator = spec.thought_generator.instantiate()
        self.checker = spec.checker.instantiate(cpu=self.cpu)
        self.tot_memory = ToTDFSMemory()
        self.tot_controller = ToTController()

    def log_thought(
        self,
        thought: Thought,
        level: int,
    ) -> None:
        text = indent(f"Thought: {thought.text}\n", prefix="    " * level)
        self.logger.info(text)

    async def execute_llm(self, call_context: CallContext, messages: List[LLMMessageTypes], tools: List[LLMCallFunction], output_format: Dict[str, Any]) -> AssistantMessage:
        # override to run the tree of thoughts algorithm in a separate thread
        new_context = call_context.derive_call_context()
        user_message = messages[-1]
        prior_messages = messages[:-1]
        thoughts_path: List[str] = []
        level = 0

        if not isinstance(user_message, UserMessage) or not isinstance(user_message.content[-1], UserMessageText):
            raise HTTPException(status_code=400, detail="The last message in the list of messages must be a user message with text content")
        else:
            user_message_text = user_message.content[-1].text

        async def exec_request(_messages: List[LLMMessage], _output_format: Dict[str, Any]) -> AssistantMessage:
            return await self.cpu.process_llm_requests(new_context, prior_messages, _messages, False, _output_format)

        for _ in range(self.spec.num_iterations):
            thought_text = await self.thought_generator.next_thought(user_message, exec_request, thoughts_path)
            thought_validity = await self.checker.evaluate(
                context=new_context,
                prior_messages=prior_messages,
                problem_description=user_message_text,
                thoughts=thoughts_path + [thought_text]
            )
            thought = Thought(text=thought_text, validity=thought_validity.validity)
            if thought.validity == "FINAL":
                self.log_thought(thought, level)
                # go back to llm now with the tree of thoughts and the requested output format
                return await self.cpu.process_llm_requests(
                    call_context,
                    boot_conversation=[],
                    conversation=messages + [UserMessage(
                        content=[UserMessageText(text="THOUGHTS\n\n" + ("\n".join(thoughts_path + [thought_text])))]
                    )],
                    should_store_tool_calls=False,
                    output_format=output_format,
                )
            self.tot_memory.store(thought)
            self.log_thought(thought, level)
            thoughts_path = self.tot_controller.thoughts(self.tot_memory)

        if self.spec.fallback == "ERROR":
            raise HTTPException(status_code=400, detail=dict(
                error=f"Could not find a valid thought within {self.spec.num_iterations} iterations.",
                thoughts=thoughts_path,
            ))
        elif self.spec.fallback == "LLM":
            return await self.cpu.process_llm_requests(call_context, [], messages, False, output_format)
        else:
            raise ValueError(f"Unknown fallback type: {self.spec.fallback}")

