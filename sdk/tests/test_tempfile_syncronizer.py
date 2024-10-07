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
        with open(tempdir2 / "foo.txt", "r") as f:
            assert f.read() == "bar"

    assert tempdir != tempdir2
