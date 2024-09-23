import asyncio
from typing import AsyncIterable

from pydantic import BaseModel, Field

from eidolon_ai_sdk.agent.retriever_agent.document_reranker import DocumentReranker
from eidolon_ai_sdk.agent.retriever_agent.document_retriever import DocumentRetriever
from eidolon_ai_sdk.agent.retriever_agent.question_transformer import QuestionTransformer
from eidolon_ai_sdk.agent.retriever_agent.result_summarizer import ResultSummarizer, DocSummary
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class RetrieverSpec(BaseModel):
    max_num_results: int = Field(default=10, description="The maximum number of results to consider.")
    question_transformer: AnnotatedReference[QuestionTransformer]
    document_retriever: AnnotatedReference[DocumentRetriever]
    document_reranker: AnnotatedReference[DocumentReranker]
    result_summarizer: AnnotatedReference[ResultSummarizer]


class Retriever(Specable[RetrieverSpec]):
    document_retriever: DocumentRetriever
    document_reranker: DocumentReranker
    question_transformer: QuestionTransformer
    result_summarizer: ResultSummarizer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)

        self.question_transformer = (
            self.spec.question_transformer.instantiate() if self.spec.question_transformer else None
        )
        self.document_reranker = self.spec.document_reranker.instantiate()
        self.document_retriever = self.spec.document_retriever.instantiate()
        self.result_summarizer = self.spec.result_summarizer.instantiate()

    async def do_search(
        self, vector_collection_name: str, apu: APU, process_id: str, question: str
    ) -> AsyncIterable[DocSummary]:
        """
        Process the question by searching the document store.
        :param process_id:
        :param apu:
        :param vector_collection_name:
        :param question: The question to process
        :return: The response from the apu
        """
        if self.question_transformer:
            questions = await self.question_transformer.transform(apu, process_id, question)
        else:
            questions = [question]
        _docs = await asyncio.gather(*(self._embed_question(vector_collection_name, question) for question in questions))
        question_to_docs = {tu[0]: tu[1] for tu in zip(questions, _docs)}
        rerank_questions = {}
        for question, docs in question_to_docs.items():
            rerank_questions[question] = {doc.id: doc.score for doc in docs}

        reranked_docs = await self.document_reranker.rerank(rerank_questions)

        # now limit reranked_docs to max_num_results
        reranked_docs = reranked_docs[: self.spec.max_num_results]

        docs = await self.document_retriever.get_docs(vector_collection_name, [doc[0] for doc in reranked_docs])

        return self.result_summarizer.summarize(docs)

    async def _embed_question(self, vector_collection_name, question):
        embedded_q = await AgentOS.similarity_memory.embed_text(question)
        results_ = await AgentOS.similarity_memory.raw_query(
            vector_collection_name, embedded_q, self.spec.max_num_results
        )
        return results_
