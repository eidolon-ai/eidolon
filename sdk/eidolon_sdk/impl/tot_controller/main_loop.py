from textwrap import indent
from typing import List, Union, Dict, Any, Tuple

from pydantic import Field, BaseModel

from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage
from eidolon_sdk.cpu.control_unit import ControlUnit, ControlUnitConfig
from eidolon_sdk.cpu.llm_message import LLMMessage, UserMessage, UserMessageText, AssistantMessage
from eidolon_sdk.impl.tot_controller.checker import ToTChecker
from eidolon_sdk.impl.tot_controller.controller import ToTController
from eidolon_sdk.impl.tot_controller.memory import ToTDFSMemory
from eidolon_sdk.impl.tot_controller.prompts import PROPOSE_PROMPT
from eidolon_sdk.impl.tot_controller.thought import Thought, ThoughtValidity
from eidolon_sdk.impl.tot_controller.thought_generators import SampleCoTStrategy, BaseThoughtGenerationStrategy
from eidolon_sdk.reference_model import Specable, Reference
from jinja2 import Environment, StrictUndefined


class ThreadOfThoughtsControllerConfig(ControlUnitConfig):
    num_iterations: int = Field(10, description="The maximum number of iterations to run the tree of thoughts algorithm.")
    num_children: int = Field(10, description="The maximum number of children to generate for each node in the tree of thoughts algorithm.")
    thought_generator: Reference[BaseThoughtGenerationStrategy] = Field(default=None, description="The thought generator to use.")


class TreeOfThoughtsController(ControlUnit, Specable[ThreadOfThoughtsControllerConfig]):
    tot_memory: ToTDFSMemory = ToTDFSMemory()
    checker: ToTChecker
    tot_controller: ToTController = ToTController()

    def __init__(self, spec: ThreadOfThoughtsControllerConfig, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
        self.thought_generator = spec.thought_generator.instantiate()

    def log_thought(
        self,
        thought: Thought,
        level: int,
    ) -> None:
        colors = {
            ThoughtValidity.VALID_FINAL: "green",
            ThoughtValidity.VALID_INTERMEDIATE: "yellow",
            ThoughtValidity.INVALID: "red",
        }
        text = indent(f"Thought: {thought.text}\n", prefix="    " * level)
        self.logger.info(text)

    async def process_llm_requests(self, call_context: CallContext, boot_conversation: List[LLMMessage], conversation: List[LLMMessage], should_store_tool_calls: bool,
                                   conv_output_format: Dict[str, Any]):
        # override to run the tree of thoughts algorithm in a separate thread
        new_context = call_context.derive_call_context()
        user_message = conversation[-1]
        thoughts_path: Tuple[str, ...] = ()
        checker_inputs = {}
        level = 0

        async def exec_request(messages: List[LLMMessage], output_format: Dict[str, Any]) -> AssistantMessage:
            return await super().process_llm_requests(new_context, [], messages, False, output_format)

        for _ in range(self.spec.num_iterations):
            thought_text = self.thought_generator.next_thought(user_message, exec_request, thoughts_path)
            checker_inputs["thoughts"] = thoughts_path + (thought_text,)
            thought_validity = self.checker(
                checker_inputs, callbacks=_run_manager.get_child()
            )["validity"]
            thought = Thought(text=thought_text, validity=thought_validity)
            if thought.validity == ThoughtValidity.VALID_FINAL:
                self.log_thought(thought, level, run_manager)
                return {self.output_key: thought.text}
            self.tot_memory.store(thought)
            self.log_thought(thought, level, run_manager)
            thoughts_path = self.tot_controller(self.tot_memory)

        return await super().process_llm_requests(call_context, boot_conversation, conversation, should_store_tool_calls, output_format)

