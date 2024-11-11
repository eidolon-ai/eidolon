import asyncio
import glob
from pathlib import Path

import aiofiles
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent_os_interfaces import FileMetadata
from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.str_utils import replace_env_var_in_string
from pydantic import Field, field_validator, BaseModel


class LocalFileMemoryConfig(BaseModel):
    """
    Retrieve documents from a local file system. Note that this is the file system where the Eidolon application is
    running. This means building the files onto the runtime image, or mounting a volume to the container.

    [Docker volume](https://docs.docker.com/engine/storage/volumes/#use-a-volume-with-docker-compose)
    [Build the files into the runtime image](https://docs.docker.com/reference/dockerfile/#copy)
    [Kubernetes volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
    """

    root_dir: str = Field("/tmp/eidolon/file_memory", description="The root directory to store files in.")

    @field_validator("root_dir", mode="before")
    def validate_root_dir(cls, inValue: str):
        """
        Validates that the provided root directory is an absolute path and exists.
        """
        inValue = str(inValue)
        value = replace_env_var_in_string(inValue)
        # Convert the string to a Path object
        path = Path(value).resolve()

        # Check if the path is absolute
        if not path.is_absolute():
            raise ValueError(f"The root_dir must be an absolute path. Received: {inValue}->{value}")

        # You could also check if path exists and is a directory if necessary
        if path.is_file():
            raise ValueError(f"The root_dir must be a directory. Received: {inValue}->{value}")

        return inValue


class LocalFileMemory(FileMemoryBase, Specable[AsyncLocalFileMemoryConfig]):
    def __init__(self, spec: AsyncLocalFileMemoryConfig):
        super().__init__(spec)
        self.root_dir = Path(replace_env_var_in_string(spec.root_dir)).resolve()

    """
    A FileMemory implementation that stores files on the local filesystem using asyncio.
    """
    root_dir: Path = Field(..., description="The root directory to store files in.")

    def resolve(self, *paths):
        """
        Resolves file paths relative to the root directory and ensures that they do not escape the root directory.

        Args:
            *paths (str): A variable number of path components to be joined and resolved.

        Returns:
            Path: The resolved path as a Path object.

        Raises:
            ValueError: If the resulting path is outside the root directory.
        """
        # Resolve the combined path
        resolved_path = self.root_dir.joinpath(*paths).resolve()

        # Check that the resolved path is a subpath of root_dir
        if not resolved_path.is_relative_to(self.root_dir):
            raise ValueError("Attempted to access a path outside the root directory")

        return resolved_path

    async def read_file(self, file_path: str) -> bytes:
        """
        Reads and returns the contents of the file specified by the file_path within the root directory.

        Args:
            file_path (str): The path to the file to be read, relative to the root directory.

        Returns:
            bytes: The contents of the file as a bytes object.
        """
        # Resolve the safe path
        safe_file_path = self.resolve(file_path)

        # Read the file and return its contents
        async with aiofiles.open(safe_file_path, mode='rb') as file:
            return await file.read()

    async def write_file(self, file_path: str, file_contents: bytes) -> None:
        """
        Writes the given file_contents to the file specified by the file_path within the root directory.

        Args:
            file_path (str): The path to the file where contents are to be written, relative to the root directory.
            file_contents (bytes): The contents to write to the file.

        Returns:
            None
        """
        # Resolve the safe path
        safe_file_path = self.resolve(file_path)

        # Write the contents to the file
        async with aiofiles.open(safe_file_path, mode='wb') as file:
            await file.write(file_contents)

    async def delete_file(self, file_path: str) -> None:
        # Resolve the safe path
        safe_file_path = self.resolve(file_path)

        # Delete the file
        try:
            await asyncio.to_thread(safe_file_path.unlink)
        except FileNotFoundError:
            logger.debug("Attempted to delete non-existent file")
            pass

    async def mkdir(self, directory: str, exist_ok: bool = False):
        """
        Creates a directory at the specified path relative to the root directory.

        Args:
            directory (str): The path to the directory to be created, relative to the root directory.
            exist_ok (bool): If True, do not raise an exception if the directory already exists.

        Returns:
            None
        """
        # Resolve the safe path
        safe_directory = self.resolve(directory)

        # Create the directory
        safe_directory.mkdir(parents=True, exist_ok=exist_ok)

    async def exists(self, file_name: str):
        """
        Checks if a file exists at the specified path relative to the root directory.

        Args:
            file_name (str): The path to the file to check, relative to the root directory.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        # Resolve the safe path
        safe_file_path = self.resolve(file_name)

        # Check if the file exists
        return await asyncio.to_thread(safe_file_path.exists)

    async def glob(self, pattern):
        safe_file_path = self.resolve(pattern)
        glob_results = await asyncio.to_thread(glob.glob, str(safe_file_path), root_dir=self.root_dir)
        for s in glob_results:
            yield FileMetadata(file_path=s.removeprefix(str(self.root_dir)).removeprefix("/"))

    async def start(self):
        """
        Starts the memory implementation. Creates the root directory if it doesn't exist.
        """
        if not self.root_dir.exists():
            self.root_dir.mkdir(parents=True)

    async def stop(self):
        """
        Stops the memory implementation. Noop for this implementation.
        """
        pass
