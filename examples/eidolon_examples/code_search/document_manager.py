import os
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Annotated, List

from eidolon_examples.code_search.code_sync import MarkdownSync
from eidolon_examples.code_search.vector_search_directory_sync import VectorSearchDirSync
from eidos_sdk.cpu.logic_unit import llm_function, LogicUnit
from eidos_sdk.memory.embeddings import OpenAIEmbeddingSpec, OpenAIEmbedding
from eidos_sdk.system.reference_model import Specable


class SearchResult(BaseModel):
    """
    A search result is a snippet of the document that matched the query
    """

    file_name: str = Field(description="The name of the file")
    document_snippet: str = Field(description="A snippet of the document that matched the query")


class DocumentDirectory(BaseModel):
    """
    A package is a collection of python files.
    """

    directory: str = Field(description="The name of the directory")
    files: List[str] = Field(description="The files that make up the package")


class DocumentManagerSpec(BaseModel):
    root_dir: str = Field(description="The root directory of the documents")


class DocumentManager(LogicUnit, Specable[DocumentManagerSpec]):
    syncer: VectorSearchDirSync = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.root_dir = os.path.abspath(os.path.expandvars(self.spec.root_dir))
        self.embedder = OpenAIEmbedding(OpenAIEmbeddingSpec())

    async def _init(self):
        if not self.syncer:
            self.syncer = MarkdownSync(os.path.abspath(self.root_dir), "documents")
            await self.syncer.sync_all()

    @llm_function()
    async def list_documents(self):
        """
        Recursively lists all directories and the files they contain.
        :return:
        """
        await self._init()
        package_directories = {}

        for root, dirs, files in os.walk(self.root_dir):
            dir_name = str(Path(root).relative_to(self.root_dir))
            package_files = [f for f in files]
            package_directories[root] = DocumentDirectory(
                directory=dir_name,
                files=package_files,
            )

        return list(package_directories.values())

    @llm_function()
    async def get_document(
            self, file_path: Annotated[str, Field(description="The path to the file to be retrieved")]
    ) -> str:
        """
        Gets a document from the document manager. The document is specified by the path.
        :param file_path: The path to the document
        :return: The document at the path
        """
        # first expand the file name wrt the root dir
        file_path = os.path.expandvars(file_path)
        # now process relative paths for file name wrt the root dir
        file_path = os.path.join(self.root_dir, file_path)
        # now convert to absolute path
        file_path = os.path.abspath(file_path)

        # now check that the file is in the root dir
        if not file_path.startswith(self.root_dir):
            raise ValueError(f"File {file_path} is not in root dir {self.root_dir}")

        with open(os.path.join(self.root_dir, file_path), "r") as f:
            return f.read()

    @llm_function()
    async def write_document(
            self,
            file_path: Annotated[str, Field(description="The path to the file to be saved")],
            contents: Annotated[str, Field(description="The contents of the file to be saved")],
    ) -> None:
        """
        Writes a document to the document manager. The document is specified by the path.
        :param file_path: The path to the document
        :param contents: The contents of the document
        """
        # first expand the file name wrt the root dir
        file_path = os.path.expandvars(file_path)
        # now process relative paths for file name wrt the root dir
        file_path = os.path.join(self.root_dir, file_path)
        # now convert to absolute path
        file_path = os.path.abspath(file_path)

        # now check that the file is in the root dir
        if not file_path.startswith(self.root_dir):
            raise ValueError(f"File {file_path} is not in root dir {self.root_dir}")

        with open(os.path.join(self.root_dir, file_path), "w") as f:
            f.write(contents)

    @llm_function()
    async def search_documents(
            self,
            query: Annotated[
                str,
                Field(description="The query to search for. The query will be embedded and searched using a vector store"),
            ],
            max_results: Annotated[
                int,
                Field(
                    description="The maximum number of results to return. The results will be sorted by similarity to the query"
                ),
            ] = 10,
    ) -> List[SearchResult]:
        """
        Search for code that matches the query
        :return: The code snippets that match the query
        """
        await self._init()
        results = await self.syncer.query(query, max_results)
        return [
            SearchResult(
                file_name=result.metadata["file_path"],
                source_code_snippet=result.page_content,
            )
            for result in results
        ]
