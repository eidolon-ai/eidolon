import os
from pathlib import Path

from eidolon_ai_sdk.agent.crew.tempfile_syncronizer import sync_temp_loc


async def test_sync_temp_loc_can_write_files(machine):
    async with sync_temp_loc("test_loc") as tempdir:
        with open(tempdir / "foo.txt", "wb") as f:
            f.write("bar".encode())


async def test_sync_temp_loc_can_read_files(machine):
    async with sync_temp_loc("test_loc") as tempdir:
        with open(tempdir / "foo.txt", "w") as f:
            f.write("bar")

    async with sync_temp_loc("test_loc") as tempdir2:
        assert os.path.exists(tempdir2 / "foo.txt")
        with open(tempdir2 / "foo.txt", "r") as f:
            assert f.read() == "bar"

    assert tempdir != tempdir2


async def test_syc_with_subdirs(machine):
    async with sync_temp_loc("test_loc") as tempdir:
        os.mkdir(Path(tempdir) / "foo")
        with open(Path(tempdir) / "foo" / "foo.txt", "w") as f:
            f.write("bar")

    async with sync_temp_loc("test_loc") as tempdir2:
        assert os.path.exists(Path(tempdir2) / "foo" / "foo.txt")


async def test_silos_write_by_identifier(machine):
    async with sync_temp_loc("test_loc") as tempdir:
        with open(tempdir / "foo.txt", "w") as f:
            f.write("bar")

    async with sync_temp_loc("not_test_loc") as tempdir2:
        assert not os.path.exists(tempdir2 / "foo.txt")
