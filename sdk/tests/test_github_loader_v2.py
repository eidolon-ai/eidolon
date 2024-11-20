from typing import List

import pytest

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import LoaderMetadata, AddedFile, RootMetadata, \
    FileInfoMetadata, FileInfo, ModifiedFile, RemovedFile
from eidolon_ai_sdk.agent.doc_manager.loaders.github_loader import GitLoader, \
    GitLoaderSpec


@pytest.fixture
def github_loader():
    return GitLoader(
        GitLoaderSpec(url="https://github.com/eidolon-ai/typedai.git")
    )


def md(metadata: dict = None, files: List[FileInfoMetadata] = None):
    metadata = metadata or {}
    files = files or []
    async def yielder():
        for f in files:
            yield f

    return LoaderMetadata(metadata, yielder)


@pytest.mark.vcr()
async def test_can_load_repo(github_loader: GitLoader):
    changes = [c async for c in github_loader.get_changes(md())]
    assert len(changes) > 40
    grouped = {}
    for c in changes:
        grouped.setdefault(type(c), []).append(c)
    assert len(grouped[AddedFile]) == len(changes) - 1
    assert len(grouped[RootMetadata]) == 1
    assert "commit" in grouped[RootMetadata][0].metadata


@pytest.mark.vcr()
async def test_reload_is_noop(github_loader: GitLoader):
    changes = [c async for c in github_loader.get_changes(md())]
    assert len(changes) > 40

    grouped = {}
    for c in changes:
        grouped.setdefault(type(c), []).append(c)

    changes = [c async for c in github_loader.get_changes(md(metadata=grouped[RootMetadata][0].metadata))]
    assert len(changes) == 0


@pytest.mark.vcr()
async def test_reloads_only_changed_files(github_loader: GitLoader):
    files = [c.file_info async for c in github_loader.get_changes(md()) if isinstance(c, AddedFile)]

    # remove 3 so 3 appears added
    files = files[:-3]

    # modify two
    files[0].metadata['sha'] = "bad"
    files[1].metadata['sha'] = "bad"

    # add one to appear removed
    files.append(FileInfo(path="foopath", metadata={"sha": "shouldn't matter"}, data=None))

    files = [FileInfoMetadata(path=a.path, metadata=a.metadata) for a in files]

    changes = [c async for c in github_loader.get_changes(md(files=files))]
    grouped = {}
    for c in changes:
        grouped.setdefault(type(c), []).append(c)

    assert len(grouped[AddedFile]) == 3
    assert len(grouped[ModifiedFile]) == 2
    assert len(grouped[RemovedFile]) == 1
