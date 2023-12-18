from abc import ABC, abstractmethod
from typing import Sequence, Any, Literal, AsyncGenerator

from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from eidos_sdk.system.reference_model import Specable
from eidos_sdk.memory.document import Document, EmbeddedDocument


class EmbeddingSpec(BaseModel):
    pass


class Embedding(ABC, Specable[EmbeddingSpec]):
    def __init__(self, spec: EmbeddingSpec):
        super().__init__(spec)
        self.spec = spec

    @abstractmethod
    async def embed_text(self, text: str, **kwargs: Any) -> Sequence[float]:
        """Create an embedding for a single piece of text.

        Args:
            text: The text to be encoded.

        Returns:
            An embedding for the text.
        """

    async def embed(self, documents: Sequence[Document], **kwargs: Any) -> AsyncGenerator[EmbeddedDocument, None]:
        """Create embeddings for a list of documents.

        Args:
            documents: A sequence of Documents to be encoded.

        Returns:
            A sequence of EmbeddedDocuments.
        """
        for document in documents:
            text = await self.embed_text(document.page_content, **kwargs)
            yield EmbeddedDocument(
                id=document.id,
                embedding=text,
                metadata=document.metadata,
            )


class OpenAIEmbeddingSpec(EmbeddingSpec):
    model: Literal[
        "text-embedding-davinci-001",
        "text-embedding-babbage-001",
        "text-embedding-curie-001",
        "text-embedding-ada-002",
    ] = Field(default="text-embedding-ada-002", description="The name of the model to use.")


class OpenAIEmbedding(Embedding, Specable[OpenAIEmbeddingSpec]):
    llm: AsyncOpenAI = None

    def __init__(self, spec: OpenAIEmbeddingSpec):
        super().__init__(spec)
        self.spec = spec

    async def embed_text(self, text: str, **kwargs: Any) -> Sequence[float]:
        if not self.llm:
            self.llm = AsyncOpenAI()
        response = await self.llm.embeddings.create(
            input=text,
            model=self.spec.model,  # Choose the model as per your requirement
        )

        embedding_vector = response.data[0].embedding
        return embedding_vector
