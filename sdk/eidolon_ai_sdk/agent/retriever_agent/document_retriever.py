from typing import List, AsyncIterable

from pydantic import BaseModel

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.system.reference_model import Specable


class DocumentRetrieverSpec(BaseModel):
    pass


class DocumentRetriever(Specable[DocumentRetrieverSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)

    async def get_docs(self, vector_collection_name: str, doc_ids: List[str]) -> AsyncIterable[Document]:
        pass


class SimilarityMemoryRetriever(DocumentRetriever):
    async def get_docs(self, vector_collection_name: str, doc_ids: List[str]) -> AsyncIterable[Document]:
        return AgentOS.similarity_memory.get_docs(vector_collection_name, doc_ids)
