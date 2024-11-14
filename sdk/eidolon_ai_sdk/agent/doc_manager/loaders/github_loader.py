import asyncio
import fnmatch
import os
from asyncio import Task
from typing import AsyncIterator, List
from typing import Dict, Any, Optional

from dulwich import client
from httpx import AsyncClient
from pydantic import Field

from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.stream_collector import merge_streams
from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import (
    DocumentLoaderSpec,
    DocumentLoader,
    FileInfo,
    AddedFile,
    ModifiedFile,
    RemovedFile,
    FileChange, LoaderMetadata,
)
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.system.specable import Specable
from eidolon_ai_sdk.util.async_wrapper import make_async


class GitHubLoaderSpec(DocumentLoaderSpec):
    """
    Loads files from a GitHub repository. Note that you will likely hit rate limits on all but the smallest repositories
    unless a TOKEN is provided
    """

    owner: str
    repo: str
    client_args: dict = {}
    root_path: Optional[str] = None
    pattern: str | List[str] = "**"
    exclude: str | List[str] = []
    token: Optional[str] = Field(
        default_factory=lambda: os.environ.get("GITHUB_TOKEN"),
        description="Github token, can also be set via envar 'GITHUB_TOKEN'",
    )

    def root_content(self):
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{self.root_path or ''}"


class GitHubLoader(DocumentLoader, Specable[GitHubLoaderSpec]):
    async def get_changes(self, metadata: LoaderMetadata) -> AsyncIterator[FileChange]:
        metadata = {doc.path: doc.metadata async for doc in metadata.doc_metadata()}
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
        token_ = self.spec.token
        if not token_:
            logger.warning("No token provided for GitHubLoader and GITHUB_TOKEN not set in environment.")
        headers = {"Authorization": f"Bearer {token_}"} if token_ else None
        response = await client.get(url=url or self.spec.root_content(), headers=headers)
        # response = await client.get(url=url or self.spec.root_content())
        response.raise_for_status()
        streams = []
        patterns = self.spec.pattern if isinstance(self.spec.pattern, list) else [self.spec.pattern]
        excluded = self.spec.exclude if isinstance(self.spec.exclude, list) else [self.spec.exclude]
        for record in response.json():
            if record["type"] == "file":
                matched = False
                for p in patterns:
                    if fnmatch.fnmatch(record["path"], p):
                        matched = True
                        break
                if matched:
                    for e in excluded:
                        if fnmatch.fnmatch(record["path"], e):
                            matched = False
                            break
                if matched:
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


class GitHubLoaderV2Spec(DocumentLoaderSpec):
    """
    Loads files from a GitHub repository. Note that you will likely hit rate limits on all but the smallest repositories
    unless a TOKEN is provided
    """

    url: str = Field(examples=["https://github.com/eidolon-ai/eidolon.git", "https://{GITHUB_TOKEN}@github.com/eidolon-ai/eidolon.git"], description="URL of the repository. Will be templated with envars.")
    pattern: str | List[str] = "**"
    exclude: str | List[str] = []

    def templated_url(self) -> str:
        return self.url.format_map(os.environ)


class GitHubLoaderV2(DocumentLoader, Specable[GitHubLoaderV2Spec]):
    async def get_changes(self, metadata: LoaderMetadata) -> AsyncIterator[FileChange]:
        depth = None
        if 'rev' in metadata.root_metadata:
            try:
                depth = await self.get_commit_depth(metadata.root_metadata['rev'])
            except _HistoryNotFound:
                logger.warning(f"{metadata.root_metadata['rev']} not found in repository")

        if depth is None:
            logger.info("Initialising metadata")
            #  todo: clone repo and get all diffs
            yield None
        elif depth >= 1:
            logger.info('Getting changes')
            #  todo get changes since last commit
        elif depth == 0:
            logger.info("No changes detected")
        else:  # should not be possible
            logger.error("Unexpected depth scenario")

    @make_async
    def get_commit_depth(self, rev1, rev2="HEAD"):
        c = client.get_transport_and_path(url)[0]

        # Get commit history
        walker = c.get_graph_walker()
        commits = list(walker)

        # Find positions of commits
        try:
            pos1 = next(i for i, c in enumerate(commits) if c.id == rev1)
            pos2 = next(i for i, c in enumerate(commits) if c.id == rev2)
        except StopIteration:
            raise _HistoryNotFound("Commit not found")

        return abs(pos2 - pos1)


class _HistoryNotFound(Exception):
    pass


