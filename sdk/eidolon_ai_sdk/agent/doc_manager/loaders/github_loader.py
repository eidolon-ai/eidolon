import asyncio
import fnmatch
import os
import tempfile
from asyncio import Task
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any
from typing import List
from typing import Optional

import certifi
from dulwich import porcelain
from dulwich.client import get_transport_and_path
from dulwich.objects import Tree
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

    Use [GitLoader](/docs/components/documentloader/gitloader) instead
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
        logger.warning("GitHubLoader is deprecated. Use GitLoader instead")
        super().__init__(*args, **kwargs)

    async def get_changes(self, metadata: LoaderMetadata) -> AsyncIterator[FileChange]:
        logger.warning("GitHubLoader is deprecated. Use GitLoader instead")
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


class GitLoaderSpec(DocumentLoaderSpec):
    """
    Loads files from a git repository. Uses raw git protocols, so this is not a GitHub specific implementation.
    """

    url: str = Field(examples=["https://github.com/eidolon-ai/eidolon.git", "https://{GITHUB_TOKEN}@github.com/eidolon-ai/eidolon.git"],
                     description="URL for source repository. Will be templated with envars.")
    branch: str = Field("HEAD", description="Branch, ref, or commit to load files from.")
    pattern: str | List[str] = Field("**", description="Blob pattern(s) of files to include.")
    exclude: str | List[str] = Field([], description="Blob pattern(s) of files to exclude. Calculated after pattern (ei, files from pattern are selected, then any matching exclude are removed).")

    def templated_url(self) -> str:
        return self.url.format_map(os.environ)


class GitLoader(DocumentLoader, Specable[GitLoaderSpec]):
    _inited: bool = False
    url: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.spec.templated_url()
        self._init()

    @classmethod
    def _init(cls):
        if not cls._inited:
            # dulwich requires these to be set
            os.environ['SSL_CERT_FILE'] = certifi.where()
            os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
            os.environ['CURL_CA_BUNDLE'] = certifi.where()
            cls._inited = True

    @asynccontextmanager
    async def with_repo(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo: Repo = await make_async(porcelain.clone)(
                self.url,
                target=tmp_dir,
                depth=1,
                bare=True,
                filter_spec="blob:none",
            )
            try:
                yield repo
            finally:
                repo.close()

    async def get_changes(self, metadata: LoaderMetadata) -> AsyncIterator[FileChange]:
        pattern = set(self.spec.pattern if isinstance(self.spec.pattern, list) else [self.spec.pattern])
        excluded = set(self.spec.exclude if isinstance(self.spec.exclude, list) else [self.spec.exclude])

        found_pattern = set(metadata.root_metadata.get('pattern', []))
        found_excluded = set(metadata.root_metadata.get('exclude', []))

        current_commit = await self.get_current_head()

        commit_matches = 'commit' in metadata.root_metadata and metadata.root_metadata['commit'] == current_commit
        if commit_matches and found_pattern == pattern and found_excluded == excluded:
            logger.info("No changes detected")
        else:
            async with self.with_repo() as repo:
                # Since we are doing bare checkout, we don't actually have the data loaded.
                # We fetch the blobs lazily that way we do not need to download irrelevant files
                blobless_changes = []
                async for change in self._get_changes(
                        metadata,
                        repo,
                        repo[repo[current_commit.encode('ascii')].tree],
                        {doc.path: doc.metadata async for doc in metadata.doc_metadata()}
                ):
                    if isinstance(change, AddedFile) or isinstance(change, ModifiedFile):
                        blobless_changes.append(change)
                    else:
                        yield change

                if blobless_changes:
                    wants = [f.file_info.metadata['sha'].encode('ascii') for f in blobless_changes]
                    client, path = get_transport_and_path(self.url)
                    writer, done, abort = repo.object_store.add_pack()
                    try:
                        await make_async(client.fetch_pack)(
                            path,
                            determine_wants=lambda refs: wants,
                            graph_walker=NullGraphWalker(),
                            pack_data=writer.write,
                        )
                        done()
                    except Exception:
                        abort()
                        raise
                    for change in blobless_changes:
                        yield await self._transform_change(change, repo)

                yield RootMetadata({'commit': current_commit, 'pattern': list(pattern), 'exclude': list(excluded)})

    @make_async
    def _transform_change(self, change, repo):
        data_bytes = repo[change.file_info.metadata['sha'].encode('ascii')].data
        change.file_info.data = DataBlob.from_bytes(data_bytes, path=change.file_info.path)
        return change

    @make_async
    def get_current_head(self) -> str:
        client, path = get_transport_and_path(self.url)
        refs = client.get_refs(path)
        branch_ref = self.spec.branch.encode('ascii')
        if branch_ref in refs:
            return refs[branch_ref].decode('ascii')

        branch_ref = f"refs/heads/{self.spec.branch}".encode('ascii')
        if branch_ref in refs:
            return refs[branch_ref].decode('ascii')

        raise ValueError(f"Neither Ref {branch_ref} nor Ref {self.spec.branch} found")

    async def _get_changes(
            self,
            metadata: LoaderMetadata,
            repo: Repo,
            tree: Tree,
            existing_files,
            delete_remaining=True,
            parent: Optional[str] = None,
    ) -> AsyncIterator[FileChange]:
        for entry in tree.iteritems():
            file_path = entry.path.decode()
            full_path = parent + '/' + file_path if parent else file_path
            if entry.mode == 0o040000:  # is directory check
                async for change in self._get_changes(
                    metadata,
                    repo=repo,
                    tree=repo[entry.sha],
                    existing_files=existing_files,
                    delete_remaining=False,
                    parent=full_path,
                ):
                    yield change
            elif self._matches(full_path):
                existing = existing_files.pop(full_path, None)
                sha_str = entry.sha.decode('ascii')
                if existing:
                    if existing['sha'] != sha_str:
                        yield ModifiedFile(FileInfo(
                            path=full_path,
                            metadata={'sha': sha_str},
                            data=None
                        ))
                    else:
                        logger.debug("Skipping unchanged file", full_path)
                else:
                    yield AddedFile(FileInfo(
                        path=full_path,
                        metadata={'sha': sha_str},
                        data=None
                    ))
            else:
                logger.debug("Skipping non-matching file", full_path)

        if delete_remaining:
            for p in existing_files.keys():
                yield RemovedFile(p)

    def _matches(self, path: str) -> bool:
        if self.spec.pattern == "**" and not self.spec.exclude:
            return True

        pattern = set(self.spec.pattern if isinstance(self.spec.pattern, list) else [self.spec.pattern])
        excluded = set(self.spec.exclude if isinstance(self.spec.exclude, list) else [self.spec.exclude])

        matched = any(fnmatch.fnmatch(path, p) for p in pattern)
        return matched and not any(fnmatch.fnmatch(path, e) for e in excluded)


class NullGraphWalker:
    """A graph walker that always returns no commits."""
    def __init__(self):
        self.shallow = set()

    def __next__(self):
        return None  # Return None instead of raising StopIteration

    def ack(self, sha):
        pass
