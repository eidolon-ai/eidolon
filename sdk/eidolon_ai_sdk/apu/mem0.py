import asyncio
from typing import cast, List

from bson import ObjectId
from mem0 import Memory
from mem0.embeddings.base import EmbeddingBase
from mem0.llms.base import LLMBase
from mem0.memory.telemetry import capture_event
from mem0.vector_stores.base import VectorStoreBase
from qdrant_client.http.models import ScoredPoint

from eidolon_ai_client.events import StringOutputEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.agent_os_interfaces import SimilarityMemory
from eidolon_ai_sdk.apu.llm_unit import LLMUnit
from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.memory.noop_memory import NoopVectorStore


class Mem0LLM(LLMBase):
    llm_unit: LLMUnit

    def __init__(self, llm_unit: LLMUnit):
        self.llm_unit = llm_unit

    def generate_response(self, messages) -> str:
        return asyncio.run(self._generate_response(messages))

    async def _generate_response(self, messages) -> str:
        acc = []
        messages = [m.model_dump() for m in messages]
        async for event in self.llm_unit.execute_llm(messages, tools=[], output_format="str"):
            if event.is_root_and_type(StringOutputEvent):
                acc.append(cast(event, StringOutputEvent).content)

        return "".join(acc)


class Mem0Embedding(EmbeddingBase):
    def embed(self, text) -> List[float]:
        return asyncio.run(self._embed(text))

    async def _embed(self, text):
        return await AgentOS.similarity_memory.embed_text(text)


class Mem0VectorDB(VectorStoreBase):
    def __init__(self):
        pass

    @property
    def vs(self) -> SimilarityMemory:
        if isinstance(AgentOS.similarity_memory, NoopVectorStore):
            logger.warning("Using NoopVectorStore. Mem0 vectordb will not work.")
        return AgentOS.similarity_memory

    def create_col(self, name, vector_size, distance):
        pass

    def insert(self, name, vectors, payloads=None, ids=None):
        return asyncio.run(self._insert(ids, name, payloads, vectors))

    async def _insert(self, ids, name, payloads, vectors):
        payloads = payloads or [None] * len(vectors)
        ids = ids or [ObjectId() for _ in range(len(vectors))]
        docs = [
            Document(id=str(vector_id), embedding=vector, page_content=payload)
            for vector, payload, vector_id in zip(vectors, payloads, ids)
        ]
        return await self.vs.add(collection=name, docs=docs)

    def search(self, name, query, limit=5, filters=None) -> List[ScoredPoint]:
        return asyncio.run(self._search(filters, limit, name, query))

    async def _search(self, filters, limit, name, query):
        found: List[Document] = await self.vs.query(collection=name, query=query, num_results=limit,
                                                    metadata_where=filters)
        return [
            ScoredPoint(
                id=doc.id,
                score=0.0,
                vector=doc.embedding,
                payload=doc.metadata
            )
            for doc in found
        ]

    def delete(self, name, vector_id):
        return asyncio.run(self._delete(name, vector_id))

    async def _delete(self, name, vector_id):
        return await self.vs.delete(collection=name, doc_ids=[str(vector_id)])

    def update(self, name, vector_id, vector=None, payload=None):
        ...

    def get(self, name, vector_id):
        return asyncio.run(self._get(name, vector_id))

    async def _get(self, name, vector_id):
        async for doc in self.vs.get_docs(collection=name, doc_ids=[str(vector_id)]):
            return doc

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
        ...


class Mem0DB:
    def __init__(self, collection: str):
        self.collection = collection

    def add_history(self, memory_id, prev_value, new_value, event, is_deleted=0):
        asyncio.run(self._add_history(event, is_deleted, memory_id, new_value, prev_value))

    async def _add_history(self, event, is_deleted, memory_id, new_value, prev_value):
        memory_id = memory_id or str(ObjectId())
        return await AgentOS.symbolic_memory.insert_one(
            self.collection,
            dict(memory_id=memory_id, prev_value=prev_value, new_value=new_value, event=event, is_deleted=is_deleted)
        )

    def get_history(self, memory_id):
        return asyncio.run(self._get_history(memory_id))

    async def _get_history(self, memory_id):
        acc = []
        async for doc in AgentOS.symbolic_memory.find(self.collection, {"memory_id": memory_id}):
            doc['id'] = doc.pop('_id')
            acc.append(doc)
        return acc

    def reset(self):
        logger.warning("history table is not resettable")
        pass


class EidolonMem0(Memory):
    def __init__(self, llm: LLMUnit, db_collection: str):
        self.embedding_model = Mem0Embedding()
        self.vector_store = Mem0VectorDB()
        self.llm = Mem0LLM(llm)
        self.db = Mem0DB(db_collection)
        self.collection_name = db_collection
        capture_event("mem0.init", self)
