from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict, Any, Union, List, AsyncIterable, Set, Literal, Sequence, AsyncGenerator
from starlette.requests import Request

from eidolon_ai_client.events import FileHandle
from eidolon_ai_sdk.memory.document import Document, EmbeddedDocument
from eidolon_ai_sdk.memory.vector_store import QueryItem
from eidolon_ai_sdk.security.user import User


class ProcessFileSystem(ABC):
    @abstractmethod
    async def read_file(self, process_id: str, file_id: str) -> Optional[Tuple[bytes, Optional[Dict[str, any]]]]:
        """
        Reads the contents of a file for the given process_id and file_id
        :param process_id:
        :param file_id:
        :return:
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def write_file(
        self, process_id: str, file_contents: bytes, file_md: Optional[Dict[str, any]] = None
    ) -> FileHandle:
        """
        Writes the given `file_contents` to a new file within the context of the process_id.
        :param file_md:
        :param process_id:
        :param file_contents:
        :return:
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def set_metadata(self, process_id: str, file_id: str, metadata: Dict[str, any]):
        """
        Sets the metadata for the file specified by `file_id` within the context of the process_id.
        :param process_id:
        :param file_id:
        :param metadata:
        :return:
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def delete_file(self, process_id: str, file_id: str):
        """
        Deletes the file specified by `file_id` within the context of the process_id.
        :param process_id:
        :param file_id:
        :return:
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def list_files(self, process_id: str, include_only_index: bool):
        """
        Lists the files within the context of the process_id.
        :param process_id:
        :param include_only_index:
        :return:
        """
        raise NotImplementedError("not implemented")


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
    async def read_file(self, file_path: str) -> bytes:
        """
            Reads the contents of a file specified by `file_path` within the context
            of an agent call. The context of the call provides additional information
            that may influence how the file is read.
        :param file_path: The path to the file to be read.
        :return: bytes: The contents of the file as a bytes object.
        """
        pass

    @abstractmethod
    async def write_file(self, file_path: str, file_contents: bytes) -> None:
        """
            Writes the given `file_contents` to the file specified by `file_path`
            within the context of an agent call. This method ensures that the file is
            written in the appropriate location and manner as dictated by the call context.

        :param file_path: The path to the file where the contents should be written.
        :param file_contents: The contents to write to the file.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> None:
        """
            Deletes the file specified by `file_path` within the context of an agent call.
            This method ensures that the file is deleted in the appropriate location and
            manner as dictated by the call context.

        :param file_path: The path to the file to be deleted.
        """
        pass

    @abstractmethod
    async def mkdir(self, directory: str, exist_ok: bool = False):
        pass

    @abstractmethod
    async def exists(self, file_name: str):
        pass

    @abstractmethod
    async def glob(self, pattern: str):
        raise NotImplementedError("not implemented")


class SymbolicMemory(ABC):
    """
    Abstract base class for a symbolic memory component within an agent.

    This class defines the contract for symbolic memory operations such as starting
    and stopping the memory service, and CRUD (Create, Read, Update, Delete) operations
    on symbolic data. Implementations of this class are expected to manage collections
    of symbols, providing a high-level interface to store and retrieve symbolic information.
    """

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


class SimilarityMemory(ABC):
    @abstractmethod
    async def embed_text(self, text: str, **kwargs: Any) -> List[float]:
        """Create an embedding for a single piece of text.

        Args:
            text: The text to be encoded.

        Returns:
            An embedding for the text.
        """
        raise NotImplementedError("not implemented")

    def embed(self, documents: Sequence[Document], **kwargs: Any) -> AsyncGenerator[EmbeddedDocument, None]:
        """
        Create embeddings for a list of documents.
        :param documents:
        :param kwargs:
        :return:
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def add(self, collection: str, docs: Sequence[Document]):
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def delete(self, collection: str, doc_ids: List[str]):
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def query(
        self,
        collection: str,
        query: str,
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
    ) -> List[Document]:
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def raw_query(
        self,
        collection: str,
        query: List[float],
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
        include_embeddings: bool = False,
    ) -> List[QueryItem]:
        raise NotImplementedError("not implemented")

    @abstractmethod
    def get_docs(self, collection: str, doc_ids: List[str]) -> AsyncIterable[Document]:
        raise NotImplementedError("not implemented")


Permission = Literal["create", "read", "update", "delete"]  # probably expands to include concept of know


class SecurityManager(ABC):
    @abstractmethod
    async def check_permissions(
        self, permissions: Permission | Set[Permission], agent: str, process_id: Optional[str] = None
    ):
        """
        Checks if the authenticated user has the specified permission(s) to the provided agent process.
        :param permissions:
        :param agent:
        :param process_id:
        :return:
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def check_auth(self, request: Request) -> User:
        """
        Check the request for expected authentication and stores information in context as needed for authorization.

        :return User: the authenticated user
        :raises HTTPException: if the request is not authenticated
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def check_process_perms(self, permissions: Set[Permission], agent: str, process_id: str):
        """
        Checks if the authenticated user has the specified permission(s) to the provided agent process.
        :raises PermissionException: If the agent does not have the required permissions.
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    async def record_process(self, agent: str, resource_id: str):
        """
        Called when a process is created. Should propagate any state needed for future resource checks.
        """
        raise NotImplementedError("not implemented")
