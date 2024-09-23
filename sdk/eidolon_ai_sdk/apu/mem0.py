import asyncio
from datetime import datetime
from types import SimpleNamespace
from typing import cast, List, Callable, Optional

import mem0
from bson import ObjectId
from mem0 import Memory
from mem0.embeddings.base import EmbeddingBase
from mem0.llms.base import LLMBase
from mem0.memory.telemetry import capture_event
from mem0.vector_stores.base import VectorStoreBase
from qdrant_client.http.models import ScoredPoint

from eidolon_ai_client.events import StringOutputEvent, LLMToolCallRequestEvent, ToolCall
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.agent_os_interfaces import SimilarityMemory, SymbolicMemory
from eidolon_ai_sdk.apu.llm_message import UserMessage, SystemMessage, UserMessageText
from eidolon_ai_sdk.apu.llm_unit import LLMUnit, LLMCallFunction
from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.memory.noop_memory import NoopVectorStore


class Mem0LLM(LLMBase):
    llm_unit: LLMUnit

    def __init__(self, llm_unit: LLMUnit):
        self.llm_unit = llm_unit

    def generate_response(self, messages, tools=None) -> str | dict:
        return asyncio.run(self._generate_response(messages, tools or []))

    async def _generate_response(self, messages, tools: List) -> str | dict:
        transformed_messages = []
        for m in messages:
            if m.get("role") == "user":
                transformed_messages.append(UserMessage(content=[UserMessageText(text=m["content"])]))
            elif m.get("role") == "system":
                transformed_messages.append(SystemMessage(content=m["content"]))
            else:
                raise ValueError(f"Unknown message role {m.get('role')}")
        transformed_tools = [
            LLMCallFunction(name=tool["name"], description=tool["description"], parameters=tool["parameters"])
            for tool in (t["function"] for t in tools)
        ]
        called_tools: List[ToolCall] = []
        acc = []
        async for event in self.llm_unit.execute_llm(transformed_messages, tools=transformed_tools, output_format="str"):
            if event.is_root_and_type(StringOutputEvent):
                acc.append(cast(StringOutputEvent, event).content)
            elif event.is_root_and_type(LLMToolCallRequestEvent):
                called_tools.append(cast(LLMToolCallRequestEvent, event).tool_call)

        content = "".join(acc)

        return (
            dict(content=content, tool_calls=[dict(name=tool.name, arguments=tool.arguments) for tool in called_tools])
            if tools
            else content
        )


class Mem0Embedding(EmbeddingBase):
    dims: str = "unknown"
    similarity_memory: SimilarityMemory

    def __init__(self, similarity_memory: SimilarityMemory = None):
        self.similarity_memory = similarity_memory or AgentOS.similarity_memory

    def embed(self, text) -> List[float]:
        return asyncio.run(self._embed(text))

    async def _embed(self, text):
        return await self.similarity_memory.embed_text(text)


class Mem0VectorDB(VectorStoreBase):
    similarity_memory: SimilarityMemory

    def __init__(self, similarity_memory: SimilarityMemory = None, memory_converter: Optional[Callable[[List[ScoredPoint]], List[ScoredPoint]]] = None):
        self.similarity_memory = similarity_memory or AgentOS.similarity_memory
        self.memory_converter = memory_converter

    @property
    def vs(self) -> SimilarityMemory:
        if isinstance(self.similarity_memory, NoopVectorStore):
            logger.warning("Using NoopVectorStore. Mem0 vectordb will not work.")
        return self.similarity_memory

    def create_col(self, name, vector_size, distance):
        pass

    def insert(self, name, vectors, payloads=None, ids=None):
        return asyncio.run(self._insert(ids, name, payloads, vectors))

    async def _insert(self, ids, name, payloads, vectors):
        payloads = payloads or [None] * len(vectors)
        ids = ids or [ObjectId() for _ in range(len(vectors))]
        docs = [
            Document(
                id=str(vector_id),
                embedding=vector,
                metadata={k: v for k, v in payload.items() if k != "data"},
                page_content=payload["data"],
            )
            for vector, payload, vector_id in zip(vectors, payloads, ids)
        ]
        return await self.vs.add(collection=name, docs=docs)

    def search(self, name, query, limit=5, filters=None) -> List[ScoredPoint]:
        return asyncio.run(self._search(filters, limit, name, query))

    async def _search(self, filters, limit, name, query):
        found: List[Document] = await self.vs.query(
            collection=name, query=query, num_results=limit, metadata_where=filters
        )
        acc = []
        for doc in found:
            acc.append(
                ScoredPoint(
                    id=doc.id,
                    score=doc.score,
                    payload=dict(**doc.metadata, data=doc.page_content),
                    vector=doc.embedding,
                    version=1,
                )
            )

        retDocs = [
            ScoredPoint(
                id=doc.id,
                score=doc.score,
                payload=dict(**doc.metadata, data=doc.page_content),
                vector=doc.embedding,
                version=1,
            )
            for doc in found
        ]

        if self.memory_converter:
            return self.memory_converter(retDocs)
        return retDocs

    async def _get_doc(self, name, vector_id):
        async for doc in self.vs.get_docs(collection=name, doc_ids=[str(vector_id)]):
            return doc

    def delete(self, name, vector_id):
        return asyncio.run(self._delete(name, vector_id))

    async def _delete(self, name, vector_id):
        return await self.vs.delete(collection=name, doc_ids=[str(vector_id)])

    def update(self, name, vector_id, vector=None, payload=None):
        return asyncio.run(self._update(name, payload, vector, vector_id))

    async def _update(self, name, payload, vector, vector_id):
        doc = None
        async for d in self.vs.get_docs(collection=name, doc_ids=[str(vector_id)]):
            doc = d
        if vector:
            doc.embedding = vector
        data = (payload or {}).pop("data", None)
        if payload:
            doc.metadata = payload
        if data:
            doc.page_content = data
        await self.vs.add(collection=name, docs=[doc])
        return SimpleNamespace(
            id=doc.id,
            payload=doc.metadata,
        )

    def get(self, name, vector_id):
        return asyncio.run(self._get(name, vector_id))

    async def _get(self, name, vector_id):
        try:
            async for doc in self.vs.get_docs(collection=name, doc_ids=[str(vector_id)]):
                doc.metadata["data"] = doc.page_content
                return SimpleNamespace(
                    id=doc.id,
                    payload=doc.metadata,
                )
        except FileNotFoundError:
            return None

    def list_cols(self):
        ...

    def delete_col(self, name):
        ...

    def col_info(self, name):
        return {"name": name}

    def list(self, name, filters=None, limit=100):
        """
        List all vectors in a collection.

        Args:
            name (str): Name of the collection.
            filters (dict, optional): Filters to apply. Defaults to None.
            limit (int, optional): Number of vectors to return. Defaults to 100.

        Returns:
            list: List of vectors.
        """
        return [asyncio.run(self._list(filters, limit, name))]

    async def _list(self, filters, limit, name):
        docs = await self.vs.query(collection=name, query="", num_results=limit, metadata_where=filters)
        return [
            SimpleNamespace(
                id=doc.id,
                payload=dict(**doc.metadata, data=doc.page_content),
            )
            for doc in docs
        ]


class Mem0DB:
    collection: str
    symbolic_memory: SymbolicMemory

    def __init__(self, collection: str, symbolic_memory: SymbolicMemory = None):
        self.collection = collection
        self.symbolic_memory = symbolic_memory or AgentOS.symbolic_memory

    def add_history(self, memory_id, prev_value, new_value, event, is_deleted=0):
        asyncio.run(self._add_history(event, is_deleted, memory_id, new_value, prev_value))

    async def _add_history(self, event, is_deleted, memory_id, new_value, prev_value):
        memory_id = memory_id or str(ObjectId())
        timestamp = datetime.utcnow()
        return await self.symbolic_memory.insert_one(
            self.collection,
            dict(
                memory_id=memory_id,
                prev_value=prev_value,
                new_value=new_value,
                event=event,
                is_deleted=is_deleted,
                timestamp=timestamp,
            ),
        )

    def get_history(self, memory_id):
        return asyncio.run(self._get_history(memory_id))

    async def _get_history(self, memory_id):
        acc = []
        async for doc in self.symbolic_memory.find(self.collection, {"memory_id": memory_id}):
            doc["id"] = doc.pop("_id")
            acc.append(doc)
        return acc

    def reset(self):
        logger.warning("history table is not resettable")
        pass


class EidolonMem0(Memory):
    def __init__(self, llm: LLMUnit, db_collection: str, similarity_memory: SimilarityMemory = None, symbolic_memory: SymbolicMemory = None,
                 memory_converter: Optional[Callable[[List[ScoredPoint]], List[ScoredPoint]]] = None):
        self.embedding_model = Mem0Embedding(similarity_memory)
        self.vector_store = Mem0VectorDB(similarity_memory, memory_converter)
        self.llm = Mem0LLM(llm)
        self.db = Mem0DB(db_collection, symbolic_memory)
        self.collection_name = db_collection
        capture_event("mem0.init", self)


class NoTelemetry:
    def __init__(self):
        pass

    def capture_event(self, event_name, properties=None):
        pass

    def identify_user(self, user_id, properties=None):
        pass

    def close(self):
        pass

mem0.memory.telemetry.telemetry = NoTelemetry()
