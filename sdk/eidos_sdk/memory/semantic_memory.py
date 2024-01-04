from typing import Any, Union, List, Dict, AsyncIterable, Optional

from abc import ABC, abstractmethod


class SymbolicMemory(ABC):
    """
    Abstract base class for a symbolic memory component within an agent.

    This class defines the contract for symbolic memory operations such as starting
    and stopping the memory service, and CRUD (Create, Read, Update, Delete) operations
    on symbolic data. Implementations of this class are expected to manage collections
    of symbols, providing a high-level interface to store and retrieve symbolic information.
    """

    @abstractmethod
    def start(self):
        """
        Prepares the symbolic memory for operation, which may include tasks like
        allocating resources or initializing connections to databases.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Properly shuts down the symbolic memory, ensuring that any resources are released
        or any established connections are terminated.
        """
        pass

    @abstractmethod
    async def count(self, symbol_collection: str, query: dict[str, Any]) -> int:
        """
        Searches for symbols within a specified collection that match the given query and returns the number matching.

        Args:
            symbol_collection (str): The name of the collection to search within.
            query (dict[str, Any]): The search criteria used to filter symbols.

        Returns:
            int: The number of symbols that match the query.
        """
        pass

    @abstractmethod
    def find(
        self,
        symbol_collection: str,
        query: dict[str, Any],
        projection: Union[List[str], Dict[str, int]] = None,
        sort: dict = None,
        skip: int = None,
    ) -> AsyncIterable[dict[str, Any]]:
        """
        Searches for symbols within a specified collection that match the given query.

        Args:
            symbol_collection (str): The name of the collection to search within.
            query (dict[str, Any]): The search criteria used to filter symbols.
            projection (Union[List[str], Dict[str, int]]): The fields to include or exclude from the results. If a list,
                the fields will be included. If a dictionary, the fields will be included or excluded based on the
                value of the dictionary. A value of 1 will include the field, and a value of 0 will exclude it.
            sort (dict): The fields to sort the results by. The key is the field to sort by, and the value is the direction
                to sort by. A value of 1 will sort in ascending order, and a value of -1 will sort in descending order.
            skip (int): The number of results to skip.

        Returns:
            Iterable[dict[str, Any]]: A list of symbols that match the query, each represented as a dictionary.
        """
        pass

    @abstractmethod
    async def find_one(
        self, symbol_collection: str, query: dict[str, Any], sort: dict[str, int] = None
    ) -> Optional[dict[str, Any]]:
        """
        Searches for a single symbol within a specified collection that matches the given query.

        Args:
            symbol_collection (str): The name of the collection to search within.
            query (dict[str, Any]): The search criteria used to filter symbols.
            sort (dict[str, int]): The fields to sort the results by. The key is the field to sort by, and the value is the direction

        Returns:
            Optional[dict[str, Any]]: A single symbol that matches the query, represented as a dictionary,
            or None if no match is found.
        """
        pass

    @abstractmethod
    async def insert(self, symbol_collection: str, documents: list[dict[str, Any]]) -> None:
        """
        Inserts multiple symbols into the specified collection.

        Args:
            symbol_collection (str): The name of the collection where symbols will be inserted.
            documents (list[dict[str, Any]]): A list of symbols to insert, each represented as a dictionary.

        Returns:
            None
        """
        pass

    @abstractmethod
    async def insert_one(self, symbol_collection: str, document: dict[str, Any]) -> None:
        """
        Inserts a single symbol into the specified collection.

        Args:
            symbol_collection (str): The name of the collection where the symbol will be inserted.
            document (dict[str, Any]): The symbol to insert, represented as a dictionary.

        Returns:
            None
        """
        pass

    @abstractmethod
    async def upsert_one(self, symbol_collection: str, document: dict[str, Any], query: dict[str, Any]) -> None:
        """
        Updates a single symbol in the specified collection based on the query, or inserts it if it does not exist.

        Args:
            symbol_collection (str): The name of the collection where the symbol will be upserted.
            document (dict[str, Any]): The symbol to upsert, represented as a dictionary.
            query (dict[str, Any]): The search criteria used to find the symbol to update.

        Returns:
            None
        """
        pass

    @abstractmethod
    async def update_many(self, symbol_collection: str, query: dict[str, Any], document: dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def delete(self, symbol_collection, query):
        pass
