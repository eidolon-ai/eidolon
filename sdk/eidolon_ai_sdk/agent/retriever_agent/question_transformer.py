from typing import List

from abc import ABC, abstractmethod

from pydantic import BaseModel

from eidolon_ai_sdk.system.reference_model import Specable


class QuestionTransformerSpec(BaseModel):
    pass


class QuestionTransformer(ABC, Specable[QuestionTransformerSpec]):
    @abstractmethod
    async def transform(self, question: str) -> List[str]:
        """Transform a question into a series of related question.

        Args:
            question: The question to be transformed.

        Returns:
            The transformed questions.
        """
