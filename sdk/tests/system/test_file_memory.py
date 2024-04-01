import os

import pytest

from eidolon_ai_sdk.memory.file_memory import FileMemory
from eidolon_ai_sdk.memory.local_file_memory import LocalFileMemoryConfig, LocalFileMemory
from eidolon_ai_sdk.memory.s3_file_memory import S3FileMemory


def file_memory(tmp_path, **kwargs):
    return LocalFileMemory(spec=LocalFileMemoryConfig(root_dir=tmp_path))


def s3_memory(test_name, **kwargs):
    return S3FileMemory(
        bucket="eidolon.test.file." + test_name.replace("_", "-").replace("[", "").replace("]", ""),
        kwargs=dict(aws_session_token=os.environ.get("AWS_SECRET_ACCESS_KEY") or "any_key_works_with_pre_recorded_tests")
    )


@pytest.mark.parametrize("memory_", [file_memory, s3_memory])
class TestFileMemory:
    @pytest.fixture
    async def memory(self, tmp_path, test_name, memory_):
        m = memory_(tmp_path=tmp_path, test_name=test_name)
        await m.start()
        try:
            yield m
        finally:
            await m.stop()

    @pytest.mark.vcr
    async def test_exists(self, memory: FileMemory):
        assert not await memory.exists("foo")

    @pytest.mark.vcr
    async def test_create(self, memory: FileMemory):
        await memory.write_file("foo", file_contents=b"FOO")
        assert await memory.exists("foo")

    @pytest.mark.vcr
    async def test_read(self, memory: FileMemory):
        await memory.write_file("foo", file_contents=b"FOO")
        assert await memory.read_file("foo") == b"FOO"

    @pytest.mark.vcr
    async def test_delete(self, memory: FileMemory):
        await memory.write_file("foo", file_contents=b"FOO")
        await memory.delete_file("foo")
        assert not await memory.exists("foo")

    @pytest.mark.vcr
    async def test_glob(self, memory: FileMemory):
        await memory.write_file("bar.py", file_contents=b"FOO")
        assert await memory.glob("**.py") == ["bar.py"]
