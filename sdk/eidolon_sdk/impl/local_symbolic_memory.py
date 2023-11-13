from typing import Any, List, Optional

from agent_memory import SymbolicMemory


class LocalSymbolicMemory(SymbolicMemory):
    def __init__(self, **data):
        super().__init__(**data)
        self.store = {}

    def start(self):
        self.store = {}

    def stop(self):
        self.store.clear()

    def _matches_query(self, document, query):
        return all(document.get(k) == v for k, v in query.items())

    def find(self, symbol_collection: str, query: dict[str, Any]) -> List[dict[str, Any]]:
        return [doc for doc in self.store.get(symbol_collection, []) if self._matches_query(doc, query)]

    def find_one(self, symbol_collection: str, query: dict[str, Any]) -> Optional[dict[str, Any]]:
        for doc in self.store.get(symbol_collection, []):
            if self._matches_query(doc, query):
                return doc
        return None

    def insert(self, symbol_collection: str, documents: List[dict[str, Any]]) -> None:
        if symbol_collection not in self.store:
            self.store[symbol_collection] = []
        self.store[symbol_collection].extend(documents)

    def insert_one(self, symbol_collection: str, document: dict[str, Any]) -> None:
        if symbol_collection not in self.store:
            self.store[symbol_collection] = []
        self.store[symbol_collection].append(document)

    def upsert_one(self, symbol_collection: str, document: dict[str, Any], query: dict[str, Any]) -> None:
        existing_document = self.find_one(symbol_collection, query)
        if existing_document is not None:
            self.store[symbol_collection].remove(existing_document)
        self.insert_one(symbol_collection, document)