from typing import Any, Optional

import numpy as np

from eidolon_sdk.agent_memory import FileMemory, SimilarityMemory, SymbolicMemory


class NoopFileMemory(FileMemory):
    def start(self):
        pass

    def stop(self):
        pass

    def read_file(self, file_path: str) -> bytes:
        pass

    def write_file(self, file_path: str, file_contents: bytes) -> None:
        pass


class NoopSymbolicMemory(SymbolicMemory):

    def start(self):
        pass

    def stop(self):
        pass

    def find(self, symbol_collection: str, query: dict[str, Any]) -> list[dict[str, Any]]:
        pass

    def find_one(self, symbol_collection: str, query: dict[str, Any]) -> Optional[dict[str, Any]]:
        pass

    def insert(self, symbol_collection: str, documents: list[dict[str, Any]]) -> None:
        pass

    def insert_one(self, symbol_collection: str, document: dict[str, Any]) -> None:
        pass

    def upsert_one(self, symbol_collection: str, document: dict[str, Any], query: dict[str, Any]) -> None:
        pass


class NoopSimilarityMemory(SimilarityMemory):
    def start(self):
        pass

    def stop(self):
        pass

    def query(self, query: np.array) -> list[dict[str, Any]]:
        pass

    def insert(self,  embedding: np.array) -> None:
        pass
