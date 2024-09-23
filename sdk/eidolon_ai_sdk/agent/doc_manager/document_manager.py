import asyncio
import logging
from typing import List

import time
from opentelemetry import trace
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


tracer = trace.get_tracer(__name__)


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
    """
    Manages a collection of documents and provides search functionality. Automatically embeds and syncs documents (
    provided by loader) into similarity memory where they can be searched.
    """

    name: str = Field(description="The name of the document manager (used to name database collections).")
    recheck_frequency: int = Field(default=60, description="The number of seconds between checks.")
    loader: AnnotatedReference[DocumentLoader]
    concurrency: int = Field(default=8, description="The number of concurrent tasks to run.")
    doc_processor: AnnotatedReference[DocumentProcessor]


class DocumentManager(Specable[DocumentManagerSpec]):
    """
    Manages a collection of documents and provides search functionality. Automatically embeds and syncs documents
    """

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

            add_count = remove_count = replace_count = 0
            tasks = set()
            with tracer.start_as_current_span("syncing docs"):
                async for change in self.loader.get_changes(data):
                    while len(tasks) > self.spec.concurrency:
                        _, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

                    if isinstance(change, AddedFile):
                        tasks.add(asyncio.create_task(self.processor.addFile(self.collection_name, change.file_info)))
                        add_count += 1
                    elif isinstance(change, ModifiedFile):
                        tasks.add(
                            asyncio.create_task(self.processor.replaceFile(self.collection_name, change.file_info))
                        )
                        replace_count += 1
                    elif isinstance(change, RemovedFile):
                        tasks.add(asyncio.create_task(self.processor.removeFile(self.collection_name, change.file_path)))
                        remove_count += 1
                    else:
                        logger.warning(f"Unknown change type {change}")
                if add_count:
                    self.logger.info(f"Adding {add_count} files...")
                if replace_count:
                    self.logger.info(f"Replacing {replace_count} files...")
                if remove_count:
                    self.logger.info(f"Removing {remove_count} files...")

                await asyncio.gather(*tasks)
                self.logger.info("Document Manager sync complete")
            self.last_reload = time.time()
