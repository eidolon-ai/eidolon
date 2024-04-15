from pathlib import Path

from pydantic import Field, BaseModel

from eidolon_ai_sdk.memory.file_memory import FileMemoryBase
from eidolon_ai_sdk.system.reference_model import Specable


class InMemoryFileMemoryConfig(BaseModel):
    pass


class InMemoryFileMemory(FileMemoryBase, Specable[InMemoryFileMemoryConfig]):
    def __init__(self, spec: InMemoryFileMemoryConfig):
        super().__init__(spec)
        self.root_dir = Path("/").resolve()
        self.files = {}
        self.spec = spec

    """
    A FileMemory implementation that stores files on the local filesystem.
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
        return self.files[safe_file_path]

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
        self.files[safe_file_path] = file_contents

    async def delete_file(self, file_path: str) -> None:
        # Resolve the safe path
        safe_file_path = self.resolve(file_path)

        # Delete the file
        del self.files[safe_file_path]

    async def mkdir(self, directory: str, exist_ok: bool = False):
        safe_file_path = self.resolve(directory)
        self.files[safe_file_path] = {}
        print(f"Created directory {safe_file_path}")

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

        print(f"Checking if {safe_file_path} exists")
        print(f"Files: {self.files}")
        # Check if the file exists
        return self.files.get(safe_file_path) is not None

    async def glob(self, pattern: str):
        pass

    async def start(self):
        """
        Starts the memory implementation. Noop for this implementation.
        """
        pass

    async def stop(self):
        """
        Stops the memory implementation. Noop for this implementation.
        """
        pass
