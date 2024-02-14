from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Sequence, AsyncIterable

from eidolon_ai_sdk.memory.document import Document


class QueryItem(BaseModel):
    id: str = Field(description="The unique identifier for the document")
    metadata: dict = Field(default_factory=dict, description="The metadata of the document.")
    score: float = Field(description="The score of the document.")
    embedding: Optional[List[float]] = Field(description="The embedding of the document.")


class VectorStore(ABC):
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def add(self, collection: str, docs: Sequence[Document]):
        pass

    @abstractmethod
    async def delete(self, collection: str, doc_ids: List[str]):
        pass

    @abstractmethod
    async def query(
        self,
        collection: str,
        query: str,
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
    ) -> List[Document]:
        pass

    @abstractmethod
    async def raw_query(
        self,
        collection: str,
        query: List[float],
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
        include_embeddings: bool = False,
    ) -> List[QueryItem]:
        pass

    @abstractmethod
    def get_docs(self, collection: str, doc_ids: List[str]) -> AsyncIterable[Document]:
        pass
