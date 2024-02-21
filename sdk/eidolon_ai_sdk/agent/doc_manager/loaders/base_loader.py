import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Dict, Any, AsyncIterator

from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.system.reference_model import Specable


@dataclass
class FileInfo:
    path: str
    metadata: Dict[str, Any]
    data: DataBlob


@dataclass
class AddedFile:
    file_info: FileInfo


@dataclass
class ModifiedFile:
    file_info: FileInfo


@dataclass
class RemovedFile:
    file_path: str


FileChange = AddedFile | ModifiedFile | RemovedFile


class DocumentLoaderSpec(BaseModel):
    pass


class DocumentLoader(ABC, Specable[DocumentLoaderSpec]):
    logger = logging.getLogger("eidolon")

    @abstractmethod
    async def get_changes(self, metadata: Dict[str, Dict[str, Any]]) -> AsyncIterator[FileChange]:
        pass

    @abstractmethod
    async def list_files(self) -> AsyncIterator[str]:
        pass
