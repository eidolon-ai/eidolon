try:
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass
import chromadb
from chromadb import Include, QueryResult
from chromadb.api.models.Collection import Collection
from pathlib import Path
from pydantic import Field, field_validator
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs

from eidolon_ai_sdk.memory.document import EmbeddedDocument
from eidolon_ai_sdk.memory.file_system_vector_store import FileSystemVectorStore, FileSystemVectorStoreSpec
from eidolon_ai_sdk.memory.vector_store import QueryItem
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.str_utils import replace_env_var_in_string


class ChromaVectorStoreConfig(FileSystemVectorStoreSpec):
    url: str = Field(
        "file://${EIDOLON_DATA_DIR}/doc_producer",
        description="The url of the chroma database. "
        + "Use http(s)://$HOST:$PORT?header1=value1&header2=value2 to pass headers to the database."
        + "Use file://$PATH to use a local file database.",
        validate_default=True,
    )

    # noinspection PyMethodParameters,HttpUrlsUsage
    @field_validator("url")
    def validate_url(cls, url):
        if url.startswith("file://"):
            if len(url) < 8:
                raise ValueError("file:// must be followed by a path")

            path = url[7:]
            if len(path) == 0:
                raise ValueError("file:// must be followed by a path")

            # validate path is a file on disk
            value = replace_env_var_in_string(path, EIDOLON_DATA_DIR="/tmp/eidolon_data_dir")
            # Convert the string to a Path object
            path = Path(value).resolve()

            # Check if the path is absolute
            if not path.is_absolute():
                raise ValueError(f"The root_dir must be an absolute path. Received: {path}->{value}")

            return f"file://{path.absolute()}"
        elif url.startswith("http://") or url.startswith("https://"):
            return url
        else:
            raise ValueError("url must start with file://, http://, or https://")


class ChromaVectorStore(FileSystemVectorStore, Specable[ChromaVectorStoreConfig]):
    spec: ChromaVectorStoreConfig
    client: chromadb.Client

    def __init__(self, spec: ChromaVectorStoreConfig):
        super().__init__(spec)
        self.spec = spec
        self.client = None

    async def start(self):
        pass

    def connect(self):
        url = urlparse(self.spec.url)
        if url.scheme == "file":
            path = url.path
            self.client = chromadb.PersistentClient(path)
        else:
            host = url.hostname
            port = url.port or "8000"
            ssl = url.scheme == "https"
            if url.query and len(url.query) > 0:
                headers = parse_qs(url.query)
            else:
                headers = None
            self.client = chromadb.HttpClient(host=host, port=port, ssl=ssl, headers=headers)

    async def stop(self):
        pass

    def _get_collection(self, name: str) -> Collection:
        if not self.client:
            self.connect()

        try:
            return self.client.get_or_create_collection(name=name)
        except BaseException as e:
            raise RuntimeError(f"Failed to get collection {name}") from e

    async def add_embedding(self, collection: str, docs: List[EmbeddedDocument], **add_kwargs: Any):
        collection = self._get_collection(name=collection)
        doc_ids = [doc.id for doc in docs]
        embeddings = [doc.embedding for doc in docs]
        metadata = [doc.metadata for doc in docs]
        collection.upsert(embeddings=embeddings, ids=doc_ids, metadatas=metadata, **add_kwargs)

    async def delete_embedding(self, collection: str, doc_ids: List[str], **delete_kwargs: Any):
        collection = self._get_collection(name=collection)
        collection.delete(ids=doc_ids, **delete_kwargs)

    async def get_metadata(self, collection: str, doc_ids: List[str]):
        collection = self._get_collection(name=collection)
        return collection.get(ids=doc_ids, include=["metadatas"])["metadatas"]

    async def query_embedding(
        self,
        collection: str,
        query: List[float],
        num_results: int,
        metadata_where: Optional[Dict[str, str]] = None,
        include_embeddings=False,
    ) -> List[QueryItem]:
        collection = self._get_collection(name=collection)
        thingsToInclude: Include = ["metadatas", "distances"]
        if include_embeddings:
            thingsToInclude.append("embeddings")

        results: QueryResult = collection.query(
            query_embeddings=[query],
            n_results=num_results,
            where=metadata_where,
            include=thingsToInclude,
        )

        ret = []
        for i, doc_id in enumerate(results["ids"][0]):
            embedding = results["embeddings"][0][i] if include_embeddings else None
            ret.append(
                QueryItem(
                    id=doc_id,
                    score=results["distances"][0][i],
                    embedding=embedding,
                    metadata=results["metadatas"][0][i],
                )
            )

        return ret
