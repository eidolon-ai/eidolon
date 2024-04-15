from abc import abstractmethod
from typing import List, Dict, Optional, Sequence, Any, Iterable

from pydantic import Field, BaseModel

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.memory.document import Document, EmbeddedDocument
from eidolon_ai_sdk.memory.vector_store import QueryItem, VectorStore
from eidolon_ai_sdk.system.reference_model import Specable


class FileSystemVectorStoreSpec(BaseModel):
    root_document_directory: str = Field(
        default="vector_memory",
        description="The root directory where the vector memory will store documents.",
    )


class FileSystemVectorStore(VectorStore, Specable[FileSystemVectorStoreSpec]):
    def __init__(self, spec: FileSystemVectorStoreSpec):
        super().__init__(spec)
        self.spec = spec

    async def start(self):
        await AgentOS.file_memory.mkdir(self.spec.root_document_directory, exist_ok=True)

    async def stop(self):
        pass

    @abstractmethod
    async def add_embedding(self, collection: str, docs: List[EmbeddedDocument], **add_kwargs: Any):
        pass

    @abstractmethod
    async def delete_embedding(self, collection: str, doc_ids: List[str], **delete_kwargs: Any):
        pass

    @abstractmethod
    async def get_metadata(self, collection: str, doc_ids: List[str]):
        pass

    @abstractmethod
    async def query_embedding(
        self,
        collection: str,
        query: List[float],
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
        include_embeddings: bool = False,
    ) -> List[QueryItem]:
        pass

    async def add(self, collection: str, docs: Sequence[Document]):
        await AgentOS.file_memory.mkdir(self.spec.root_document_directory + "/" + collection, exist_ok=True)
        # Asynchronously collect embedded documents
        embeddedDocs = []
        async for embeddedDoc in AgentOS.similarity_memory.embed(docs):
            embeddedDocs.append(embeddedDoc)
        await self.add_embedding(collection, embeddedDocs)
        for doc in docs:
            await AgentOS.file_memory.write_file(
                self.spec.root_document_directory + "/" + collection + "/" + doc.id,
                doc.page_content.encode(),
            )

    async def delete(self, collection: str, doc_ids: List[str]):
        await self.delete_embedding(collection, doc_ids)
        for doc_id in doc_ids:
            await AgentOS.file_memory.delete_file(self.spec.root_document_directory + "/" + collection + "/" + doc_id)

    async def query(
        self,
        collection: str,
        query: str,
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
    ) -> List[Document]:
        text = await AgentOS.similarity_memory.embed_text(query)
        results = await self.query_embedding(collection, text, num_results, metadata_where, False)
        returnDocuments = []
        for result in results:
            returnDocuments.append(
                Document(
                    id=result.id,
                    metadata=result.metadata,
                    page_content=await AgentOS.file_memory.read_file(
                        self.spec.root_document_directory + "/" + collection + "/" + result.id
                    ).decode(),
                )
            )
        return returnDocuments

    async def raw_query(
        self,
        collection: str,
        query: List[float],
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
        include_embeddings: bool = False,
    ) -> List[QueryItem]:
        return await self.query_embedding(collection, query, num_results, metadata_where, include_embeddings)

    async def get_docs(self, collection: str, doc_ids: List[str]) -> Iterable[Document]:
        metadatas = await self.get_metadata(collection, doc_ids)
        for i, doc_id in enumerate(doc_ids):
            content = await AgentOS.file_memory.read_file(
                self.spec.root_document_directory + "/" + collection + "/" + doc_id
            )
            yield Document(
                id=doc_id,
                metadata=metadatas[i],
                page_content=content.decode(),
            )
