from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.system.reference_model import Specable


class QuestionTransformerSpec(BaseModel):
    pass


class QuestionTransformer(ABC, Specable[QuestionTransformerSpec]):
    @abstractmethod
    async def transform(self, apu: APU, process_id: str, question: str) -> List[str]:
        """Transform a question into a series of related question.

        Args:
            question: The question to be transformed.

        Returns:
            The transformed questions.
            :param question:
            :param apu:
        """


class NoopQuestionTransformer(QuestionTransformer):
    async def transform(self, apu: APU, process_id: str, question: str) -> List[str]:
        return [question]
