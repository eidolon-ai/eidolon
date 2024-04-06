from abc import ABC, abstractmethod
from typing import Sequence, Any, AsyncGenerator, Optional, List

from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from eidolon_ai_sdk.cpu.llm.open_ai_llm_unit import ArgBuilder
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
from eidolon_ai_sdk.memory.document import Document, EmbeddedDocument


class EmbeddingSpec(BaseModel):
    pass


class Embedding(ABC, Specable[EmbeddingSpec]):
    def __init__(self, spec: EmbeddingSpec):
        super().__init__(spec)
        self.spec = spec

    @abstractmethod
    async def embed_text(self, text: str, **kwargs: Any) -> List[float]:
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

    async def start(self):
        pass

    async def stop(self):
        pass


class NoopEmbedding(Embedding, Specable[EmbeddingSpec]):
    async def embed_text(self, text: str, **kwargs: Any) -> Sequence[float]:
        return []


class OpenAIEmbeddingSpec(EmbeddingSpec):
    model: str = Field(default="text-embedding-ada-002", description="The name of the model to use.")
    client: AnnotatedReference[AsyncOpenAI]
    client_args: dict = {}
    client_arg_builder: AnnotatedReference[ArgBuilder]


class OpenAIEmbedding(Embedding, Specable[OpenAIEmbeddingSpec]):
    _llm: Optional[AsyncOpenAI] = None

    def __init__(self, spec: OpenAIEmbeddingSpec):
        super().__init__(spec)
        self.spec = spec
        self._llm = None

    async def stop(self):
        await super().stop()
        await self.llm.close()
        self._llm = None

    @property
    def llm(self) -> AsyncOpenAI:
        if not self._llm:
            client_args = self.spec.client_args
            client_args.update(self.spec.client_arg_builder.instantiate().get_args())
            self._llm = self.spec.client.instantiate(**client_args)
        return self._llm

    async def embed_text(self, text: str, **kwargs: Any) -> Sequence[float]:
        response = await self.llm.embeddings.create(
            input=text,
            model=self.spec.model,  # Choose the model as per your requirement
        )

        embedding_vector = response.data[0].embedding
        return embedding_vector
