from typing import Optional, List, Dict, Sequence, Iterable

from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.memory.vector_store import VectorStore, QueryItem


class NoopVectorStore(VectorStore):
    async def start(self):
        pass

    async def stop(self):
        pass

    async def add(self, collection: str, docs: Sequence[Document]):
        pass

    async def delete(self, collection: str, doc_ids: List[str]):
        pass

    async def query(
        self, collection: str, query: str, num_results: int, metadata_where: Optional[Dict[str, str]] = None
    ) -> List[Document]:
        return []

    async def raw_query(
        self,
        collection: str,
        query: List[float],
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
        include_embeddings: bool = False,
    ) -> List[QueryItem]:
        pass

    async def get_docs(self, collection: str, doc_ids: List[str]) -> Iterable[Document]:
        pass
