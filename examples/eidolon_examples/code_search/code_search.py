import os
from pathlib import Path
from typing import List, Annotated

from pydantic import Field, BaseModel

from eidos.agent_os import AgentOS
from eidos.cpu.logic_unit import LogicUnit, llm_function
from eidos.memory.embeddings import OpenAIEmbeddingSpec, OpenAIEmbedding
from eidos.system.reference_model import Specable
from eidolon_examples.code_search.code_sync import CodeSync


class CodePackage(BaseModel):
    """
    A package is a collection of python files.
    """

    package_directory: str = Field(description="The directory that contains the package")
    files: List[str] = Field(description="The files that make up the package")


class SourceCode(BaseModel):
    """
    Source code is a collection of lines of code for a given file
    """

    file_name: str = Field(description="The name of the file")
    source_code: str = Field(description="The source code for the file")


class SearchResult(BaseModel):
    """
    A search result is a snippet of source code that matched the query
    """

    file_name: str = Field(description="The name of the file")
    source_code_snippet: str = Field(description="A snippet of the source code that matched the query")


class CodeSearchConfig(BaseModel):
    root_dir: str = Field(description="The root directory to search for code in")


class CodeSearch(LogicUnit, Specable[CodeSearchConfig]):
    syncer: CodeSync = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_dir = os.path.abspath(os.path.expandvars(self.spec.root_dir))
        self.embedder = OpenAIEmbedding(OpenAIEmbeddingSpec())

    async def _init(self):
        if not self.syncer:
            self.syncer = CodeSync(os.path.abspath(self.root_dir))
            await self.syncer.sync_all()

    @llm_function()
    async def list_packages(self) -> List[CodePackage]:
        """
        Recursively search for Python modules in the code.

        :return: A list of CodeModules containing Python modules.
        """
        await self._init()
        package_directories = {}

        for root, dirs, files in os.walk(self.root_dir):
            if "__init__.py" in files:
                package_name = str(Path(root).relative_to(self.root_dir))
                package_files = [f for f in files if f.endswith(".py")]
                package_directories[root] = CodePackage(
                    package_directory=package_name,
                    files=package_files,
                )

        return list(package_directories.values())

    @llm_function()
    async def get_code(
        self, file_name: Annotated[str, Field(description="The name of the file to get code from")]
    ) -> SourceCode:
        """
        Get the source code for a given file
        :return: The source code for the file
        """
        await self._init()
        # first expand the file name wrt the root dir
        file_name = os.path.expandvars(file_name)
        # now process relative paths for file name wrt the root dir
        file_name = os.path.relpath(file_name, self.root_dir)
        # now convert to absolute path
        file_name = os.path.abspath(file_name)

        # now check that the file is in the root dir
        if not file_name.startswith(self.root_dir):
            raise ValueError(f"File {file_name} is not in root dir {self.root_dir}")

        with open(os.path.join(self.root_dir, file_name), "r") as f:
            return SourceCode(
                file_name=file_name,
                source_code=f.read(),
            )

    @llm_function()
    async def search_code(
        self,
        query: Annotated[
            str,
            Field(description="The query to search for. The query will be embedded and searched using a vector store"),
        ],
    ) -> List[SearchResult]:
        """
        Search for code that matches the query
        :return: The code snippets that match the query
        """
        await self._init()
        results = await AgentOS.similarity_memory.query("code_sync", self.embedder, query, 10, {})
        return [
            SearchResult(
                file_name=result.metadata["file_path"],
                source_code_snippet=result.page_content,
            )
            for result in results
        ]
