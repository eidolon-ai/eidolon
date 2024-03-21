from typing import Tuple

from openai import AsyncOpenAI
from openai.lib.azure import AsyncAzureOpenAI
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import SpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
from opentelemetry.sdk.trace.sampling import Sampler

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import DocumentLoader
from eidolon_ai_sdk.agent.doc_manager.loaders.filesystem_loader import FilesystemLoader
from eidolon_ai_sdk.agent.doc_manager.loaders.github_loader import GitHubLoader
from eidolon_ai_sdk.agent.doc_manager.parsers.auto_parser import AutoParser
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser
from eidolon_ai_sdk.agent.doc_manager.transformer.auto_transformer import AutoTransformer
from eidolon_ai_sdk.agent.doc_manager.transformer.document_transformer import DocumentTransformer
from eidolon_ai_sdk.agent.generic_agent import GenericAgent
from eidolon_ai_sdk.agent.openai_whisper_agent import AutonomousSpeechAgent
from eidolon_ai_sdk.agent.retriever_agent.document_reranker import RAGFusionReranker, DocumentReranker
from eidolon_ai_sdk.agent.retriever_agent.multi_question_transformer import MultiQuestionTransformer
from eidolon_ai_sdk.agent.retriever_agent.question_transformer import QuestionTransformer
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.agent.tot_agent.checker import ToTChecker
from eidolon_ai_sdk.agent.tot_agent.thought_generators import ThoughtGenerationStrategy, ProposePromptStrategy
from eidolon_ai_sdk.agent.tot_agent.tot_agent import TreeOfThoughtsAgent
from eidolon_ai_sdk.builtins.components.opentelemetry import OpenTelemetryManager, CustomSampler, NoopSpanExporter
from eidolon_ai_sdk.builtins.components.usage import UsageMiddleware
from eidolon_ai_sdk.builtins.logic_units.web_search import WebSearch, Browser, Search
from eidolon_ai_sdk.cpu.agent_cpu import AgentCPU
from eidolon_ai_sdk.cpu.agent_io import IOUnit
from eidolon_ai_sdk.cpu.conversation_memory_unit import RawMemoryUnit
from eidolon_ai_sdk.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidolon_ai_sdk.cpu.llm.open_ai_llm_unit import OpenAIGPT
from eidolon_ai_sdk.cpu.llm.open_ai_speech import OpenAiSpeech
from eidolon_ai_sdk.cpu.llm_unit import LLMUnit
from eidolon_ai_sdk.cpu.memory_unit import MemoryUnit
from eidolon_ai_sdk.security.azure_authorizer import AzureJWTProcessor
from eidolon_ai_sdk.security.google_auth import GoogleJWTProcessor
from eidolon_ai_sdk.system.dynamic_middleware import Middleware, MultiMiddleware
from eidolon_ai_sdk.system.process_file_system import ProcessFileSystem
from eidolon_ai_usage_client.client import UsageClient

try:
    from eidolon_ai_sdk.memory.chroma_vector_store import ChromaVectorStore
except ImportError:
    logger.warning("Error, ChromaVectorStore is not available")
    ChromaVectorStore = None

from eidolon_ai_sdk.memory.embeddings import NoopEmbedding, Embedding, OpenAIEmbedding
from eidolon_ai_sdk.memory.file_memory import FileMemory
from eidolon_ai_sdk.memory.local_file_memory import LocalFileMemory
from eidolon_ai_sdk.memory.local_symbolic_memory import LocalSymbolicMemory
from eidolon_ai_sdk.memory.mongo_symbolic_memory import MongoSymbolicMemory
from eidolon_ai_sdk.memory.noop_memory import NoopVectorStore
from eidolon_ai_sdk.memory.semantic_memory import SymbolicMemory
from eidolon_ai_sdk.memory.similarity_memory import SimilarityMemory
from eidolon_ai_sdk.memory.vector_store import VectorStore
from eidolon_ai_sdk.security.security_manager import SecurityManager
from eidolon_ai_sdk.security.functional_authorizer import (
    FunctionalAuthorizer,
    NoopFunctionalAuth,
    GlobPatternFunctionalAuthorizer,
)
from eidolon_ai_sdk.security.process_authorizer import ProcessAuthorizer, PrivateAuthorizer
from eidolon_ai_sdk.security.authentication_processor import AuthenticationProcessor, NoopAuthProcessor
from eidolon_ai_sdk.system.agent_machine import AgentMachine
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn
from eidolon_ai_sdk.util.replay import ReplayConfig


def _to_resource(maybe_tuple: type | Tuple[type | str, type]) -> ReferenceResource:
    if isinstance(maybe_tuple, tuple):
        name = maybe_tuple[0] if isinstance(maybe_tuple[0], str) else maybe_tuple[0].__name__
        return ReferenceResource(
            apiVersion="eidolon/v1",
            metadata=Metadata(name=name),
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
        # security manager
        SecurityManager,
        (AuthenticationProcessor, NoopAuthProcessor),
        NoopAuthProcessor,
        GoogleJWTProcessor,
        AzureJWTProcessor,
        (ProcessAuthorizer, PrivateAuthorizer),
        PrivateAuthorizer,
        (FunctionalAuthorizer, NoopFunctionalAuth),
        NoopFunctionalAuth,
        GlobPatternFunctionalAuthorizer,
        # agents
        ("Agent", SimpleAgent),
        SimpleAgent,
        GenericAgent,  # deprecated
        TreeOfThoughtsAgent,
        RetrieverAgent,
        AutonomousSpeechAgent,
        # cpu
        (AgentCPU, ConversationalAgentCPU),
        ConversationalAgentCPU,
        # cpu components
        IOUnit,
        (LLMUnit, OpenAIGPT),
        OpenAIGPT,
        (MemoryUnit, RawMemoryUnit),
        RawMemoryUnit,
        WebSearch,
        Search,
        Browser,
        # machine components
        (SymbolicMemory, MongoSymbolicMemory),
        MongoSymbolicMemory,
        LocalSymbolicMemory,
        (FileMemory, LocalFileMemory),
        LocalFileMemory,
        SimilarityMemory,
        (Embedding, OpenAIEmbedding),
        NoopEmbedding,
        OpenAIEmbedding,
        (VectorStore, ChromaVectorStore),
        NoopVectorStore,
        ChromaVectorStore,
        # middleware
        (Middleware, MultiMiddleware),
        MultiMiddleware,
        UsageMiddleware,
        # open telemetry
        OpenTelemetryManager,
        (SpanExporter, NoopSpanExporter),
        NoopSpanExporter,
        OTLPSpanExporter,
        (Sampler, CustomSampler),
        CustomSampler,
        (SpanProcessor, BatchSpanProcessor),
        BatchSpanProcessor,
        ProcessFileSystem,
        # sub components
        (DocumentParser, AutoParser),
        AutoParser,
        (DocumentTransformer, AutoTransformer),
        AutoTransformer,
        (ThoughtGenerationStrategy, ProposePromptStrategy),
        ProposePromptStrategy,
        (QuestionTransformer, MultiQuestionTransformer),
        MultiQuestionTransformer,
        (DocumentReranker, RAGFusionReranker),
        RAGFusionReranker,
        (DocumentLoader, FilesystemLoader),
        FilesystemLoader,
        GitHubLoader,
        ToTChecker,
        OpenAiSpeech,
        AsyncOpenAI,
        AsyncAzureOpenAI,
        UsageClient,
        # config objects
        ReplayConfig,
    ]
    return [_to_resource(maybe_tuple) for maybe_tuple in builtin_list if maybe_tuple]
