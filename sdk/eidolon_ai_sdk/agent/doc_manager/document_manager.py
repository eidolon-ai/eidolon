import logging
import time
from pydantic import BaseModel, Field
from typing import List

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import DocumentLoader, FileInfo
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser
from eidolon_ai_sdk.agent.doc_manager.transformer.document_transformer import DocumentTransformer
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class SearchResult(BaseModel):
    """
    A search result is a snippet of the document that matched the query
    """

    file_name: str = Field(description="The name of the file")
    document_snippet: str = Field(description="A snippet of the document that matched the query")


class DocumentDirectory(BaseModel):
    """
    A package is a collection of python files.
    """

    directory: str = Field(description="The name of the directory")
    files: List[str] = Field(description="The files that make up the package")


class DocumentManagerSpec(BaseModel):
    name: str
    recheck_frequency: int = Field(default=60, description="The number of seconds between checks.")
    loader: AnnotatedReference[DocumentLoader]
    parser: AnnotatedReference[DocumentParser]
    splitter: AnnotatedReference[DocumentTransformer]


class DocumentManager(Specable[DocumentManagerSpec]):
    last_reload = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.loader = self.spec.loader.instantiate()
        self.loader.name = self.spec.name
        self.parser = self.spec.parser.instantiate()
        self.splitter = self.spec.splitter.instantiate()
        self.logger = logging.getLogger("eidolon")
        self.collection_name = f"doc_sync_{self.spec.name}"

    async def _addFile(self, file_info: FileInfo):
        try:
            parsedDocs = list(self.parser.parse(file_info.data))
            docs = list(self.splitter.transform_documents(parsedDocs))
            await AgentOS.symbolic_memory.insert_one(
                self.collection_name,
                {
                    "file_path": file_info.path,
                    "data": file_info.metadata,
                    "doc_ids": [doc.id for doc in docs],
                },
            )
            if len(docs) == 0:
                self.logger.warning(f"File contained no text {file_info.path}")
                return
            await AgentOS.similarity_memory.vector_store.add(f"doc_contents_{self.spec.name}", docs)
            self.logger.info(f"Added file {file_info.path}")
        except Exception as e:
            self.logger.warning(f"Failed to parse file {file_info.path}: {e}")

    async def _removeFile(self, path: str):
        # get the doc ids for the file
        file_info = await AgentOS.symbolic_memory.find_one(self.collection_name, {"file_path": path})
        if file_info is not None:
            doc_ids = file_info["doc_ids"]
            await AgentOS.similarity_memory.vector_store.delete(f"doc_contents_{self.spec.name}", doc_ids)
            await AgentOS.symbolic_memory.delete(self.collection_name, {"file_path": path})

    async def list_files(self):
        return self.loader.list_files()

    async def sync_docs(self, force: bool = False):
        if force or self.last_reload + self.spec.recheck_frequency < time.time():
            self.last_reload = time.time()
            data = {}
            async for file in AgentOS.symbolic_memory.find(self.collection_name, {}):
                data[file["file_path"]] = file["data"]

            self.logger.info(f"Found {len(data)} files in symbolic memory")

            ret = await self.loader.get_changes(data)

            async for file_info in ret.added_files:
                await self._addFile(file_info)

            async for file_info in ret.modified_files:
                await self._removeFile(file_info.path)
                await self._addFile(file_info)

            async for file_path in ret.removed_files:
                await self._removeFile(file_path)

            self.last_reload = time.time()
