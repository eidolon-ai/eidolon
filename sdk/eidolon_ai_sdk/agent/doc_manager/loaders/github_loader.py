import asyncio
import fnmatch
import os
from asyncio import Task
from typing import Dict, Any, AsyncIterator, List, Optional

from httpx import AsyncClient

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import DocumentLoaderSpec, DocumentLoader, FileInfo, \
    AddedFile, ModifiedFile, RemovedFile, FileChange
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.logger import logger
from eidolon_ai_sdk.util.stream_collector import merge_streams


class GitHubLoaderSpec(DocumentLoaderSpec):
    owner: str
    repo: str
    client_args: dict = {}
    root_path: Optional[str] = None
    pattern: str = "**/*"

    def root_content(self):
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{self.root_path or ''}"


class GitHubLoader(DocumentLoader, Specable[GitHubLoaderSpec]):
    async def list_files(self) -> AsyncIterator[str]:
        async with AsyncClient(**self.spec.client_args) as client:
            async for file in self._raw_list_files(client):
                yield file["path"]

    async def get_changes(self, metadata: Dict[str, Dict[str, Any]]) -> AsyncIterator[FileChange]:
        async with AsyncClient(**self.spec.client_args) as client:
            tasks: List[Task] = []
            async for file in self._raw_list_files(client):
                if file["path"] not in metadata:
                    tasks.append(asyncio.create_task(self._file_op(AddedFile, file, client)))
                else:
                    if metadata[file["path"]]["sha"] != file["sha"]:
                        tasks.append(asyncio.create_task(self._file_op(ModifiedFile, file, client)))
                    del metadata[file["path"]]
            while tasks:
                done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    yield await task
            for file_path in metadata:
                yield RemovedFile(file_path)

    async def _raw_list_files(self, client: AsyncClient, url=None) -> AsyncIterator[Dict[str, Any]]:
        token_ = os.environ['GITHUB_TOKEN']
        headers = {"Authorization": f"Bearer {token_}"} if token_ else None
        response = await client.get(url=url or self.spec.root_content(), headers=headers)
        # response = await client.get(url=url or self.spec.root_content())
        response.raise_for_status()
        streams = []
        for record in response.json():
            if record["type"] == "file":
                if fnmatch.fnmatch(record["path"], self.spec.pattern):
                    yield record
                else:
                    logger.debug(f"Skipping file {record['path']}")
            elif record["type"] == "dir":
                streams.append(self._raw_list_files(client, record["url"]))
            else:
                logger.warning(f"Unknown file type: {record['type']}")
        async for e in merge_streams(streams):
            yield e

    async def _data(self, client, file):
        response = await client.get(file["download_url"])
        response.raise_for_status()
        data = await response.aread()
        return DataBlob.from_bytes(data, path=file["path"])

    async def _file_op(self, op, file, client):
        new_metadata = {"sha": file["sha"], "size": file["size"], "download_url": file["download_url"]}
        return op(FileInfo(file["path"], new_metadata, await self._data(client, file)))
