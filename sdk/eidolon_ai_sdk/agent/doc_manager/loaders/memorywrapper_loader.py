import asyncio
import hashlib
from typing import AsyncIterator, Optional, Dict

from dateutil.tz import tzutc
from opentelemetry import trace

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import (
    DocumentLoader,
    FileInfo,
    DocumentLoaderSpec,
    FileChange,
    ModifiedFile,
    AddedFile,
    RemovedFile, LoaderMetadata,
)
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.agent_os_interfaces import FileMetadata
from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.specable import Specable

tracer = trace.get_tracer("memory wrapper loader")


def hash_file(chunk: bytes):
    hasher = hashlib.sha256()
    hasher.update(chunk)
    return hasher.hexdigest()


class WrappedMemoryLoaderSpec(DocumentLoaderSpec):
    """
    Use a FileMemory implementation to load files. Relies on file metadata to handle change detection with manual
    hashing as a fallback.
    """

    memory: Reference[FileMemoryBase]
    pattern: str = "**"
    concurrency: int = 16


# noinspection PyShadowingNames
class WrappedMemoryLoader(DocumentLoader, Specable[WrappedMemoryLoaderSpec]):
    memory: FileMemoryBase

    def __init__(self, spec: WrappedMemoryLoaderSpec, **kwargs: object):
        super().__init__(spec, **kwargs)
        self.memory = spec.memory.instantiate()

    async def start(self):
        await self.memory.start()

    async def get_changes(self, metadata: LoaderMetadata) -> AsyncIterator[FileChange]:
        metadata_mapping: Dict[str, FileMetadata] = {}
        async for doc in metadata.doc_metadata():
            md = FileMetadata(**doc.metadata)
            if md.updated:
                md.updated = md.updated.replace(tzinfo=tzutc())
            metadata_mapping[doc.path] = md

        tasks = set()
        async for file in self.memory.glob(self.spec.pattern):
            while len(tasks) >= self.spec.concurrency:
                done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    change_record = task.result()
                    if change_record:
                        yield change_record

            if file.file_path in metadata_mapping:
                tasks.add(
                    asyncio.create_task(self._process_existing_file(file, metadata_mapping[file.file_path]))
                )
                del metadata_mapping[file.file_path]
            else:
                tasks.add(asyncio.create_task(self._process_new_file(file)))

        for not_found in metadata_mapping.keys():
            yield RemovedFile(not_found)
        while tasks:
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                change_record = task.result()
                if change_record:
                    yield change_record

    async def _process_new_file(self, file: FileMetadata):
        with tracer.start_as_current_span("reading file"):
            file_path = file.file_path
            data = await self.memory.read_file(file_path)
            file.extra["loader_hash"] = hash_file(data)
            if file.updated:  # convert to utc for storage
                file.updated = file.updated.astimezone(tz=tzutc())
            return AddedFile(FileInfo(file_path, file.model_dump(), DataBlob.from_bytes(data, path=file_path)))

    async def _process_existing_file(self, file: FileMetadata, saved_metadata: FileMetadata):
        with tracer.start_as_current_span("process existing file"):
            file_path = file.file_path
            data: Optional[bytes] = None
            if saved_metadata.hash:
                changed = saved_metadata.hash != file.hash
            elif saved_metadata.updated:
                changed = saved_metadata.updated != file.updated
            elif "loader_hash" in saved_metadata.extra:
                data = await self.memory.read_file(file_path)
                loader_hash = hash_file(data)
                file.extra["loader_hash"] = loader_hash
                changed = loader_hash != saved_metadata.extra["loader_hash"]
            else:
                changed = True
            if changed:
                if not data:
                    data = await self.memory.read_file(file_path)
                if "loader_hash" not in file.extra:
                    file.extra["loader_hash"] = hash_file(data)
                return ModifiedFile(FileInfo(file_path, file.model_dump(), DataBlob.from_bytes(data, path=file_path)))
            else:
                return None
