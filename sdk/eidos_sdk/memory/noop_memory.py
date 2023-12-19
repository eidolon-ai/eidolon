from typing import Any, Optional, List, Dict, Union

from eidos_sdk.memory.agent_memory import FileMemory, SymbolicMemory, VectorMemory, VectorMemorySpec
from eidos_sdk.memory.document import EmbeddedDocument
from eidos_sdk.memory.vector_store import VectorStore, QueryItem
from eidos_sdk.system.reference_model import Reference
from eidos_sdk.util.class_utils import fqn


class NoopFileMemory(FileMemory):
    def start(self):
        pass

    def stop(self):
        pass

    async def read_file(self, file_path: str) -> bytes:
        pass

    async def write_file(self, file_path: str, file_contents: bytes) -> None:
        pass

    def delete_file(self, file_path: str) -> None:
        pass

    def mkdir(self, directory: str, exist_ok: bool = False):
        pass

    def exists(self, file_name: str):
        pass


class NoopSymbolicMemory(SymbolicMemory):
    def start(self):
        pass

    def stop(self):
        pass

    async def count(self, symbol_collection: str, query: dict[str, Any]) -> int:
        return 0

    def find(
        self,
        symbol_collection: str,
        query: dict[str, Any],
        projection: Union[List[str], Dict[str, int]] = None,
        sort: dict = None,
        skip: int = None,
    ):
        pass

    async def find_one(self, symbol_collection: str, query: dict[str, Any]) -> Optional[dict[str, Any]]:
        pass

    async def insert(self, symbol_collection: str, documents: list[dict[str, Any]]) -> None:
        pass

    async def insert_one(self, symbol_collection: str, document: dict[str, Any]) -> None:
        pass

    async def upsert_one(self, symbol_collection: str, document: dict[str, Any], query: dict[str, Any]) -> None:
        pass

    async def update_many(self, symbol_collection: str, query: dict[str, Any], document: dict[str, Any]) -> None:
        pass

    async def delete(self, symbol_collection, query):
        pass


class NoopVectorStore(VectorStore):
    def start(self):
        pass

    def stop(self):
        pass

    async def add(self, collection: str, docs: List[EmbeddedDocument], **add_kwargs: Any):
        pass

    async def delete(self, collection: str, doc_ids: List[str], **delete_kwargs: Any):
        pass

    async def query(
        self,
        collection: str,
        query: List[float],
        num_results: int,
        metadata_where: Dict[str, str],
    ) -> List[QueryItem]:
        pass


class NoopVectorMemory(VectorMemory):
    def __init__(self, file_memory: FileMemory, **kwargs):
        super().__init__(
            file_memory=file_memory, spec=VectorMemorySpec(vector_store=Reference(implementation=fqn(NoopVectorStore)))
        )
