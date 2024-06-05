import hashlib
from typing import Dict, Any, AsyncIterator, Optional

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import (
    DocumentLoader,
    FileInfo,
    DocumentLoaderSpec,
    FileChange,
    ModifiedFile,
    AddedFile,
    RemovedFile,
)
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.agent_os_interfaces import FileMetadata
from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.system.reference_model import Specable, T, Reference


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


# noinspection PyShadowingNames
class WrappedMemoryLoader(DocumentLoader, Specable[WrappedMemoryLoaderSpec]):
    memory: FileMemoryBase

    def __init__(self, spec: T, **kwargs: object):
        super().__init__(spec, **kwargs)
        self.memory = spec.memory.instantiate()

    async def list_files(self) -> AsyncIterator[str]:
        async for file in self.memory.glob(self.spec.pattern):
            yield file.file_path

    async def get_changes(self, metadata: Dict[str, Dict[str, Any]]) -> AsyncIterator[FileChange]:
        async for file in self.memory.glob(self.spec.pattern):
            # get the file path relative to the root_dir
            file_path = file.file_path
            if file_path in metadata:
                saved_metadata: FileMetadata = FileMetadata(**metadata[file_path])
                data: Optional[bytes] = None
                if saved_metadata.updated:
                    changed = saved_metadata.updated != file.updated
                elif saved_metadata.hash:
                    changed = saved_metadata.hash != file.hash
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
                    yield ModifiedFile(FileInfo(file_path, file.model_dump(), DataBlob.from_bytes(data, path=file_path)))
                del metadata[file_path]
            else:
                data = await self.memory.read_file(file_path)
                file.extra["loader_hash"] = hash_file(data)
                yield AddedFile(FileInfo(file_path, file.model_dump(), DataBlob.from_bytes(data, path=file_path)))

        for not_found in metadata.keys():
            yield RemovedFile(not_found)
