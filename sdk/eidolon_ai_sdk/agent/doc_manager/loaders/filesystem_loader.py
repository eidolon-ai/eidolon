import hashlib
import os
from pathlib import Path
from typing import Dict, Any, Iterable

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import (
    DocumentLoader,
    FileChangeset,
    FileInfo,
    DocumentLoaderSpec,
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

    async def list_files(self) -> Iterable[str]:
        for file in self.root_path.glob(self.spec.pattern):
            yield str(file.relative_to(self.root_dir))

    async def get_changes(self, metadata: Dict[str, Dict[str, Any]]) -> FileChangeset:
        added = {}
        modified = {}
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
                            modified[file_path] = {"timestamp": timestamp, "file_hash": file_hash}
                    # delete from hashes
                    del metadata[file_path]
                else:
                    timestamp = os.path.getmtime(file)
                    file_hash = hash_file(file)
                    added[file_path] = {"timestamp": timestamp, "file_hash": file_hash}

        self.logger.info(f"Found {len(added)} added files")
        self.logger.info(f"Found {len(modified)} modified files")
        self.logger.info(f"Found {len(metadata)} deleted files")

        async def added_files():
            for file_path in added:
                yield FileInfo(file_path, added[file_path], DataBlob.from_path(str(self.root_path / file_path)))

        async def modified_files():
            for file_path in modified:
                yield FileInfo(file_path, modified[file_path], DataBlob.from_path(str(self.root_path / file_path)))

        async def deleted_files():
            for file_path in metadata:
                yield file_path

        return FileChangeset(added_files=added_files(), modified_files=modified_files(), removed_files=deleted_files())
