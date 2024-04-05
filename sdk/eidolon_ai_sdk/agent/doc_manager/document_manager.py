import asyncio
import logging
from typing import List

import time
from pydantic import BaseModel, Field

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent.doc_manager.document_processor import DocumentProcessor
from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import (
    DocumentLoader,
    RemovedFile,
    ModifiedFile,
    AddedFile,
)
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
    doc_processor: AnnotatedReference[DocumentProcessor]


class DocumentManager(Specable[DocumentManagerSpec]):
    last_reload = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.loader = self.spec.loader.instantiate()
        self.loader.name = self.spec.name
        self.logger = logging.getLogger("eidolon")
        self.processor = self.spec.doc_processor.instantiate()
        self.collection_name = f"doc_sync_{self.spec.name}"

    async def list_files(self):
        return self.loader.list_files()

    async def sync_docs(self, force: bool = False):
        if force or self.last_reload + self.spec.recheck_frequency < time.time():
            self.logger.info(f"Syncing files from {self.spec.name}")

            self.last_reload = time.time()
            data = {}
            async for file in AgentOS.symbolic_memory.find(self.collection_name, {}):
                data[file["file_path"]] = file["data"]

            self.logger.info(f"Found {len(data)} files in symbolic memory")

            tasks = []
            async for change in self.loader.get_changes(data):
                if isinstance(change, AddedFile):
                    tasks.append(self.processor.addFile(self.collection_name, change.file_info))
                elif isinstance(change, ModifiedFile):
                    tasks.append(self.processor.replaceFile(self.collection_name, change.file_info))
                elif isinstance(change, RemovedFile):
                    tasks.append(self.processor.removeFile(self.collection_name, change.file_path))
                else:
                    logger.warning(f"Unknown change type {change}")
            await asyncio.gather(*tasks)
            self.last_reload = time.time()
