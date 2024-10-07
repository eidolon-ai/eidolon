import os
import shutil
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
        yield tempdir
        written = await _write(tempdir, identifier)
    for deleted in  existing.difference(written):
        await AgentOS.file_memory.delete_file(str(Path(identifier) / deleted))


async def _read(loc, write_loc):
    acc = set()
    async for record in AgentOS.file_memory.glob(str(Path(loc)/"*")):
        record = cast(FileMetadata, record)
        relative_path = Path(record.file_path).relative_to(loc)
        acc.add(relative_path)
        found = await AgentOS.file_memory.read_file(record.file_path)
        with open(Path(write_loc) / relative_path, "wb") as f:
            f.write(found)
    return acc


async def _write(loc, write_loc, is_root=True):
    acc = set()
    await AgentOS.file_memory.mkdir(Path(write_loc) / loc, exist_ok=True)
    for path in os.listdir(loc):
        item_loc = str(Path(loc) / path)
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                await AgentOS.file_memory.write_file(str(Path(write_loc) / item_loc), f.read())
            acc.add(path if is_root else item_loc)
        else:
            acc.union(await _write(path, is_root=False))
    return acc
