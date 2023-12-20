import os
from pathlib import Path
from typing import List, Annotated

from eidos_sdk.agent_os import AgentOS
from eidos_sdk.cpu.logic_unit import LogicUnit, llm_function
from eidos_sdk.memory.embeddings import OpenAIEmbeddingSpec, OpenAIEmbedding
from eidos_sdk.system.reference_model import Specable
from pydantic import Field, BaseModel

from eidolon_examples.code_search.code_sync import CodeSync
from eidolon_examples.code_search.vector_search_directory_sync import VectorSearchDirSync
from eidos.cpu.llm_message import LLMMessage
from eidos.system.eidos_handler import EidosHandler


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
    name: str = Field(default="Code Search", description="The name of the tool")
    description_preamble: str = Field(default="", description="The description preamble for all tools")


class CodeSearch(LogicUnit, Specable[CodeSearchConfig]):
    syncer: VectorSearchDirSync = None

    def __init__(self, spec: CodeSearchConfig, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec
        self.root_dir = os.path.abspath(os.path.expandvars(self.spec.root_dir))
        self.embedder = OpenAIEmbedding(OpenAIEmbeddingSpec())

    async def build_tools(self, conversation: List[LLMMessage]) -> List[EidosHandler]:
        tools = await super().build_tools(conversation)
        def add_description(spec, handler):
            ret = handler.description(spec, handler)
            if len(self.spec.description_preamble) > 0:
                ret = self.spec.description_preamble + "\n" + ret

            def desc_wrapper(_spec, _handler):
                return ret
            return desc_wrapper

        ret_tools = []
        for tool in tools:
            ret_tools.append(EidosHandler(
                name=self.spec.name + "_" + tool.name,
                description=add_description(self.spec, tool),
                fn=tool.fn,
                input_model_fn=tool.input_model_fn,
                output_model_fn=tool.output_model_fn,
                extra=tool.extra
            ))

        return ret_tools

    async def _init(self):
        if not self.syncer:
            self.syncer = CodeSync(os.path.abspath(self.root_dir), self.spec.name)
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
                package_files = [f for f in files]
                package_directories[root] = CodePackage(
                    package_directory=package_name,
                    files=package_files,
                )

        return list(package_directories.values())

    @llm_function()
    async def get_code(
        self, file_path: Annotated[str, Field(description="The path to the file to get the source code for")]
    ) -> SourceCode:
        """
        Get the source code for a given file. Make sure the complete file path is passed in and not just the file name.
        :return: The source code for the file
        """
        await self._init()
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
            return SourceCode(
                file_name=file_path,
                source_code=f.read(),
            )

    @llm_function()
    async def search_code(
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
        results = await AgentOS.similarity_memory.query("code_sync", self.embedder, query, max_results, {})
        return [
            SearchResult(
                file_name=result.metadata["file_path"],
                source_code_snippet=result.page_content,
            )
            for result in results
        ]
