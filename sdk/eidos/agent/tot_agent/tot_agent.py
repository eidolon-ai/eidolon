from __future__ import annotations

from textwrap import indent
from typing import List, Dict, Any, Literal, Optional

from fastapi import HTTPException
from jinja2 import StrictUndefined, Environment
from pydantic import Field, BaseModel

from eidos.agent.agent import register_program, Agent, AgentSpec, spec_input_model, \
    spec_output_model, nest_with_fn, get_output_model
from eidos.agent.tot_agent.checker import ToTChecker
from eidos.agent.tot_agent.controller import ToTController
from eidos.agent.tot_agent.memory import ToTDFSMemory
from eidos.agent.tot_agent.thought import Thought
from eidos.agent.tot_agent.thought_generators import BaseThoughtGenerationStrategy, ProposePromptStrategy
from eidos.cpu.agent_io import UserTextCPUMessage
from eidos.cpu.llm_message import LLMMessage
from eidos.system.reference_model import Specable, Reference
from eidos.util.class_utils import fqn
from eidos.util.logger import logger


class ToTAgentConfig(AgentSpec):
    num_iterations: int = Field(10, description="The maximum number of iterations to run the tree of thoughts algorithm.")
    question_prompt: str = Field(description="The prompt to use when asking the user for a question.")
    prompt_properties: Dict[str, Any] = Field(description="The json schema for the question input model.")
    thought_generator: Reference(BaseThoughtGenerationStrategy, default=fqn(ProposePromptStrategy))
    checker: Reference(ToTChecker, default=fqn(ToTChecker))
    fallback: Literal["ERROR", "LLM"] = "ERROR"
    output_format: Dict[str, Any] = Field(default=dict(type='string'), description="The requested output format of the INIT endpoint.")
    init_description: Optional[str] = Field(default=None, description="Overrides the description of the INIT endpoint.")


class TotResponse(BaseModel):
    answer: Any
    thoughts: List[str]


class TreeOfThoughtsAgent(Agent, Specable[ToTAgentConfig]):
    thought_generator: BaseThoughtGenerationStrategy
    tot_memory: ToTDFSMemory
    tot_controller: ToTController
    checker: ToTChecker

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.thought_generator = self.spec.thought_generator.instantiate()
        self.checker = self.spec.checker.instantiate(cpu=self.cpu)
        self.tot_memory = ToTDFSMemory()
        self.tot_controller = ToTController()
        if self.spec.init_description:
            self.question.eidolon_handler.description = self.spec.init_description

    def log_thought(
        self,
        thought: Thought,
        level: int,
    ) -> None:
        text = indent(f"Thought ({thought.validity}): {thought.text}", prefix="    " * level)
        logger.info(text)

    @register_program(
        input_model=spec_input_model(lambda spec: dict(type="object", properties=spec.prompt_properties)),
        output_model=spec_output_model(
            get_schema=lambda spec: spec.output_format,
            transformer=nest_with_fn(get_output_model, embed="answer")
        ),
    )
    async def question(self, process_id, body) -> TotResponse:
        """
        Answers a question using the tree of thoughts algorithm. This is computationally expensive, but will provide
        better results than standard llm calls for some problems. Specializes in questions which need to make initial
        assumptions which may not be accurate. The tree of thoughts algorithm will explore many possible assumptions
        and solutions and trim branches when they are found to be invalid.
        """

        # override to run the tree of thoughts algorithm in a separate thread
        thoughts_path: List[str] = []
        level = 0
        question = Environment(undefined=StrictUndefined).from_string(self.spec.question_prompt).render(**body.model_dump())

        async def exec_request(_boot_messages: List[LLMMessage], _messages: List[LLMMessage], _output_format: Dict[str, Any]) -> Dict[str, Any]:
            t2 = await self.cpu.new_thread(process_id)
            await t2.set_boot_messages(_output_format, *_boot_messages)
            return await t2.schedule_request(_messages, _output_format)

        for i in range(self.spec.num_iterations):
            thought_text = await self.thought_generator.next_thought(question, exec_request, thoughts_path)
            thought_validity = await self.checker.evaluate(
                process_id,
                problem_description=question,
                thoughts=thoughts_path + [thought_text]
            )
            thought = Thought(text=thought_text, validity=thought_validity.validity)
            self.tot_memory.store(thought)
            self.log_thought(thought, level)
            if thought.validity == "VALID":
                mainThread = await self.cpu.main_thread(process_id)
                # go back to llm now with the tree of thoughts and the requested output format
                conversation = [UserTextCPUMessage(prompt=question), UserTextCPUMessage(prompt="THOUGHTS\n\n" + ("\n".join(thoughts_path + [thought_text])))]
                resp = await mainThread.schedule_request(conversation, self.spec.output_format)
                return TotResponse(answer=resp, thoughts=thoughts_path)
            thoughts_path = self.tot_controller.thoughts(self.tot_memory)

        synopsis = self.tot_controller.exploration_synopsis(self.tot_memory)
        if self.spec.fallback == "ERROR":
            raise HTTPException(status_code=400, detail=dict(
                error=f"Could not find a valid thought within {self.spec.num_iterations} iterations.",
                remaining_thoughts=synopsis
            ))
        elif self.spec.fallback == "LLM":
            conversation = [UserTextCPUMessage(prompt=question), UserTextCPUMessage(
                prompt="You have had some helpful thoughts on the question. Please use them to provide an answer\n\n" + str(synopsis)
            )]
            thread = await self.cpu.new_thread(process_id)
            resp = await thread.schedule_request(conversation, self.spec.output_format)
            return TotResponse(answer=resp, thoughts=thoughts_path)
        else:
            raise ValueError(f"Unknown fallback type: {self.spec.fallback}")
