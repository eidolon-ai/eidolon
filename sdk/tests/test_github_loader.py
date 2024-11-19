import pytest

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import LoaderMetadata, AddedFile
from eidolon_ai_sdk.agent.doc_manager.loaders.github_loader import GitHubLoader, GitHubLoaderSpec


def md(metadata: dict = None, files: list = None):
    metadata = metadata or {}
    files = files or []
    async def yielder():
        for f in files:
            yield f

    return LoaderMetadata(metadata, yielder)


@pytest.fixture
def github_loader():
    return GitHubLoader(
        GitHubLoaderSpec(owner="eidolon-ai", repo="eidolon", pattern="sdk/**/conftest.py", root_path="sdk/tests")
    )


@pytest.mark.vcr()
async def test_get_changes(github_loader):
    changes = [c async for c in github_loader.get_changes(md())]
    assert len(changes) == 1
    assert type(changes[0]) == AddedFile
    assert changes[0].file_info.path == "sdk/tests/conftest.py"
