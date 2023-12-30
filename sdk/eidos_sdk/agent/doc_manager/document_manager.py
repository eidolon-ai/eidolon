import logging

import uuid
from pydantic import BaseModel, Field
from typing import List

from eidos_sdk.agent.doc_manager.loaders.base_loader import BaseLoader, FileInfo
from eidos_sdk.agent.doc_manager.parsers.auto_parser import AutoParser
from eidos_sdk.agent.doc_manager.parsers.base_parser import BaseParser
from eidos_sdk.agent.doc_manager.transformer.auto_transformer import AutoTransformer
from eidos_sdk.agent.doc_manager.transformer.document_transformer import BaseDocumentTransformer
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.system.reference_model import Specable, AnnotatedReference, Reference


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
    loader: Reference[BaseLoader]
    parser: AnnotatedReference[BaseParser, AutoParser]
    splitter: AnnotatedReference[BaseDocumentTransformer, AutoTransformer]


class DocumentManager(Specable[DocumentManagerSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.loader = self.spec.loader.instantiate()
        self.loader.name = self.spec.name
        self.parser = self.spec.parser.instantiate()
        self.splitter = self.spec.splitter.instantiate()
        self.logger = logging.getLogger("eidolon")

    async def _addFile(self, file_info: FileInfo):
        try:
            docs = self.parser.parse(file_info.data)
            docs = list(self.splitter.transform_documents(docs))
            for doc in docs:
                doc.id = str(uuid.uuid4())
            await AgentOS.similarity_memory.add(f"doc_contents_{self.spec.name}", docs)
        except Exception as e:
            self.logger.warning(f"Failed to parse file {file_info.path}: {e}")

    async def _removeFile(self, file_info: FileInfo):
        # get the doc ids for the file
        docs = await AgentOS.symbolic_memory.find_one(f"doc_contents_{self.spec.name}", {"file_path": file_info.path})
        for doc in docs:
            # remove the docs from similarity memory
            await AgentOS.similarity_memory.delete(f"doc_contents_{self.spec.name}", doc.id)

    async def list_files(self):
        return self.loader.list_files()

    async def sync_docs(self):
        changes = await self.loader.load_changes()
        async for file_info in changes.added_files:
            await self._addFile(file_info)

        async for file_info in changes.removed_files:
            await self._removeFile(file_info)

        async for file_info in changes.modified_files:
            await self._removeFile(file_info)
            await self._addFile(file_info)
