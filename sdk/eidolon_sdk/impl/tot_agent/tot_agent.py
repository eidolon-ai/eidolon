import copy
import logging
from textwrap import indent
from typing import List, Dict, Any, Literal, Optional, Iterable

from fastapi import HTTPException
from jinja2 import StrictUndefined, Environment
from pydantic import Field, BaseModel

from eidolon_sdk.agent import initializer, Agent
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage
from eidolon_sdk.cpu.call_context import CallContext
from eidolon_sdk.cpu.llm_message import LLMMessage, AssistantMessage
from eidolon_sdk.impl.tot_agent.checker import ToTChecker
from eidolon_sdk.impl.tot_agent.controller import ToTController
from eidolon_sdk.impl.tot_agent.memory import ToTDFSMemory
from eidolon_sdk.impl.tot_agent.thought import Thought, ThoughtValidity
from eidolon_sdk.impl.tot_agent.thought_generators import BaseThoughtGenerationStrategy, ProposePromptStrategy
from eidolon_sdk.reference_model import Specable, Reference
from eidolon_sdk.util.class_utils import fqn
from eidolon_sdk.util.schema_to_model import schema_to_model


class ToTAgentConfig(BaseModel):
    num_iterations: int = Field(10, description="The maximum number of iterations to run the tree of thoughts algorithm.")
    question_prompt: str = Field(description="The prompt to use when asking the user for a question.")
    question_json_schema: Dict[str, Any] = Field(description="The json schema for the question input model.")
    thought_generator: Reference[BaseThoughtGenerationStrategy] = Field(
        default=Reference(implementation=fqn(ProposePromptStrategy)),
        description="The thought generator to use."
    )
    checker: Reference[ToTChecker] = Field(default=Reference(implementation=fqn(ToTChecker)), description="The checker to use.")
    fallback: Literal["ERROR", "LLM"] = "ERROR"
    output_format: Dict[str, Any] = Field(default=None, description="The requested output format of the INIT endpoint.")
    init_description: Optional[str] = Field(default=None, description="Overrides the description of the INIT endpoint.")


class TotResponse(BaseModel):
    answer: Any
    thoughts: List[str]


class TreeOfThoughtsAgent(Agent, Specable[ToTAgentConfig]):
    spec: ToTAgentConfig
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
        if self.spec.init_description:
            self.action_handlers["INIT"].description = self.spec.init_description

    def log_thought(
        self,
        thought: Thought,
        level: int,
    ) -> None:
        text = indent(f"Thought ({thought.validity}): {thought.text}", prefix="    " * level)
        self.logger.info(text)

    def get_input_model(self, action: str):
        if action == 'INIT':
            return schema_to_model(self.spec.question_json_schema, "InitialQuestionInputModel")
        else:
            return super().get_input_model(action)

    def get_response_model(self, action: str):
        if action == 'INIT':
            schema = TotResponse.model_json_schema()
            schema['properties']['answer'] = self.spec.output_format or dict(type='string')
            return schema_to_model(schema, "InitialQuestionOutputModel")
        else:
            return super().get_response_model(action)

    @initializer
    async def execute_llm(self, **kwargs) -> TotResponse:
        """
        Answers a question using the tree of thoughts algorithm. This is computationally expensive, but will provide
        better results than standard llm calls for some problems. Specializes in questions which need to make initial
        assumptions which may not be accurate. The tree of thoughts algorithm will explore many possible assumptions
        and solutions and trim branches when they are found to be invalid.
        """

        # override to run the tree of thoughts algorithm in a separate thread
        context = CallContext(process_id=self.get_context().process_id, thread_id=None)
        new_context = context.derive_call_context()
        thoughts_path: List[str] = []
        level = 0
        question = Environment(undefined=StrictUndefined).from_string(self.spec.question_prompt).render(**kwargs)

        async def exec_request(_messages: List[LLMMessage], _output_format: Dict[str, Any]) -> AssistantMessage:
            # todo, this should perhaps use schedule request interface
            return await self.cpu.process_llm_requests(new_context, _messages, False, _output_format)

        for i in range(self.spec.num_iterations):
            thought_text = await self.thought_generator.next_thought(question, exec_request, thoughts_path)
            thought_validity = await self.checker.evaluate(
                context=new_context,
                problem_description=question,
                thoughts=thoughts_path + [thought_text]
            )
            thought = Thought(text=thought_text, validity=thought_validity.validity)
            self.tot_memory.store(thought)
            self.log_thought(thought, level)
            if thought.validity == "VALID" or (i == self.spec.num_iterations - 1 and self.spec.fallback == "LLM"):
                if thought.validity != "VALID":
                    # todo, we should give all remaining valid thoughts in this scenario rather than just the current path
                    self.logger.warning(f"Problem not solved after after {self.spec.num_iterations} iterations, but falling back to LLM anyway.")
                # go back to llm now with the tree of thoughts and the requested output format
                conversation = [UserTextCPUMessage(prompt=question), UserTextCPUMessage(prompt="THOUGHTS\n\n" + ("\n".join(thoughts_path + [thought_text])))]
                resp = await self.cpu_request(conversation, self.spec.output_format)
                return TotResponse(answer=resp, thoughts=thoughts_path)
            thoughts_path = self.tot_controller.thoughts(self.tot_memory)

        if self.spec.fallback == "ERROR":
            raise HTTPException(status_code=400, detail=dict(
                error=f"Could not find a valid thought within {self.spec.num_iterations} iterations.",
                remaining_thoughts=self.tot_controller.exploration_synopsis(self.tot_memory)
            ))
        else:
            raise ValueError(f"Unknown fallback type: {self.spec.fallback}")
