"""
We provide two strategies for generating thoughts in the Tree of Thoughts (ToT)
framework to avoid repetition:

These strategies ensure that the language model generates diverse and
non-repeating thoughts, which are crucial for problem-solving tasks that require
exploration.
"""
from abc import abstractmethod
from typing import Any, Dict, List, Callable, Awaitable

from jinja2 import StrictUndefined, Environment
from pydantic import Field, BaseModel

from eidolon_ai_sdk.cpu.agent_io import SystemAPUMessage, UserTextAPUMessage, CPUMessageTypes
from eidolon_ai_sdk.cpu.llm_message import UserMessage, LLMMessage
from eidolon_ai_sdk.agent.tot_agent.prompts import (
    POST_AMBLE,
    THOUGHTS,
    PREAMBLE,
    POST_AMBLE_MULTI,
)
from eidolon_ai_sdk.system.reference_model import Specable


class TGSConfig(BaseModel):
    preamble: str = PREAMBLE
    thoughts: str = THOUGHTS
    post_amble: str = POST_AMBLE
    num_children: int = Field(3, description="The number of thoughts to generate.")


class ThoughtGenerationStrategy(Specable[TGSConfig]):
    """
    Base class for a thought generation strategy.
    """

    spec: TGSConfig
    env = Environment(undefined=StrictUndefined)

    def __init__(self, spec):
        super().__init__(spec)
        self.spec = spec

    def build_prompt(self, user_message, thoughts_path: List[str]) -> (List[CPUMessageTypes], List[CPUMessageTypes]):
        thoughts_tuple = tuple(thoughts_path)
        preamble_txt = self.env.from_string(self.spec.preamble).render(thoughts=thoughts_tuple, n=self.spec.num_children)
        thoughts_txt = self.env.from_string(self.spec.thoughts).render(thoughts=thoughts_tuple, n=self.spec.num_children)
        post_amble_txt = self.env.from_string(self.spec.post_amble).render(
            thoughts=thoughts_tuple, n=self.spec.num_children
        )
        return (
            [SystemAPUMessage(prompt=preamble_txt)],
            [
                UserTextAPUMessage(prompt=user_message),
                UserTextAPUMessage(prompt=thoughts_txt),
                UserTextAPUMessage(prompt=post_amble_txt),
            ],
        )

    @abstractmethod
    async def next_thought(
        self,
        user_message: str,
        llm_call: Callable[
            [List[LLMMessage], List[LLMMessage], Dict[str, Any]],
            Awaitable[Dict[str, Any]],
        ],
        thoughts_path: List[str] = Field(default_factory=list),
    ) -> str:
        """
        Generate the next thought given the problem description and the thoughts
        generated so far.
        """


class SampleCoTStrategyOutput(BaseModel):
    thought: str


class SampleCoTStrategy(ThoughtGenerationStrategy):
    """
    Sample thoughts from a Chain-of-Thought (CoT) prompt.

    This strategy works better when the thought space is rich, such as when each
    thought is a paragraph. Independent and identically distributed samples
    lead to diversity, which helps to avoid repetition.
    """

    async def next_thought(
        self,
        user_message: UserMessage,
        llm_call: Callable[
            [List[LLMMessage], List[LLMMessage], Dict[str, Any]],
            Awaitable[Dict[str, Any]],
        ],
        thoughts_path: List[str] = Field(default_factory=list),
    ) -> str:
        system_messages, messages = self.build_prompt(user_message, thoughts_path)
        next_thought = await llm_call(system_messages, messages, SampleCoTStrategyOutput.model_json_schema())
        return next_thought["thought"]


class ProposeOutputFormat(BaseModel):
    thoughts: List[str]


class ProposePromptStrategyConfig(TGSConfig):
    post_amble: str = POST_AMBLE_MULTI


class ProposePromptStrategy(ThoughtGenerationStrategy, Specable[ProposePromptStrategyConfig]):
    """
    Propose thoughts sequentially using a "propose prompt".

    This strategy works better when the thought space is more constrained, such
    as when each thought is just a word or a line. Proposing different thoughts
    in the same prompt completion helps to avoid duplication.
    """

    tot_memory: Dict[tuple, List[str]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tot_memory = {}

    async def next_thought(
        self,
        user_message: UserMessage,
        llm_call: Callable[
            [List[LLMMessage], List[LLMMessage], Dict[str, Any]],
            Awaitable[Dict[str, Any]],
        ],
        thoughts_path: List[str] = Field(default_factory=list),
    ) -> str:
        thoughts_tuple = tuple(thoughts_path)
        if thoughts_tuple not in self.tot_memory or not self.tot_memory[thoughts_tuple]:
            system_messages, messages = self.build_prompt(user_message, thoughts_path)
            next_thought_msg = await llm_call(system_messages, messages, ProposeOutputFormat.model_json_schema())
            self.tot_memory[thoughts_tuple] = next_thought_msg["thoughts"]
        return self.tot_memory[thoughts_tuple].pop()
