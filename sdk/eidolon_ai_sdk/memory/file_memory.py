from abc import abstractmethod

from eidolon_ai_sdk.agent_os_interfaces import FileMemory


class FileMemoryBase(FileMemory):
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
    async def start(self):
        """
        Starts the memory implementation.
        """
        pass

    @abstractmethod
    async def stop(self):
        """
        Stops the memory implementation.
        """
        pass
