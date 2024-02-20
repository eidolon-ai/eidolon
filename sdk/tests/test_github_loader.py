import pytest

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import AddedFile
from eidolon_ai_sdk.agent.doc_manager.loaders.github_loader import GitHubLoader, GitHubLoaderSpec


@pytest.fixture
def github_loader():
    return GitHubLoader(GitHubLoaderSpec(owner="eidolon-ai", repo="eidolon", pattern="sdk/**/*.py"))


@pytest.mark.vcr()
async def test_list_files(github_loader):
    files = [f async for f in github_loader.list_files()]
    assert "sdk/tests/conftest.py" in files


@pytest.mark.vcr()
async def test_get_changes(github_loader):
    num_files = len([f async for f in github_loader.list_files()])
    changes = [c async for c in github_loader.get_changes({})]
    assert len(changes) == num_files
    metadata = {c.file_info.path: c.file_info.metadata for c in changes}
    for c in changes:
        assert isinstance(c, AddedFile)
    updates = [c async for c in github_loader.get_changes(metadata)]
    assert not updates
