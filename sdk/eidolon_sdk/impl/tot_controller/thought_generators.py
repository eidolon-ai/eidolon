"""
We provide two strategies for generating thoughts in the Tree of Thoughts (ToT)
framework to avoid repetition:

These strategies ensure that the language model generates diverse and
non-repeating thoughts, which are crucial for problem-solving tasks that require
exploration.
"""
from abc import abstractmethod
from typing import Any, Dict, List, Tuple, Callable, Awaitable

from jinja2 import StrictUndefined, Environment
from pydantic import Field, BaseModel

from eidolon_sdk.cpu.llm_message import UserMessageText, UserMessage, LLMMessage, AssistantMessage
from eidolon_sdk.impl.tot_controller.prompts import PROPOSE_PROMPT, COT_PROMPT
from eidolon_sdk.reference_model import Specable


class BaseThoughtGenerationStrategyConfig(BaseModel):
    pass


class BaseThoughtGenerationStrategy(Specable[BaseThoughtGenerationStrategyConfig]):
    """
    Base class for a thought generation strategy.
    """
    env = Environment(undefined=StrictUndefined)

    c: int = 3
    """The number of children thoughts to propose at each step."""

    def build_prompt(self, user_message, prompt: Dict[str, str], thoughts_path: Tuple[str, ...], n: int):
        preamble_txt = self.env.from_string(prompt["preamble"]).render(thoughts=thoughts_path, n=n)
        thoughts_txt = self.env.from_string(prompt["thoughts"]).render(thoughts=thoughts_path, n=n)
        post_amble_txt = self.env.from_string(prompt["post-amble"]).render(thoughts=thoughts_path, n=n)
        messages = [UserMessage(content=[UserMessageText(text=preamble_txt)]),
                    user_message,
                    UserMessage(content=[UserMessageText(text=thoughts_txt)]),
                    UserMessage(content=[UserMessageText(text=post_amble_txt)])]
        return messages

    @abstractmethod
    async def next_thought(
        self,
        user_message: UserMessage,
        llm_call: Callable[[List[LLMMessage], Dict[str, Any]], Awaitable[str]],
        thoughts_path: Tuple[str, ...] = (),
    ) -> str:
        """
        Generate the next thought given the problem description and the thoughts
        generated so far.
        """


class SampleCoTStrategyOutput(BaseModel):
    thought: str


class SampleCoTStrategy(BaseThoughtGenerationStrategy):
    """
    Sample thoughts from a Chain-of-Thought (CoT) prompt.

    This strategy works better when the thought space is rich, such as when each
    thought is a paragraph. Independent and identically distributed samples
    lead to diversity, which helps to avoid repetition.
    """

    prompt: Dict[str, str] = COT_PROMPT

    async def next_thought(
        self,
        user_message: UserMessage,
        llm_call: Callable[[List[LLMMessage], Dict[str, Any]], Awaitable[AssistantMessage]],
        thoughts_path: Tuple[str, ...] = (),
    ) -> str:
        messages = self.build_prompt(user_message, self.prompt, thoughts_path, self.c)
        next_thought = await llm_call(messages, SampleCoTStrategyOutput.model_json_schema())
        return next_thought.content["thought"]


class ProposeOutputFormat(BaseModel):
    thoughts: List[str]


class ProposePromptStrategy(BaseThoughtGenerationStrategy):
    """
    Propose thoughts sequentially using a "propose prompt".

    This strategy works better when the thought space is more constrained, such
    as when each thought is just a word or a line. Proposing different thoughts
    in the same prompt completion helps to avoid duplication.
    """

    prompt: Dict[str, str] = PROPOSE_PROMPT
    tot_memory: Dict[Tuple[str, ...], List[str]] = Field(default_factory=dict)

    async def next_thought(
        self,
        user_message: UserMessage,
        llm_call: Callable[[List[LLMMessage], Dict[str, Any]], Awaitable[AssistantMessage]],
        thoughts_path: Tuple[str, ...] = (),
    ) -> str:
        if thoughts_path not in self.tot_memory or not self.tot_memory[thoughts_path]:
            messages = self.build_prompt(user_message, self.prompt, thoughts_path, self.c)
            next_thought_msg = await llm_call(messages, ProposeOutputFormat.model_json_schema())
            new_thoughts = next_thought_msg.content["thoughts"]
            self.tot_memory[thoughts_path] = new_thoughts[::-1]
        return self.tot_memory[thoughts_path].pop()
