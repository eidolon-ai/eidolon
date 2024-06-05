from __future__ import annotations

from textwrap import indent
from typing import List, Dict, Any, Literal, Optional, Type, Union

from fastapi import HTTPException
from jinja2 import StrictUndefined, Environment
from pydantic import Field, BaseModel

from eidolon_ai_sdk.agent.agent import register_program, Agent, AgentSpec
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.agent.tot_agent.checker import ToTChecker
from eidolon_ai_sdk.agent.tot_agent.controller import ToTController
from eidolon_ai_sdk.agent.tot_agent.memory import ToTDFSMemory
from eidolon_ai_sdk.agent.tot_agent.thought import Thought
from eidolon_ai_sdk.agent.tot_agent.thought_generators import (
    ThoughtGenerationStrategy,
)
from eidolon_ai_sdk.cpu.agent_io import UserTextAPUMessage
from eidolon_ai_sdk.cpu.llm_message import LLMMessage
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class ToTAgentConfig(AgentSpec):
    description: str
    num_iterations: int = Field(
        10,
        description="The maximum number of iterations to run the tree of thoughts algorithm.",
    )
    user_prompt: str = Field(description="The prompt to use when asking the user for a question.")
    input_schema: Dict[str, Any] = Field(description="The json schema for the question input model.")
    output_schema: Union[Literal["str"], Dict[str, Any]] = Field(
        description="The json schema for the output model or the literal 'str' for text output."
    )
    thought_generator: AnnotatedReference[ThoughtGenerationStrategy] = Field(
        description="The thought generation strategy to use."
    )
    checker: AnnotatedReference[ToTChecker] = Field(description="The checker to use to evaluate thoughts.")
    fallback: Literal["ERROR", "LLM"] = "ERROR"
    init_description: Optional[str] = Field(default=None, description="Overrides the description of the INIT endpoint.")


def make_description(agent: object, _handler: FnHandler) -> str:
    # noinspection PyUnresolvedReferences
    spec = agent.spec
    return spec.description


def make_input_schema(agent: object, handler: FnHandler) -> Type[BaseModel]:
    # noinspection PyUnresolvedReferences
    spec = agent.spec
    properties: Dict[str, Any] = {}
    if spec.input_schema:
        properties["body"] = dict(
            type="object",
            properties=spec.input_schema,
        )
    required = ["body"]
    schema = {"type": "object", "properties": properties, "required": required}
    return schema_to_model(schema, f"{handler.name.capitalize()}InputModel")


def make_output_schema(agent: object, handler: FnHandler) -> Type[Any]:
    # noinspection PyUnresolvedReferences
    spec = agent.spec
    if spec.output_schema == "str":
        return str
    elif spec.output_schema:
        return schema_to_model(spec.output_schema, f"{handler.name.capitalize()}OutputModel")
    else:
        raise ValueError("output_schema must be specified")


class TotResponse(BaseModel):
    answer: Any
    thoughts: List[str]


class TreeOfThoughtsAgent(Agent, Specable[ToTAgentConfig]):
    thought_generator: ThoughtGenerationStrategy
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
            handlers = getattr(self.question, "eidolon_handlers")
            for handler in handlers:
                handler.description = self.spec.description

    def log_thought(
        self,
        thought: Thought,
        level: int,
    ) -> None:
        text = indent(f"Thought ({thought.validity}): {thought.text}", prefix="    " * level)
        logger.info(text)

    @register_program(
        input_model=make_input_schema,
        output_model=make_output_schema,
        description=make_description,
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
        question = Environment(undefined=StrictUndefined).from_string(self.spec.user_prompt).render(**body.model_dump())

        async def exec_request(
            _boot_messages: List[LLMMessage],
            _messages: List[LLMMessage],
            _output_format: Dict[str, Any],
        ) -> Dict[str, Any]:
            t2 = await self.cpu.new_thread(process_id)
            await t2.set_boot_messages(prompts=_boot_messages)
            return await t2.run_request(_messages, _output_format)

        for i in range(self.spec.num_iterations):
            thought_text = await self.thought_generator.next_thought(question, exec_request, thoughts_path)
            thought_validity = await self.checker.evaluate(
                process_id,
                problem_description=question,
                thoughts=thoughts_path + [thought_text],
            )
            thought = Thought(text=thought_text, validity=thought_validity.validity)
            self.tot_memory.store(thought)
            self.log_thought(thought, level)
            if thought.validity == "VALID":
                mainThread = await self.cpu.main_thread(process_id)
                # go back to llm now with the tree of thoughts and the requested output format
                conversation = [
                    UserTextAPUMessage(prompt=question),
                    UserTextAPUMessage(prompt="THOUGHTS\n\n" + ("\n".join(thoughts_path + [thought_text]))),
                ]
                resp = await mainThread.run_request(conversation, self.spec.output_schema)
                return TotResponse(answer=resp, thoughts=thoughts_path)
            thoughts_path = self.tot_controller.thoughts(self.tot_memory)

        synopsis = self.tot_controller.exploration_synopsis(self.tot_memory)
        if self.spec.fallback == "ERROR":
            raise HTTPException(
                status_code=400,
                detail=dict(
                    error=f"Could not find a valid thought within {self.spec.num_iterations} iterations.",
                    remaining_thoughts=synopsis,
                ),
            )
        elif self.spec.fallback == "LLM":
            conversation = [
                UserTextAPUMessage(prompt=question),
                UserTextAPUMessage(
                    prompt="You have had some helpful thoughts on the question. Please use them to provide an answer\n\n"
                    + str(synopsis)
                ),
            ]
            thread = await self.cpu.new_thread(process_id)
            resp = await thread.run_request(conversation, self.spec.output_schema)
            return TotResponse(answer=resp, thoughts=thoughts_path)
        else:
            raise ValueError(f"Unknown fallback type: {self.spec.fallback}")
