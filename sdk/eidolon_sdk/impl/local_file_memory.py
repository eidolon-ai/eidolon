from pathlib import Path

from pydantic import Field, field_validator

from eidolon_sdk.agent_memory import FileMemory
from eidolon_sdk.util.str_utils import replace_env_var_in_string


class LocalFileMemory(FileMemory):
    """
    A FileMemory implementation that stores files on the local filesystem.
    """
    root_dir: Path = Field(..., description="The root directory to store files in.")

    @field_validator('root_dir', mode='before')
    def validate_root_dir(cls, inValue: str):
        """
        Validates that the provided root directory is an absolute path and exists.

        Args:
            inValue (str): The root directory path to validate.

        Returns:
            Path: The validated root directory as a Path object.

        Raises:
            ValueError: If the root directory is not an absolute path or does not exist.
        """
        value = replace_env_var_in_string(inValue)
        # Convert the string to a Path object
        path = Path(value).resolve()

        # Check if the path is absolute
        if not path.is_absolute():
            raise ValueError(f"The root_dir must be an absolute path. Received: {inValue}->{value}")

        if not path.exists():
            path.mkdir(parents=True)

        # You could also check if path exists and is a directory if necessary
        if not path.exists() or not path.is_dir():
            raise ValueError(f"The root_dir must exist and be a directory. Received: {inValue}->{value}")

        return path

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
        with open(safe_file_path, 'rb') as file:
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
        with open(safe_file_path, 'wb') as file:
            file.write(file_contents)

    def start(self):
        """
        Starts the memory implementation. Noop for this implementation.
        """
        pass

    def stop(self):
        """
        Stops the memory implementation. Noop for this implementation.
        """
        pass

