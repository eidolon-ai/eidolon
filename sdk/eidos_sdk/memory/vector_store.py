from abc import ABC, abstractmethod
from typing import Optional, List, Any, Dict

from pydantic import BaseModel, Field

from eidos_sdk.memory.document import EmbeddedDocument


class QueryItem(BaseModel):
    id: str = Field(description="The unique identifier for the document")
    metadata: dict = Field(default_factory=dict, description="The metadata of the document.")
    distance: float = Field(description="The score of the document.")
    embedding: Optional[List[float]] = Field(description="The embedding of the document.")


class VectorStore(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    async def add(self, collection: str, docs: List[EmbeddedDocument], **add_kwargs: Any):
        pass

    @abstractmethod
    async def delete(self, collection: str, doc_ids: List[str], **delete_kwargs: Any):
        pass

    @abstractmethod
    async def query(
        self,
        collection: str,
        query: List[float],
        num_results: int,
        metadata_where: Dict[str, str],
    ) -> List[QueryItem]:
        pass
