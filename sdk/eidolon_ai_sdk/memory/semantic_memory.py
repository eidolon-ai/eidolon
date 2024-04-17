from eidolon_ai_sdk.agent_os_interfaces import SymbolicMemory


class SymbolicMemoryBase(SymbolicMemory):
    """
    Abstract base class for a symbolic memory component within an agent.

    This class defines the contract for symbolic memory operations such as starting
    and stopping the memory service, and CRUD (Create, Read, Update, Delete) operations
    on symbolic data. Implementations of this class are expected to manage collections
    of symbols, providing a high-level interface to store and retrieve symbolic information.
    """

    async def start(self):
        """
        Prepares the symbolic memory for operation, which may include tasks like
        allocating resources or initializing connections to databases.
        """
        pass

    async def stop(self):
        """
        Properly shuts down the symbolic memory, ensuring that any resources are released
        or any established connections are terminated.
        """
        pass
