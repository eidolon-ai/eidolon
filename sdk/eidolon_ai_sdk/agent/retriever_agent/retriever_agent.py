from typing import Annotated, List
from urllib.parse import urlparse

from fastapi import Body
from pydantic import model_validator, Field

from eidolon_ai_sdk.agent.agent import register_program, AgentState
from eidolon_ai_sdk.agent.doc_manager.document_manager import DocumentManager
from eidolon_ai_sdk.agent.doc_manager.loaders.filesystem_loader import FilesystemLoader
from eidolon_ai_sdk.agent.retriever_agent.retriever import RetrieverSpec, Retriever, DocSummary
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable, Reference
from eidolon_ai_sdk.util.class_utils import fqn


def make_description(agent: object, _handler: FnHandler) -> str:
    # noinspection PyUnresolvedReferences
    return agent.spec.description


class RetrieverAgentSpec(RetrieverSpec):
    name: str = Field(description="The name of the document store to use.")
    description: str = Field(
        description="A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc..."
    )
    # these three fields are required and override the defaults of the subcomponents
    loader_root_location: str = Field(None, description="A URL specifying the root location of the loader.")

    loader_pattern: str = Field(default="**/*", description="The search pattern to use when loading files.")
    document_manager: Reference[DocumentManager]

    # noinspection PyMethodParameters
    @model_validator(mode="before")
    def set_fields(cls, value):
        spec = value
        if "document_manager" not in spec:
            spec["document_manager"] = dict()
        doc_manager_spec = spec["document_manager"]
        # always set name
        doc_manager_spec["name"] = spec["name"]
        if "loader" not in doc_manager_spec:
            doc_manager_spec["loader"] = dict()
        if "spec" not in doc_manager_spec["loader"]:
            doc_manager_spec["loader"]["spec"] = dict()

        if "loader_root_location" in spec:
            loader_url = urlparse(spec["loader_root_location"])
            if loader_url.scheme == "file":
                doc_manager_spec["loader"]["implementation"] = fqn(FilesystemLoader)
                doc_manager_spec["loader"]["root_dir"] = spec["loader_root_location"][7:]
            else:
                raise ValueError("loader_root_location spec must be a file:// url")
        if "loader_pattern" in spec:
            doc_manager_spec["loader"]["pattern"] = spec["loader_pattern"]

        return value


class RetrieverAgent(Retriever, Specable[RetrieverAgentSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.document_manager = self.spec.document_manager.instantiate()
        self.document_manager.collection_name = f"doc_contents_{self.spec.name}"

    @register_program()
    async def list_files(self) -> AgentState[List[str]]:
        """
        List the files in the document store.
        :return: The response from the cpu
        """
        files = [item async for item in await self.document_manager.list_files()]
        return AgentState(name="idle", data=files)

    @register_program(description=make_description)
    async def search(
        self, question: Annotated[str, Body(description="The question to search for", embed=True)]
    ) -> List[DocSummary]:
        """
        Process the question by searching the document store.
        :param question: The question to process
        :return: The response from the cpu
        """
        await self.document_manager.sync_docs()

        return await super().search(f"doc_contents_{self.spec.name}", question)
