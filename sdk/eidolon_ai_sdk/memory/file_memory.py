from abc import ABC, abstractmethod


# todo, memory contracts all need to be async
class FileMemory(ABC):
    """
    Abstract base class representing the file memory interface for an agent.

    This class defines the essential file operations that an agent's memory component
    must support. It includes starting and stopping the file memory processes,
    reading from a file, and writing to a file within the agent's operational context.

    All methods in this class are abstract and must be implemented by a subclass
    that provides the specific logic for handling file operations related to the
    agent's memory.
    """

    @abstractmethod
    def start(self):
        """
        Starts the memory implementation.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Stops the memory implementation.
        """
        pass

    @abstractmethod
    def read_file(self, file_path: str) -> bytes:
        """
            Reads the contents of a file specified by `file_path` within the context
            of an agent call. The context of the call provides additional information
            that may influence how the file is read.
        :param file_path: The path to the file to be read.
        :return: bytes: The contents of the file as a bytes object.
        """
        pass

    @abstractmethod
    def write_file(self, file_path: str, file_contents: bytes) -> None:
        """
            Writes the given `file_contents` to the file specified by `file_path`
            within the context of an agent call. This method ensures that the file is
            written in the appropriate location and manner as dictated by the call context.

        :param file_path: The path to the file where the contents should be written.
        :param file_contents: The contents to write to the file.
        """
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        """
            Deletes the file specified by `file_path` within the context of an agent call.
            This method ensures that the file is deleted in the appropriate location and
            manner as dictated by the call context.

        :param file_path: The path to the file to be deleted.
        """
        pass

    @abstractmethod
    def mkdir(self, directory: str, exist_ok: bool = False):
        pass

    @abstractmethod
    def exists(self, file_name: str):
        pass
