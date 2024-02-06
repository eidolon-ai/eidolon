from fastapi import Body
from pydantic import BaseModel, Field, model_validator
from typing import Annotated, List
from urllib.parse import urlparse

from eidolon_ai_sdk.agent.agent import register_program, AgentState
from eidolon_ai_sdk.agent.doc_manager.document_manager import DocumentManager
from eidolon_ai_sdk.agent.doc_manager.loaders.filesystem_loader import FilesystemLoader
from eidolon_ai_sdk.agent.retriever_agent.document_reranker import DocumentReranker
from eidolon_ai_sdk.agent.retriever_agent.question_transformer import QuestionTransformer
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference, Reference
from eidolon_ai_sdk.util.class_utils import fqn


def make_description(agent: object, _handler: FnHandler) -> str:
    # noinspection PyUnresolvedReferences
    return agent.spec.description


class RetrieverAgentSpec(BaseModel):
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

        if "loader_root_location" not in spec:
            raise ValueError("loader_root_location must be specified in the spec")
        loader_url = urlparse(spec["loader_root_location"])
        if loader_url.scheme == "file":
            doc_manager_spec["loader"]["implementation"] = fqn(FilesystemLoader)
            doc_manager_spec["loader"]["root_dir"] = spec["loader_root_location"][7:]
        else:
            raise ValueError("loader_root_location spec must be a file:// url")
        if "loader_pattern" in spec:
            doc_manager_spec["loader"]["pattern"] = spec["loader_pattern"]

        return value

    # these three fields are required and override the defaults of the subcomponents
    name: str = Field(description="The name of the document store to use.")
    description: str = Field(
        description="A detailed description of the the retriever including all necessary information for the calling agent to decide to call this agent, i.e. file type or location or etc..."
    )
    loader_root_location: str = Field(description="A URL specifying the root location of the loader.")

    loader_pattern: str = Field(default="**/*", description="The search pattern to use when loading files.")
    max_num_results: int = Field(default=10, description="The maximum number of results to send to cpu.")

    document_manager: Reference[DocumentManager]
    question_transformer: AnnotatedReference[QuestionTransformer]
    document_reranker: AnnotatedReference[DocumentReranker]


class DocSummary(BaseModel):
    id: str
    file_name: str
    file_path: str
    text: str


class RetrieverAgent(Specable[RetrieverAgentSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.document_manager = self.spec.document_manager.instantiate()

        self.question_transformer = (
            self.spec.question_transformer.instantiate() if self.spec.question_transformer else None
        )
        self.document_reranker = self.spec.document_reranker.instantiate()

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

        if self.question_transformer:
            questions = await self.question_transformer.transform(question)
        else:
            questions = [question]
        question_to_docs = {}
        for question in questions:
            embedded_q = await AgentOS.similarity_memory.embedder.embed_text(question)
            results_ = await AgentOS.similarity_memory.vector_store.raw_query(
                f"doc_contents_{self.spec.name}", embedded_q, self.spec.max_num_results
            )
            question_to_docs[question] = results_
        rerank_questions = {}
        for question, docs in question_to_docs.items():
            rerank_questions[question] = {doc.id: doc.score for doc in docs}

        reranked_docs = await self.document_reranker.rerank(rerank_questions)

        # now limit reranked_docs to max_num_results
        reranked_docs = reranked_docs[: self.spec.max_num_results]

        docs = AgentOS.similarity_memory.vector_store.get_docs(
            f"doc_contents_{self.spec.name}", [doc[0] for doc in reranked_docs]
        )
        summaries = []
        async for doc in docs:
            file_path = doc.metadata["source"]
            summaries.append(
                DocSummary(id=doc.id, file_name=file_path.split("/")[-1], file_path=file_path, text=doc.page_content)
            )

        return summaries
