import hashlib
import os
from pathlib import Path
from typing import Dict, Any, AsyncIterator

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import (
    DocumentLoader,
    FileInfo,
    DocumentLoaderSpec,
    FileChange,
    ModifiedFile,
    AddedFile,
    RemovedFile,
)
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidolon_ai_sdk.system.reference_model import Specable, T


def hash_file(file_path, chunk_size=8192):
    """
    Hash the contents of a file using SHA-256.

    :param file_path: Path to the file to be hashed.
    :param chunk_size: Size of each chunk to read. Default is 8192 bytes.
    :return: Hexadecimal string of the hash.
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        chunk = file.read(chunk_size)
        while chunk:
            hasher.update(chunk)
            chunk = file.read(chunk_size)
    return hasher.hexdigest()


class FilesystemLoaderSpec(DocumentLoaderSpec):
    root_dir: str
    pattern: str = "**/*"


# noinspection PyShadowingNames
class FilesystemLoader(DocumentLoader, Specable[FilesystemLoaderSpec]):
    def __init__(self, spec: T, **kwargs: object):
        super().__init__(spec, **kwargs)
        root_dir = os.path.expanduser(os.path.expandvars(self.spec.root_dir))
        self.root_path = Path(root_dir).absolute()
        self.root_dir = str(self.root_path)
        if not self.root_path.exists():
            raise ValueError(f"Root directory {self.root_dir} does not exist")

    async def list_files(self) -> AsyncIterator[str]:
        for file in self.root_path.glob(self.spec.pattern):
            yield str(file.relative_to(self.root_dir))

    async def get_changes(self, metadata: Dict[str, Dict[str, Any]]) -> AsyncIterator[FileChange]:
        # iterate over all python files in the root_dir
        for file in self.root_path.glob(self.spec.pattern):
            if file.is_file():
                # get the file path relative to the root_dir
                file_path = str(file.relative_to(self.root_dir))
                # first check the timestamp to see if it changed.  If not, skip the file
                timestamp = os.path.getmtime(file)
                if file_path in metadata:
                    if timestamp != metadata[file_path]["timestamp"]:
                        # create a hash of the file at file path
                        file_hash = hash_file(file)
                        # if the file exists in symbolic memory, check if the hashes are different
                        if "hash" not in file_hash != metadata[file_path]:
                            new_metadata = {"timestamp": timestamp, "file_hash": file_hash}
                            yield ModifiedFile(
                                FileInfo(file_path, new_metadata, DataBlob.from_path(str(self.root_path / file_path)))
                            )
                    del metadata[file_path]
                else:
                    timestamp = os.path.getmtime(file)
                    file_hash = hash_file(file)
                    new_metadata = {"timestamp": timestamp, "file_hash": file_hash}
                    yield AddedFile(
                        FileInfo(file_path, new_metadata, DataBlob.from_path(str(self.root_path / file_path)))
                    )

        for not_found in metadata.keys():
            yield RemovedFile(not_found)
