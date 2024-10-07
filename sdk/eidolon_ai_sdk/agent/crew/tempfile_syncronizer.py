import os
from contextlib import asynccontextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.agent_os_interfaces import FileMetadata


@asynccontextmanager
async def sync_temp_loc(identifier: str):
    with TemporaryDirectory() as tempdir:
        existing = await _read(tempdir, identifier)
        yield Path(tempdir)
        written = await _write(tempdir, tempdir, identifier)
    for deleted in  existing.difference(written):
        await AgentOS.file_memory.delete_file(str(Path(identifier) / deleted))


async def _read(loc, write_loc):
    acc = set()
    async for record in AgentOS.file_memory.glob(str(Path(write_loc)/"*")):
        record = cast(FileMetadata, record)
        relative_path = Path(record.file_path).relative_to(write_loc)
        found = await AgentOS.file_memory.read_file(record.file_path)
        with open(loc / relative_path, "wb") as f:
            f.write(found)
        acc.add(relative_path)
    return acc


async def _write(root, loc, write_loc):
    acc = set()
    relative_loc = Path(root).relative_to(loc)
    await AgentOS.file_memory.mkdir(str(Path(write_loc) / relative_loc), exist_ok=True)
    for path in os.listdir(loc):
        item_loc = str(Path(loc) / path)
        item_relative_loc = str(relative_loc / path)
        if os.path.isfile(item_loc):
            with open(item_loc, 'rb') as f:
                write_loc = str(Path(write_loc) / item_relative_loc)
                await AgentOS.file_memory.write_file(write_loc, f.read())
            acc.add(item_relative_loc)
        else:
            acc.union(await _write(root, item_loc, write_loc))
    return acc
