import asyncio
import json
from pathlib import Path
from typing import cast, Optional, Dict, Tuple
from uuid import uuid4

from pydantic import BaseModel

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.memory.file_memory import FileMemory
from eidolon_ai_sdk.system.reference_model import Specable


class FileHandle(BaseModel):
    machineURL: str
    process_id: str
    file_id: str


class ProcessFileSystemSpec(BaseModel):
    root: str = "processes"


class ProcessFileSystem(Specable[ProcessFileSystemSpec]):
    root: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = self.spec.root

    def file_memory(self):
        return cast(FileMemory, AgentOS.file_memory)

    async def start(self):
        """
        Starts the memory implementation.
        """
        pass

    async def stop(self):
        """
        Stops the memory implementation.
        """
        pass

    async def read_file(self, process_id: str, file_id: str) -> Optional[Tuple[bytes, Optional[Dict[str, any]]]]:
        """
        Reads the contents of a file for the given process_id and file_id
        :param process_id:
        :param file_id:
        :return:
        """
        path = str(Path(self.root, process_id, file_id))
        exists = await self.file_memory().exists(path)
        if not exists:
            return None
        file_md = None
        if await self.file_memory().exists(path + ".md"):
            file_md = json.loads((await self.file_memory().read_file(path + ".md")).decode())
        return await self.file_memory().read_file(path), file_md

    async def write_file(self, process_id: str, file_contents: bytes, file_md: Optional[Dict[str, any]] = None) -> str:
        """
        Writes the given `file_contents` to a new file within the context of the process_id.
        :param file_md:
        :param process_id:
        :param file_contents:
        :return:
        """
        file_id = uuid4().hex
        await self.file_memory().mkdir(str(Path(self.root, process_id)), exist_ok=True)
        await self.file_memory().write_file(str(Path(self.root, process_id, file_id)), file_contents)
        md_to_write = {
            "process_id": process_id,
            "file_id": file_id
        }
        if file_md:
            md_to_write.update(file_md)
        path = str(Path(self.root, process_id, file_id + ".md"))
        await self.file_memory().write_file(path, json.dumps(md_to_write).encode())
        return file_id

    async def delete_file(self, process_id: str, file_id: str):
        """
        Deletes the file specified by `file_id` within the context of the process_id.
        :param process_id:
        :param file_id:
        :return:
        """
        path = str(Path(self.root, process_id, file_id))
        exists = await self.file_memory().exists(path)
        if not exists:
            return None
        await self.file_memory().delete_file(path)
        return "deleted"

    async def list_files(self, process_id: str, include_only_index: bool):
        path = Path(self.root, process_id)
        files = await AgentOS.file_memory.glob(f"{path}/*.md")
        for file in files:
            contents = await AgentOS.file_memory.read_file(file)
            file_md = json.loads(contents)
            if not include_only_index or ("indexed" in file_md and file_md["indexed"]):
                yield file_md

    @classmethod
    async def delete_process(cls, process_id: str):
        """
        Deletes the entire process directory
        :param process_id:
        :return:
        """
        memory: FileMemory = AgentOS.file_memory
        pfs: ProcessFileSystem = AgentOS.process_file_system
        process_path = str(Path(pfs.root, process_id))
        found = await memory.glob(f"{process_path}/**/*")
        await asyncio.gather(*[memory.delete_file(file) for file in found])
