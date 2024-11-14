import asyncio
import fnmatch
import os
from asyncio import Task
from typing import Dict, Any, AsyncIterator, List, Optional

from dulwich import client
from dulwich.client import GitClient
from httpx import AsyncClient
from pydantic import Field

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
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.stream_collector import merge_streams
from eidolon_ai_sdk.util.async_wrapper import make_async


class GitHubLoaderSpec(DocumentLoaderSpec):
    """
    Loads files from a GitHub repository. Note that you will likely hit rate limits on all but the smallest repositories
    unless a TOKEN is provided
    """

    url: str = Field(examples=["https://github.com/eidolon-ai/eidolon.git", "https://{GITHUB_TOKEN}@github.com/eidolon-ai/eidolon.git"], description="URL of the repository. Will be templated with envars.")
    pattern: str | List[str] = "**"
    exclude: str | List[str] = []

    def templated_url(self) -> str:
        return self.url.format_map(os.environ)


class GitHubLoader(DocumentLoader, Specable[GitHubLoaderSpec]):
    async def get_changes(self, metadata: LoaderMetadata) -> AsyncIterator[FileChange]:
        git_client: GitClient = (await make_async(client.get_transport_and_path)("https://github.com/user/repo.git"))[0]
        updated_metadata = False

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
