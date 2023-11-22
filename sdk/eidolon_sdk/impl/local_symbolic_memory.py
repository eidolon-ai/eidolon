from typing import Any, List, Optional

from eidolon_sdk.agent_memory import SymbolicMemory


_DB = {}


class LocalSymbolicMemory(SymbolicMemory):
    implementation: str = "local_symbolic_memory"

    def start(self):
        _DB = {}

    def stop(self):
        _DB.clear()

    def _matches_query(self, document, query):
        # Handle MongoDB-like query operations.
        for k, v in query.items():
            if isinstance(v, dict):
                if any(op in v for op in ["$eq", "$ne", "$lt", "$lte", "$gt", "$gte"]):
                    if not self._evaluate_query_op(document.get(k), v):
                        return False
                else:
                    return self._matches_query(document.get(k), v)
            elif not document.get(k) == v:
                return False
        return True

    def _evaluate_query_op(self, doc_value, query_value):
        for op, val in query_value.items():
            if op == "$eq":
                if doc_value != val:
                    return False
            elif op == "$ne":
                if doc_value == val:
                    return False
            elif op == "$lt":
                if doc_value >= val:
                    return False
            elif op == "$lte":
                if doc_value > val:
                    return False
            elif op == "$gt":
                if doc_value <= val:
                    return False
            elif op == "$gte":
                if doc_value < val:
                    return False
        return True

    async def count(self, symbol_collection: str, query: dict[str, Any]) -> int:
        return len([doc for doc in _DB.get(symbol_collection, []) if self._matches_query(doc, query)])

    async def find(self, symbol_collection: str, query: dict[str, Any]):
        for doc in [doc for doc in _DB.get(symbol_collection, []) if self._matches_query(doc, query)]:
            yield doc

    async def find_one(self, symbol_collection: str, query: dict[str, Any]) -> Optional[dict[str, Any]]:
        for doc in _DB.get(symbol_collection, []):
            if self._matches_query(doc, query):
                return doc
        return None

    async def insert(self, symbol_collection: str, documents: List[dict[str, Any]]) -> None:
        if symbol_collection not in _DB:
            _DB[symbol_collection] = []
        _DB[symbol_collection].extend(documents)

    async def insert_one(self, symbol_collection: str, document: dict[str, Any]) -> None:
        if symbol_collection not in _DB:
            _DB[symbol_collection] = []
        _DB[symbol_collection].append(document)

    def _apply_update_modifiers(self, existing_document, modifiers):
        for op, change in modifiers.items():
            if op == "$set":
                for field, value in change.items():
                    existing_document[field] = value
            elif op == "$unset":
                for field in change:
                    existing_document.pop(field, None)
            elif op == "$push":
                for field, value in change.items():
                    if field not in existing_document:
                        existing_document[field] = []
                    if isinstance(value, dict) and "$each" in value:
                        existing_document[field].extend(value["$each"])
                    else:
                        existing_document[field].append(value)
            elif op == "$pop":
                for field, value in change.items():
                    if field in existing_document and isinstance(existing_document[field], list):
                        if value == 1:
                            existing_document[field].pop()
                        elif value == -1:
                            existing_document[field].pop(0)
            elif op == "$pull":
                for field, value in change.items():
                    if field in existing_document and isinstance(existing_document[field], list):
                        existing_document[field] = [item for item in existing_document[field] if item != value]

    async def upsert_one(self, symbol_collection: str, document: dict[str, Any], query: dict[str, Any]) -> None:
        global _DB
        existing_document = await self.find_one(symbol_collection, query)
        if existing_document is not None:
            self._apply_update_modifiers(existing_document, document)
            _DB[symbol_collection].append(existing_document)
        else:
            await self.insert_one(symbol_collection, document)

    async def update_many(self, symbol_collection: str, query: dict[str, Any], document: dict[str, Any]) -> None:
        global _DB
        for doc in _DB.get(symbol_collection, []):
            if self._matches_query(doc, query):
                self._apply_update_modifiers(doc, document)

    async def delete(self, symbol_collection, query):
        for doc in _DB.get(symbol_collection, []):
            if self._matches_query(doc, query):
                _DB[symbol_collection].remove(doc)

