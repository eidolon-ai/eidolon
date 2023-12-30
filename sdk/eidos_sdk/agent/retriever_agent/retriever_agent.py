from fastapi import Body
from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel, Field
from typing import Optional, Annotated, List

from eidos_sdk.agent.agent import register_action, register_program, AgentState
from eidos_sdk.agent.doc_manager.document_manager import DocumentManager
from eidos_sdk.agent.retriever_agent.document_reranker import DocumentReranker, RAGFusionReranker
from eidos_sdk.agent.retriever_agent.question_transformer import QuestionTransformer
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.cpu.agent_cpu import AgentCPU
from eidos_sdk.cpu.agent_io import UserTextCPUMessage
from eidos_sdk.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidos_sdk.system.reference_model import Specable, AnnotatedReference, Reference


class RetrieverAgentSpec(BaseModel):
    doc_store_name: str = Field(description="The name of the document store to use.")
    document_manager: Reference[DocumentManager]

    cpu: AnnotatedReference[AgentCPU, ConversationalAgentCPU]
    prompt: str = Field(
        default="""Important:
Answer with the facts listed in the list of sources below. If there isn't enough information below, say you don't know.
If asking a clarifying question to the user would help, ask the question. 
ALWAYS return a "SOURCES" part in your answer, except for small-talk conversations.

Question: {{question}}
Sources:
---------------------
    {{summaries}}
---------------------""",
        description="The prompt to be used for the question transformer. This should be a template where the user question is the field {{question}} and the summaries go in the {{summaries}} field."
    )
    max_num_results: int = Field(default=10, description="The maximum number of results to send to cpu.")
    question_transformer: Optional[AnnotatedReference[QuestionTransformer]] = Field(default=None, description="The question transformer to use. Defaults to no transformation.")
    document_reranker: AnnotatedReference[DocumentReranker, RAGFusionReranker]


class RetrieverAgent(Specable[RetrieverAgentSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.document_manager = self.spec.document_manager.instantiate()

        self.cpu = self.spec.cpu.instantiate()
        self.question_transformer = self.spec.question_transformer.instantiate() if self.spec.question_transformer else None
        self.document_reranker = self.spec.document_reranker.instantiate()

    async def _do_search(self, question: str, process_id: str):

        await self.document_manager.sync_docs()

        if self.question_transformer:
            questions = await self.question_transformer.transform(question)
        else:
            questions = [question]
        question_to_docs = {}
        for question in questions:
            embedded_q = await AgentOS.embedder.embed_text(question)
            results_ = await AgentOS.similarity_memory.raw_query(f"doc_contents_{self.spec.doc_store_name}", embedded_q, self.spec.max_num_results)
            question_to_docs[question] = results_
        rerank_questions = {}
        for question, docs in question_to_docs.items():
            rerank_questions[question] = {doc.id: doc.score for doc in docs}

        reranked_docs = await self.document_reranker.rerank(rerank_questions)

        # now limit reranked_docs to max_num_results
        reranked_docs = reranked_docs[:self.spec.max_num_results]

        docs = AgentOS.similarity_memory.get_docs(f"doc_contents_{self.spec.doc_store_name}", [doc[0] for doc in reranked_docs])
        # todo -- add source of the document and metadata to the summaries
        summaries = []
        async for doc in docs:
            summaries.append(doc.model_dump_json())
        summaries = "\n".join(summaries)

        # now send the question and summaries to the cpu
        thread = await self.cpu.main_thread(process_id)
        env = Environment(undefined=StrictUndefined)
        userPrompt = env.from_string(self.spec.prompt).render(question=question, summaries=summaries)
        response = await thread.schedule_request(
            prompts=[UserTextCPUMessage(prompt=userPrompt)], output_format="str"
        )

        return response

    @register_program()
    async def list_files(self) -> AgentState[List[str]]:
        """
        List the files in the document store.
        :return: The response from the cpu
        """
        files = [item async for item in await self.document_manager.list_files()]
        return AgentState(name="idle", data=files)

    @register_program()
    async def search(self, process_id, question: Annotated[str, Body(description="The question to search for", embed=True)]) -> AgentState[str]:
        """
        Process the question by searching the document store and then sending the results to the cpu.
        :param question: The question to process
        :return: The response from the cpu
        """
        return AgentState(name="idle", data=await self._do_search(question, process_id))

    @register_action("idle")
    async def followup_question(self, process_id, question: Annotated[str, Body(description="The question to search for", embed=True)]) -> AgentState[str]:
        """
        Process the question by searching the document store and then sending the results to the cpu.
        This is used to ask a followup question after the user has already asked a question.
        Only use this if the user asks a followup question to an answer, otherwise use search.
        :param process_id:
        :param question: The question to process
        :return: The response from the cpu
        """
        return AgentState(name="idle", data=await self._do_search(question, process_id))
