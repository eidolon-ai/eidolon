from typing import Tuple

from eidos_sdk.agent.doc_manager.loaders.base_loader import BaseLoader
from eidos_sdk.agent.doc_manager.loaders.filesystem_loader import FilesystemLoader
from eidos_sdk.agent.doc_manager.parsers.auto_parser import AutoParser
from eidos_sdk.agent.doc_manager.parsers.base_parser import BaseParser
from eidos_sdk.agent.doc_manager.transformer.auto_transformer import AutoTransformer
from eidos_sdk.agent.doc_manager.transformer.document_transformer import BaseDocumentTransformer
from eidos_sdk.agent.generic_agent import GenericAgent
from eidos_sdk.agent.retriever_agent.document_reranker import RAGFusionReranker, DocumentReranker
from eidos_sdk.agent.retriever_agent.multi_question_transformer import MultiQuestionTransformer
from eidos_sdk.agent.retriever_agent.question_transformer import QuestionTransformer
from eidos_sdk.agent.tot_agent.checker import ToTChecker
from eidos_sdk.agent.tot_agent.thought_generators import BaseThoughtGenerationStrategy, ProposePromptStrategy
from eidos_sdk.agent.tot_agent.tot_agent import TreeOfThoughtsAgent
from eidos_sdk.cpu.agent_cpu import AgentCPU
from eidos_sdk.cpu.agent_io import IOUnit
from eidos_sdk.cpu.conversation_memory_unit import ConversationalMemoryUnit
from eidos_sdk.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidos_sdk.cpu.llm.open_ai_llm_unit import OpenAIGPT
from eidos_sdk.cpu.llm.open_ai_speech import OpenAiSpeech
from eidos_sdk.cpu.llm_unit import LLMUnit
from eidos_sdk.cpu.memory_unit import MemoryUnit
from eidos_sdk.cpu.message_summarizer import MessageSummarizer
from eidos_sdk.cpu.no_memory_cpu import NoMemoryCPU
from eidos_sdk.cpu.summarization_memory_unit import SummarizationMemoryUnit
from eidos_sdk.memory.chroma_vector_store import ChromaVectorStore
from eidos_sdk.memory.embeddings import NoopEmbedding, Embedding, OpenAIEmbedding
from eidos_sdk.memory.file_memory import FileMemory
from eidos_sdk.memory.file_system_vector_store import FileSystemVectorStore
from eidos_sdk.memory.local_file_memory import LocalFileMemory
from eidos_sdk.memory.local_symbolic_memory import LocalSymbolicMemory
from eidos_sdk.memory.mongo_symbolic_memory import MongoSymbolicMemory
from eidos_sdk.memory.noop_memory import NoopVectorStore
from eidos_sdk.memory.semantic_memory import SymbolicMemory
from eidos_sdk.memory.similarity_memory import SimilarityMemory
from eidos_sdk.memory.vector_store import VectorStore
from eidos_sdk.system.agent_machine import AgentMachine
from eidos_sdk.system.resources.reference_resource import ReferenceResource
from eidos_sdk.system.resources.resources_base import Metadata
from eidos_sdk.util.class_utils import fqn


def _to_resource(maybe_tuple: type | Tuple[type, type]) -> ReferenceResource:
    if isinstance(maybe_tuple, tuple):
        return ReferenceResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name=maybe_tuple[0].__name__),
            spec=maybe_tuple[1].__name__,
        )
    else:
        return ReferenceResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name=maybe_tuple.__name__),
            spec=fqn(maybe_tuple),
        )


def named_builtins():
    """
    Shorthand for defining builtin resources since most are just a pointer to a class.

    This will allow us to capture refactoring location of a class automatically.

    Tuples map the name of the first element to the name of the second.
    Single types map the name of first element to it's fqn.
    """

    builtin_list = [
        AgentMachine,

        # agents
        GenericAgent,
        TreeOfThoughtsAgent,

        # cpu
        (AgentCPU, ConversationalAgentCPU),
        ConversationalAgentCPU,
        NoMemoryCPU,

        # cpu components
        IOUnit,

        (LLMUnit, OpenAIGPT),
        OpenAIGPT,

        (MemoryUnit, ConversationalMemoryUnit),
        ConversationalMemoryUnit,
        SummarizationMemoryUnit,

        # machine components
        (SymbolicMemory, MongoSymbolicMemory),
        MongoSymbolicMemory,
        LocalSymbolicMemory,

        (FileMemory, LocalFileMemory),
        LocalFileMemory,
        SimilarityMemory,

        (Embedding, NoopEmbedding),
        NoopEmbedding,
        OpenAIEmbedding,

        (VectorStore, NoopVectorStore),
        NoopVectorStore,
        FileSystemVectorStore,
        ChromaVectorStore,

        # sub components
        (BaseParser, AutoParser),
        AutoParser,

        (BaseDocumentTransformer, AutoTransformer),
        AutoTransformer,

        (BaseThoughtGenerationStrategy, ProposePromptStrategy),
        ProposePromptStrategy,

        (QuestionTransformer, MultiQuestionTransformer),
        MultiQuestionTransformer,
        (DocumentReranker, RAGFusionReranker),
        RAGFusionReranker,

        (BaseLoader, FilesystemLoader),
        FilesystemLoader,

        ToTChecker,
        OpenAiSpeech,
        MessageSummarizer,
    ]
    return [_to_resource(maybe_tuple) for maybe_tuple in builtin_list]
