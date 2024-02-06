import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Dict, Any, AsyncIterable, Iterable

from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.system.reference_model import Specable


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


class DocumentLoaderSpec(BaseModel):
    pass


class DocumentLoader(ABC, Specable[DocumentLoaderSpec]):
    logger = logging.getLogger("eidolon")

    @abstractmethod
    async def get_changes(self, metadata: Dict[str, Dict[str, Any]]) -> FileChangeset:
        pass

    @abstractmethod
    async def list_files(self) -> Iterable[str]:
        pass
