from typing import Annotated, List, Optional
from urllib.parse import urlparse

from fastapi import Body
from pydantic import model_validator, Field

from eidolon_ai_sdk.agent.agent import register_program, AgentState
from eidolon_ai_sdk.agent.doc_manager.document_manager import DocumentManager
from eidolon_ai_sdk.agent.doc_manager.loaders.filesystem_loader import FilesystemLoader
from eidolon_ai_sdk.agent.retriever_agent.result_summarizer import DocSummary
from eidolon_ai_sdk.agent.retriever_agent.retriever import RetrieverSpec, Retriever
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable, Reference, AnnotatedReference
from eidolon_ai_sdk.util.class_utils import fqn


def make_description(agent: object, _handler: FnHandler) -> str:
    # noinspection PyUnresolvedReferences
    return agent.spec.description


class RetrieverAgentSpec(RetrieverSpec):
    """
    A RetrieverAgent is an agent that will take a query, rewrite it for better similarity vector search, and then perform the vector search on the document store.
    The agent will dynamically load and embed files, so it is not performant for loading large bodies of files, but performs very well for small to medium-sized document stores (hundreds to thousands of documents) which are updating frequently.
    """

    name: str = Field(description="The name of the document store to use.")
    description: str = Field(
        description="A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc..."
    )
    # these three fields are required and override the defaults of the subcomponents
    loader_root_location: Optional[str] = Field(None, description="A URL specifying the root location of the loader.")

    loader_pattern: Optional[str] = Field(default="**/*", description="The search pattern to use when loading files.")
    document_manager: Optional[Reference[DocumentManager]] = None

    apu: AnnotatedReference[APU] = Field(description="The APU to use for question transformation.")

    # noinspection PyMethodParameters
    @model_validator(mode="before")
    def set_fields(cls, value):
        spec = value
        if "document_manager" not in spec and ("loader_root_location" in spec or "loader_pattern" in spec):
            spec["document_manager"] = dict()
        doc_manager_spec = spec["document_manager"] if "document_manager" in spec else None
        if doc_manager_spec is not None:
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
    apu: APU
    document_manager: DocumentManager

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)

        self.apu = self.spec.apu.instantiate()

        if self.spec.document_manager:
            self.document_manager = self.spec.document_manager.instantiate()
            self.document_manager.collection_name = f"doc_contents_{self.spec.name}"

    @register_program()
    async def list_files(self) -> AgentState[List[str]]:
        """
        List the files in the document store.
        :return: The response from the apu
        """
        if self.document_manager:
            files = [item async for item in await self.document_manager.list_files()]
        else:
            files = []
        return AgentState(name="idle", data=files)

    @register_program(description=make_description)
    async def search(
        self, process_id, question: Annotated[str, Body(description="The question to search for", embed=True)]
    ) -> List[DocSummary]:
        """
        Process the question by searching the document store.
        :param question: The question to process
        :return: The response from the apu
        """
        if hasattr(self, "document_manager") and self.document_manager:
            await self.document_manager.sync_docs()

        results = await super().do_search(f"doc_contents_{self.spec.name}", self.apu, process_id, question)
        return [doc async for doc in results]
