from typing import Any, List, Optional

from eidolon_sdk.agent_memory import SymbolicMemory


_DB = {}


class LocalSymbolicMemory(SymbolicMemory):
    def start(self):
        _DB = {}

    def stop(self):
        _DB.clear()

    def _matches_query(self, document, query):
        if isinstance(query, dict):
            return all(self._matches_query(document.get(k), v) for k, v in query.items())
        else:
            return document == query

    def find(self, symbol_collection: str, query: dict[str, Any]) -> List[dict[str, Any]]:
        return [doc for doc in _DB.get(symbol_collection, []) if self._matches_query(doc, query)]

    def find_one(self, symbol_collection: str, query: dict[str, Any]) -> Optional[dict[str, Any]]:
        for doc in _DB.get(symbol_collection, []):
            if self._matches_query(doc, query):
                return doc
        return None

    def insert(self, symbol_collection: str, documents: List[dict[str, Any]]) -> None:
        if symbol_collection not in _DB:
            _DB[symbol_collection] = []
        _DB[symbol_collection].extend(documents)

    def insert_one(self, symbol_collection: str, document: dict[str, Any]) -> None:
        if symbol_collection not in _DB:
            _DB[symbol_collection] = []
        _DB[symbol_collection].append(document)

    def upsert_one(self, symbol_collection: str, document: dict[str, Any], query: dict[str, Any]) -> None:
        existing_document = self.find_one(symbol_collection, query)
        if existing_document is not None:
            _DB[symbol_collection].remove(existing_document)
        self.insert_one(symbol_collection, document)