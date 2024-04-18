import asyncio
import json
from pathlib import Path
from typing import Optional, Dict, Tuple

import bson
from pydantic import BaseModel

from eidolon_ai_client.events import FileHandle
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.agent_os_interfaces import ProcessFileSystem
from eidolon_ai_sdk.system.reference_model import Specable


class ProcessFileSystemSpec(BaseModel):
    root: str = "processes"


class ProcessFileSystemImpl(Specable[ProcessFileSystemSpec], ProcessFileSystem):
    root: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = self.spec.root

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
        exists = await AgentOS.file_memory.exists(path)
        if not exists:
            return None
        file_md = None
        if await AgentOS.file_memory.exists(path + ".md"):
            file_md = json.loads((await AgentOS.file_memory.read_file(path + ".md")).decode())
        return await AgentOS.file_memory.read_file(path), file_md

    async def write_file(
        self, process_id: str, file_contents: bytes, file_md: Optional[Dict[str, any]] = None
    ) -> FileHandle:
        """
        Writes the given `file_contents` to a new file within the context of the process_id.
        :param file_md:
        :param process_id:
        :param file_contents:
        :return:
        """
        file_id = str(bson.ObjectId())
        await AgentOS.file_memory.mkdir(str(Path(self.root, process_id)), exist_ok=True)
        await AgentOS.file_memory.write_file(str(Path(self.root, process_id, file_id)), file_contents)
        md_to_write = {"process_id": process_id, "file_id": file_id}
        if file_md:
            md_to_write.update(file_md)
        path = str(Path(self.root, process_id, file_id + ".md"))
        await AgentOS.file_memory.write_file(path, json.dumps(md_to_write).encode())
        return FileHandle(
            machineURL=AgentOS.current_machine_url(), process_id=process_id, file_id=file_id, metadata=md_to_write
        )

    async def set_metadata(self, process_id: str, file_id: str, metadata: Dict[str, any]):
        """
        Sets the metadata for the file specified by `file_id` within the context of the process_id.
        :param process_id:
        :param file_id:
        :param metadata:
        :return:
        """
        path = str(Path(self.root, process_id, file_id + ".md"))
        # read the contents of the metadata file
        # update the metadata
        # write the metadata back to the file
        exists = await AgentOS.file_memory.exists(path)
        if not exists:
            file_md = {}
        else:
            contents = await AgentOS.file_memory.read_file(path)
            file_md = json.loads(contents)
        file_md.update(metadata)
        await AgentOS.file_memory.write_file(path, json.dumps(file_md).encode())
        return FileHandle(
            machineURL=AgentOS.current_machine_url(), process_id=process_id, file_id=file_id, metadata=file_md
        )

    async def delete_file(self, process_id: str, file_id: str):
        """
        Deletes the file specified by `file_id` within the context of the process_id.
        :param process_id:
        :param file_id:
        :return:
        """
        path = str(Path(self.root, process_id, file_id))
        exists = await AgentOS.file_memory.exists(path)
        if not exists:
            return None
        await AgentOS.file_memory.delete_file(path)
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
        pfs: ProcessFileSystem = AgentOS.process_file_system
        process_path = str(Path(pfs.root, process_id))
        found = await AgentOS.file_memory.glob(f"{process_path}/**/*")
        await asyncio.gather(*[AgentOS.file_memory.delete_file(file) for file in found])
