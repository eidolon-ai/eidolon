from typing import Any, List, Optional, Dict, AsyncIterable, Sequence, AsyncGenerator

from pydantic import BaseModel

from eidolon_ai_sdk.agent_os_interfaces import SimilarityMemory
from eidolon_ai_sdk.memory.document import Document, EmbeddedDocument
from eidolon_ai_sdk.memory.embeddings import Embedding
from eidolon_ai_sdk.memory.vector_store import VectorStore, QueryItem
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class SimilarityMemorySpec(BaseModel):
    embedder: AnnotatedReference[Embedding]
    vector_store: AnnotatedReference[VectorStore]


class SimilarityMemoryImpl(Specable[SimilarityMemorySpec], SimilarityMemory):
    embedder: Embedding
    vector_store: VectorStore

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.embedder = self.spec.embedder.instantiate()
        self.vector_store = self.spec.vector_store.instantiate()

    async def start(self):
        await self.embedder.start()
        await self.vector_store.start()

    async def stop(self):
        await self.embedder.stop()
        await self.vector_store.stop()

    async def embed_text(self, text: str, **kwargs: Any) -> List[float]:
        """Create an embedding for a single piece of text.

        Args:
            text: The text to be encoded.

        Returns:
            An embedding for the text.
        """
        return await self.embedder.embed_text(text, **kwargs)

    def embed(self, documents: Sequence[Document], **kwargs: Any) -> AsyncGenerator[EmbeddedDocument, None]:
        """
        Create embeddings for a list of documents.
        :param documents:
        :param kwargs:
        :return:
        """
        return self.embedder.embed(documents, **kwargs)

    async def add(self, collection: str, docs: Sequence[Document]):
        return await self.vector_store.add(collection, docs)

    async def delete(self, collection: str, doc_ids: List[str]):
        return await self.vector_store.delete(collection, doc_ids)

    async def query(
        self,
        collection: str,
        query: str,
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
    ) -> List[Document]:
        return await self.vector_store.query(collection, query, num_results, metadata_where)

    async def raw_query(
        self,
        collection: str,
        query: List[float],
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
        include_embeddings: bool = False,
    ) -> List[QueryItem]:
        return await self.vector_store.raw_query(collection, query, num_results, metadata_where, include_embeddings)

    def get_docs(self, collection: str, doc_ids: List[str]) -> AsyncIterable[Document]:
        return self.vector_store.get_docs(collection, doc_ids)
