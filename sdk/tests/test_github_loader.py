import pytest

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import LoaderMetadata
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
        GitHubLoaderSpec(owner="eidolon-ai", repo="eidolon", pattern="**/*.py")
    )


# @pytest.mark.vcr()
async def test_get_changes(github_loader):
    changes = [c async for c in github_loader.get_changes(md())]
    assert len(changes) > 300
