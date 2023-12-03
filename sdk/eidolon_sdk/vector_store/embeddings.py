from abc import ABC, abstractmethod
from typing import Sequence, Any, Literal

import openai
from pydantic import BaseModel, Field

from eidolon_sdk.reference_model import Specable
from eidolon_sdk.vector_store.document import Document, EmbeddedDocument


class EmbeddingSpec(BaseModel):
    pass


class Embedding(ABC, Specable[EmbeddingSpec]):
    def __init__(self, spec: EmbeddingSpec):
        self.spec = spec

    @abstractmethod
    def embed_text(self, text: str, **kwargs: Any) -> Sequence[float]:
        """Create an embedding for a single piece of text.

        Args:
            text: The text to be encoded.

        Returns:
            An embedding for the text.
        """

    def embed(self, documents: Sequence[Document], **kwargs: Any) -> Sequence[EmbeddedDocument]:
        """Create embeddings for a list of documents.

        Args:
            documents: A sequence of Documents to be encoded.

        Returns:
            A sequence of EmbeddedDocuments.
        """
        for document in documents:
            yield EmbeddedDocument(
                id=document.id,
                embedding=self.embed_text(document.page_content, **kwargs),
                metadata=document.metadata,
            )


class OpenAIEmbeddingSpec(EmbeddingSpec):
    model: Literal[
        'text-embedding-davinci-001',
        'text-embedding-babbage-001',
        'text-embedding-curie-001',
        'text-embedding-ada-001',
    ] = Field(default='text-embedding-babbage-001', description="The name of the model to use.")


class OpenAIEmbedding(Embedding, Specable[OpenAIEmbeddingSpec]):
    def __init__(self, spec: OpenAIEmbeddingSpec):
        super().__init__(spec)
        self.spec = spec

    def embed_text(self, text: str, **kwargs: Any) -> Sequence[float]:
        response = openai.Embedding.create(
            input=text,
            model=self.spec.model  # Choose the model as per your requirement
        )

        embedding_vector = response['data'][0]['embedding']
        return embedding_vector
