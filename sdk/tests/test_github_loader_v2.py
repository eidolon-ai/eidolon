import pytest

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import AddedFile, LoaderMetadata
from eidolon_ai_sdk.agent.doc_manager.loaders.github_loader import GitHubLoaderV2, \
    GitHubLoaderV2Spec


@pytest.fixture
def github_loader():
    return GitHubLoaderV2(
        GitHubLoaderV2Spec(url="https://github.com/eidolon-ai/eidolon.git", pattern="sdk/pyproject.toml")
    )


def md(metadata: dict = None, files: list = None):
    metadata = metadata or {}
    files = files or []
    async def yielder():
        for f in files:
            yield f

    return LoaderMetadata(metadata, yielder)


# @pytest.mark.vcr()
async def test_can_load_repo(github_loader: GitHubLoaderV2):
    changes = [c async for c in github_loader.get_changes(md())]
    assert len(changes) == 2
