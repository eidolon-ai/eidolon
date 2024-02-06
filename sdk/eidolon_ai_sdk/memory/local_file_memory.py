from pathlib import Path

from pydantic import Field, field_validator, BaseModel

from eidolon_ai_sdk.memory.file_memory import FileMemory
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.str_utils import replace_env_var_in_string


class LocalFileMemoryConfig(BaseModel):
    root_dir: str = Field("/tmp/eidolon/file_memory", description="The root directory to store files in.")

    @field_validator("root_dir", mode="before")
    def validate_root_dir(cls, inValue: str):
        """
        Validates that the provided root directory is an absolute path and exists.
        """
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


class LocalFileMemory(FileMemory, Specable[LocalFileMemoryConfig]):
    def __init__(self, spec: LocalFileMemoryConfig):
        super().__init__(spec)
        self.root_dir = Path(replace_env_var_in_string(spec.root_dir)).resolve()

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

    def read_file(self, file_path: str) -> bytes:
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
        with open(safe_file_path, "rb") as file:
            return file.read()

    def write_file(self, file_path: str, file_contents: bytes) -> None:
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
        with open(safe_file_path, "wb") as file:
            file.write(file_contents)

    def delete_file(self, file_path: str) -> None:
        # Resolve the safe path
        safe_file_path = self.resolve(file_path)

        # Delete the file
        safe_file_path.unlink()

    def mkdir(self, directory: str, exist_ok: bool = False):
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

    def exists(self, file_name: str):
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
        return safe_file_path.exists()

    def start(self):
        """
        Starts the memory implementation. Noop for this implementation.
        """
        if not self.root_dir.exists():
            self.root_dir.mkdir(parents=True)

    def stop(self):
        """
        Stops the memory implementation. Noop for this implementation.
        """
        pass
