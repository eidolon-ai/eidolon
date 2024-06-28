import os

import pytest

from eidolon_ai_sdk.memory.azure_file_memory import AzureFileMemory, AzureFileMemorySpec
from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.memory.local_file_memory import LocalFileMemoryConfig, LocalFileMemory
from eidolon_ai_sdk.memory.s3_file_memory import S3FileMemory


def file_memory(tmp_path, **kwargs):
    return LocalFileMemory(spec=LocalFileMemoryConfig(root_dir=tmp_path))


def s3_memory(test_name, **kwargs):
    os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "secret_not_needed_with_saved_cassettes")
    os.environ.setdefault("AWS_ACCESS_KEY_ID", "key_not_needed_with_saved_cassettes")
    return S3FileMemory(bucket="eidolon.test.file." + test_name.replace("_", "-").replace("[", "").replace("]", ""))


def azure_memory(test_name, **kwargs):
    return AzureFileMemory(spec=AzureFileMemorySpec(
        account_url="https://eidolon.blob.core.windows.net",
        container="eidolon-test-file-" + test_name.replace("_", "-").replace("[", "").replace("]", ""),
        create_container_on_startup=True))


@pytest.mark.parametrize("memory_", [file_memory, s3_memory, azure_memory])
class TestFileMemory:
    @pytest.fixture()
    async def memory(self, tmp_path, test_name, memory_):
        m = memory_(tmp_path=tmp_path, test_name=test_name)
        await m.start()
        try:
            yield m
        finally:
            await m.stop()

    @pytest.mark.vcr
    async def test_exists(self, memory: FileMemoryBase):
        assert not await memory.exists("foo")

    @pytest.mark.vcr
    async def test_create(self, memory: FileMemoryBase):
        await memory.write_file("foo", file_contents=b"FOO")
        assert await memory.exists("foo")

    @pytest.mark.vcr
    async def test_read(self, memory: FileMemoryBase):
        await memory.write_file("foo", file_contents=b"FOO")
        assert await memory.read_file("foo") == b"FOO"

    @pytest.mark.vcr
    async def test_delete(self, memory: FileMemoryBase):
        await memory.write_file("foo", file_contents=b"FOO")
        await memory.delete_file("foo")
        assert not await memory.exists("foo")

    @pytest.mark.vcr
    async def test_glob(self, memory: FileMemoryBase):
        await memory.write_file("bar.py", file_contents=b"FOO")
        assert [f.file_path async for f in memory.glob("**.py")] == ["bar.py"]
