import asyncio
import fnmatch
import os
import tempfile
from asyncio import Task
from contextlib import asynccontextmanager
from typing import AsyncContextManager, Optional
from typing import AsyncIterator, Dict, Any
from typing import List

import certifi
from dulwich import porcelain
from dulwich.client import get_transport_and_path, default_urllib3_manager
from dulwich.objects import Commit, Tree
from dulwich.refs import SYMREF
from dulwich.repo import Repo
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
    FileChange, LoaderMetadata, RootMetadata,
)
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.system.specable import Specable
from eidolon_ai_sdk.util.async_wrapper import make_async


class GitHubLoaderSpec(DocumentLoaderSpec):
    """
    Deprecated. Will be removed at a later version.

    Use GitHubLoaderV2 instead
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
    def __init__(self, *args, **kwargs):
        logger.warning("GitHubLoader is deprecated. Use GitHubLoaderV2 instead")
        super().__init__(*args, **kwargs)

    async def get_changes(self, metadata: LoaderMetadata) -> AsyncIterator[FileChange]:
        logger.warning("GitHubLoader is deprecated. Use GitHubLoaderV2 instead")
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


# dulwich requires these to be set
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['CURL_CA_BUNDLE'] = certifi.where()


class GitHubLoaderV2Spec(DocumentLoaderSpec):
    """
    Loads files from a GitHub repository. Note that you will likely hit rate limits on all but the smallest repositories
    unless a TOKEN is provided
    """

    url: str = Field(examples=["https://github.com/eidolon-ai/eidolon.git", "https://{GITHUB_TOKEN}@github.com/eidolon-ai/eidolon.git"], description="URL of the repository. Will be templated with envars.")
    branch: str = "main"
    pattern: str | List[str] = "**"
    exclude: str | List[str] = []
    diff_depth: int = 100

    def templated_url(self) -> str:
        return self.url.format_map(os.environ)


class GitHubLoaderV2(DocumentLoader, Specable[GitHubLoaderV2Spec]):
    url: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.spec.templated_url()

    async def get_changes(self, metadata: LoaderMetadata, current_commit_override: Optional[str] = None) -> AsyncIterator[FileChange]:
        pattern = set(self.spec.pattern if isinstance(self.spec.pattern, list) else [self.spec.pattern])
        excluded = set(self.spec.exclude if isinstance(self.spec.exclude, list) else [self.spec.exclude])

        found_pattern = set(metadata.root_metadata.get('pattern', []))
        found_excluded = set(metadata.root_metadata.get('exclude', []))

        current_commit = current_commit_override or await self.get_current_head()
        new_root_metadata = RootMetadata({'pattern': list(pattern), 'exclude': list(excluded)})

        if 'commit' in metadata.root_metadata and metadata.root_metadata['commit'] == current_commit:
            logger.info("No changes detected")
        elif not metadata.root_metadata.get('commit') or found_pattern != pattern or found_excluded != excluded:
            logger.info("Initializing loader with current commit as root commit.")
            async with self._temp_repo(current_commit, 1) as repo:
                new_root_metadata.metadata['commit'] = repo.head().decode('ascii')
                async for change in self.from_uninitialized(repo, metadata):
                    yield change
            yield new_root_metadata
        else:
            async with self._temp_repo(current_commit, self.spec.diff_depth) as repo:
                new_root_metadata.metadata['commit'] = repo.head().decode('ascii')
                logger.info(f"Loading changes from commit {metadata.root_metadata['commit']} to {current_commit}")
                try:
                    old_commit: Optional[Commit] = repo[metadata.root_metadata['commit'].encode('ascii')]
                    found_commit = True
                except KeyError:
                    found_commit = False
                if found_commit:
                    async for change in self.from_commit(repo, old_commit):
                        yield change
                else:
                    logger.warning(f"Commit {metadata.root_metadata['commit']} not found in history (depth={self.spec.diff_depth})")
                    async for change in self.from_uninitialized(repo, metadata):
                        yield change
            yield new_root_metadata

    @make_async
    def get_current_head(self) -> str:
        client, path = get_transport_and_path(self.url)
        refs = client.get_refs(path)

        for ref, sha in refs.items():
            if ref == b'HEAD':
                return sha.decode('ascii')

        raise ValueError(f"No HEAD found for branch {self.spec.branch}")

    async def from_uninitialized(self, repo: Repo, metadata: LoaderMetadata) -> AsyncIterator[FileChange]:
        # if we are here we don't expect files, but there are edge cases where this is possible
        existing_files = {doc.path: doc.metadata async for doc in metadata.doc_metadata()}

        commit: Commit = repo[repo.head()]
        tree: Tree = repo[commit.tree]

        # Walk the tree and yield all files
        for entry in tree.iteritems():
            file_path = entry.path.decode()
            if not self._matches(file_path):
                continue

            blob = repo[entry.sha]

            existing = existing_files.pop(file_path, None)
            if existing:
                if existing['sha'] != entry.sha.decode('ascii'):
                    yield ModifiedFile(FileInfo(
                        path=file_path,
                        metadata={'sha': entry.sha.decode('ascii')},
                        data=DataBlob(blob.data)
                    ))
            else:
                yield AddedFile(FileInfo(
                    path=file_path,
                    metadata={'sha': entry.sha.decode('ascii')},
                    data=DataBlob(blob.data)
                ))

        for file_path in existing_files.keys():
            yield RemovedFile(file_path)

    async def from_commit(self, repo: Repo, old_commit: Commit) -> AsyncIterator[FileChange]:
        current_commit: Commit = repo[repo.head()]
        # Get the changes between commits
        changes = repo.object_store.tree_changes(
            old_commit.tree,
            current_commit.tree,
        )

        for (oldpath, newpath), (oldmode, newmode), (oldsha, newsha) in changes:
            if not self._matches(newpath.decode()):
                newpath = None
            if oldpath and newpath is None:
                yield RemovedFile(oldpath.decode())
            else:
                blob = repo[newsha]
                file_info = FileInfo(
                    path=newpath.decode(),
                    metadata={'mode': newmode},
                    data=DataBlob(blob.data)
                )
                yield AddedFile(file_info) if oldpath is None else ModifiedFile(file_info)

    @asynccontextmanager
    async def _temp_repo(self, current_commit: str, depth: int) -> AsyncContextManager[Repo]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo: Repo = await self._clone(tmp_dir, depth)
            try:
                yield repo
            finally:
                repo.close()

    @make_async
    def _clone(self, tmp_dir, depth) -> Repo:
        return porcelain.clone(
            self.url,
            target=tmp_dir,
            depth=depth,
            branch=self.spec.branch,
            checkout=True,
        )

    def _matches(self, path: str) -> bool:
        if self.spec.pattern == "**" and not self.spec.exclude:
            return True

        pattern = set(self.spec.pattern if isinstance(self.spec.pattern, list) else [self.spec.pattern])
        excluded = set(self.spec.exclude if isinstance(self.spec.exclude, list) else [self.spec.exclude])

        matched = any(fnmatch.fnmatch(path, p) for p in pattern)
        return matched and not any(fnmatch.fnmatch(path, e) for e in excluded)
