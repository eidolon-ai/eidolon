from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Dict, Any, AsyncIterator, AsyncGenerator

from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.system.specable import Specable


@dataclass
class FileInfoMetadata:
    path: str
    metadata: Dict[str, Any]


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


@dataclass
class RootMetadata:
    metadata: Dict[str, Any]


FileChange = AddedFile | ModifiedFile | RemovedFile | RootMetadata


class DocumentLoaderSpec(BaseModel):
    """
    Loads documents from a particular source and can check for changes.
    """

    pass


class DocumentLoader(ABC, Specable[DocumentLoaderSpec]):
    logger = logging.getLogger("eidolon")

    @abstractmethod
    async def get_changes(self, metadata: LoaderMetadata) -> AsyncIterator[FileChange]:
        pass


class LoaderMetadata:
    root_metadata: Dict[str, Any]

    def __init__(self, metadata: Dict[str, Any], doc_fn):
        self.root_metadata = metadata
        self._fn = doc_fn

    async def doc_metadata(self) -> AsyncGenerator[FileInfoMetadata]:
        async for d in self._fn():
            yield d
