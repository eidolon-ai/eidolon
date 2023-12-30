import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Dict, Any, AsyncIterable, Annotated, Iterable

from eidos_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.system.reference_model import Specable


@dataclass
class FileInfo:
    path: str
    metadata: Dict[str, Any]
    data: DataBlob


@dataclass
class FileChangeset:
    added_files: AsyncIterable[FileInfo]
    modified_files: AsyncIterable[FileInfo]
    removed_files: AsyncIterable[str]


class BaseLoaderSpec(BaseModel):
    name: str
    recheck_frequency: int = Field(default=60, description="The number of seconds between checks.")


class BaseLoader(ABC, Specable[BaseLoaderSpec]):
    logger = logging.getLogger("eidolon")
    last_reload = 0
    name = None

    @abstractmethod
    async def get_changes(self, metadata: Dict[str, Dict[str, Any]]) -> FileChangeset:
        pass

    @abstractmethod
    async def list_files(self) -> Iterable[str]:
        pass

    async def load_changes(self, force: bool = False) -> FileChangeset:
        if force or self.last_reload + self.spec.recheck_frequency < time.time():
            self.last_reload = time.time()
            data = {}
            async for file in AgentOS.symbolic_memory.find(f"doc_sync_{self.name}", {}):
                data[file["file_path"]] = file["data"]

            self.logger.info(f"Found {len(data)} files in symbolic memory")

            ret = await self.get_changes(data)

            async def added_files():
                async for file_info in ret.added_files:
                    yield file_info
                    await AgentOS.symbolic_memory.insert_one(
                        f"doc_sync_{self.name}",
                        {
                            "file_path": file_info.path,
                            "data": file_info.metadata
                        }
                    )

            async def modified_files():
                async for file_info in ret.modified_files:
                    yield file_info
                    await AgentOS.symbolic_memory.delete(f"doc_sync_{self.name}", {"file_path": file_info.path})
                    await AgentOS.symbolic_memory.insert_one(
                        f"doc_sync_{self.name}",
                        {
                            "file_path": file_info.path,
                            "data": file_info.metadata
                        }
                    )

            async def deleted_files():
                async for file_path in ret.removed_files:
                    yield file_path
                    await AgentOS.symbolic_memory.delete(f"doc_sync_{self.name}", {"file_path": file_path})

            self.last_reload = time.time()
            
            return FileChangeset(
                added_files=added_files(),
                modified_files=modified_files(),
                removed_files=deleted_files()
            )
        else:
            async def empty_async_iterable():
                for _ in []:
                    yield _

            return FileChangeset(
                added_files=empty_async_iterable(),
                modified_files=empty_async_iterable(),
                removed_files=empty_async_iterable()
            )
