from typing import Tuple, List

from azure.identity import DefaultAzureCredential, EnvironmentCredential
from openai import AsyncOpenAI
from openai.lib.azure import AsyncAzureOpenAI
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import SpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
from opentelemetry.sdk.trace.sampling import Sampler

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent.api_agent import APIAgent
from eidolon_ai_sdk.agent.audio_agent import AutonomousSpeechAgent
from eidolon_ai_sdk.agent.browser.scraping_agent import WebScrapingAgent
from eidolon_ai_sdk.agent.browser.search_agent import WebSearchAgent
from eidolon_ai_sdk.agent.browser.web_researcher import WebResearcher
from eidolon_ai_sdk.agent.doc_manager.document_manager import DocumentManager
from eidolon_ai_sdk.agent.doc_manager.document_processor import DocumentProcessor
from eidolon_ai_sdk.agent.doc_manager.loaders.azure_loader import AzureLoader
from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import DocumentLoader
from eidolon_ai_sdk.agent.doc_manager.loaders.filesystem_loader import FilesystemLoader
from eidolon_ai_sdk.agent.doc_manager.loaders.github_loader import GitHubLoader
from eidolon_ai_sdk.agent.doc_manager.loaders.s3_loader import S3Loader
from eidolon_ai_sdk.agent.doc_manager.parsers.auto_parser import AutoParser
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser
from eidolon_ai_sdk.agent.doc_manager.transformer.auto_transformer import AutoTransformer
from eidolon_ai_sdk.agent.doc_manager.transformer.document_transformer import DocumentTransformer
from eidolon_ai_sdk.agent.generic_agent import GenericAgent
from eidolon_ai_sdk.agent.retriever_agent.document_reranker import RAGFusionReranker, DocumentReranker
from eidolon_ai_sdk.agent.retriever_agent.document_retriever import SimilarityMemoryRetriever, DocumentRetriever
from eidolon_ai_sdk.agent.retriever_agent.multi_question_transformer import MultiQuestionTransformer
from eidolon_ai_sdk.agent.retriever_agent.question_transformer import QuestionTransformer
from eidolon_ai_sdk.agent.retriever_agent.result_summarizer import ResultSummarizer
from eidolon_ai_sdk.agent.retriever_agent.retriever import Retriever
from eidolon_ai_sdk.agent.retriever_agent.retriever_agent import RetrieverAgent
from eidolon_ai_sdk.agent.simple_agent import SimpleAgent
from eidolon_ai_sdk.agent.sql_agent.agent import SqlAgent
from eidolon_ai_sdk.agent.sql_agent.client import SqlClient, SqlAlchemy
from eidolon_ai_sdk.agent.tot_agent.checker import ToTChecker
from eidolon_ai_sdk.agent.tot_agent.thought_generators import ThoughtGenerationStrategy, ProposePromptStrategy
from eidolon_ai_sdk.agent.tot_agent.tot_agent import TreeOfThoughtsAgent
from eidolon_ai_sdk.agent_os_interfaces import FileMemory, SymbolicMemory, SimilarityMemory, SecurityManager
from eidolon_ai_sdk.builtins.components.opentelemetry import OpenTelemetryManager, CustomSampler, NoopSpanExporter
from eidolon_ai_sdk.builtins.components.usage import UsageMiddleware
from eidolon_ai_sdk.builtins.logic_units.api_logic_unit import ApiLogicUnit
from eidolon_ai_sdk.builtins.logic_units.web_search import WebSearch, Browser, Search
from eidolon_ai_sdk.apu.agent_io import IOUnit
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.apu.audio_unit import AudioUnit
from eidolon_ai_sdk.apu.conversation_memory_unit import RawMemoryUnit
from eidolon_ai_sdk.apu.conversational_apu import ConversationalAPU
from eidolon_ai_sdk.apu.llm.anthropic_llm_unit import AnthropicLLMUnit
from eidolon_ai_sdk.apu.llm.mistral_llm_unit import MistralGPT
from eidolon_ai_sdk.apu.llm.ollama_llm_unit import OllamaLLMUnit
from eidolon_ai_sdk.apu.llm.open_ai_connection_handler import OpenAIConnectionHandler, AzureOpenAIConnectionHandler
from eidolon_ai_sdk.apu.llm.open_ai_image_unit import OpenAIImageUnit
from eidolon_ai_sdk.apu.llm.open_ai_llm_unit import OpenAIGPT
from eidolon_ai_sdk.apu.llm.open_ai_speech import OpenAiSpeech
from eidolon_ai_sdk.apu.llm_unit import LLMUnit, LLMModel
from eidolon_ai_sdk.apu.memory_unit import MemoryUnit
from eidolon_ai_sdk.apu.tool_call_unit import ToolCallLLMWrapper
from eidolon_ai_sdk.memory.azure_file_memory import AzureFileMemory
from eidolon_ai_sdk.memory.s3_file_memory import S3FileMemory
from eidolon_ai_sdk.security.azure_authorizer import AzureJWTProcessor
from eidolon_ai_sdk.security.google_auth import GoogleJWTProcessor
from eidolon_ai_sdk.system.dynamic_middleware import Middleware, MultiMiddleware
from eidolon_ai_sdk.system.process_file_system import ProcessFileSystem, ProcessFileSystemImpl
from eidolon_ai_usage_client.client import UsageClient

try:
    from eidolon_ai_sdk.memory.chroma_vector_store import ChromaVectorStore
except ImportError:
    logger.warning("Error, ChromaVectorStore is not available")
    ChromaVectorStore = None

from eidolon_ai_sdk.memory.embeddings import NoopEmbedding, Embedding, OpenAIEmbedding
from eidolon_ai_sdk.memory.local_file_memory import LocalFileMemory
from eidolon_ai_sdk.memory.local_symbolic_memory import LocalSymbolicMemory
from eidolon_ai_sdk.memory.mongo_symbolic_memory import MongoSymbolicMemory
from eidolon_ai_sdk.memory.noop_memory import NoopVectorStore
from eidolon_ai_sdk.memory.similarity_memory import SimilarityMemoryImpl
from eidolon_ai_sdk.memory.vector_store import VectorStore
from eidolon_ai_sdk.security.security_manager import SecurityManagerImpl
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


def named_builtins() -> List[ReferenceResource]:
    """
    Shorthand for defining builtin resources since most are just a pointer to a class.

    This will allow us to capture refactoring location of a class automatically.

    Tuples map the name of the first element to the name of the second.
    Single types map the name of first element to it's fqn.
    """

    builtin_list = [
        AgentMachine,
        # security manager
        (SecurityManager, SecurityManagerImpl),
        SecurityManagerImpl,
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
        SqlAgent,
        # apu
        (APU, ConversationalAPU),
        ConversationalAPU,
        # apu components
        IOUnit,
        (LLMUnit, OpenAIGPT),
        OpenAIGPT,
        MistralGPT,
        AnthropicLLMUnit,
        OllamaLLMUnit,
        LLMModel,
        (MemoryUnit, RawMemoryUnit),
        RawMemoryUnit,
        WebSearch,
        Search,
        Browser,
        Retriever,
        WebScrapingAgent,
        WebSearchAgent,
        WebResearcher,
        ApiLogicUnit,
        APIAgent,
        # machine components
        (SymbolicMemory, MongoSymbolicMemory),
        MongoSymbolicMemory,
        LocalSymbolicMemory,
        (FileMemory, LocalFileMemory),
        LocalFileMemory,
        S3FileMemory,
        AzureFileMemory,
        (SimilarityMemory, SimilarityMemoryImpl),
        SimilarityMemoryImpl,
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
        (ProcessFileSystem, ProcessFileSystemImpl),
        ProcessFileSystemImpl,
        # sub components
        (SqlClient, SqlAlchemy),
        SqlAlchemy,
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
        (DocumentRetriever, SimilarityMemoryRetriever),
        SimilarityMemoryRetriever,
        ResultSummarizer,
        (DocumentLoader, FilesystemLoader),
        DocumentProcessor,
        DocumentManager,
        FilesystemLoader,
        GitHubLoader,
        S3Loader,
        AzureLoader,
        ToTChecker,
        (AudioUnit, OpenAiSpeech),
        OpenAiSpeech,
        AsyncOpenAI,
        AsyncAzureOpenAI,
        UsageClient,
        OpenAIConnectionHandler,
        AzureOpenAIConnectionHandler,
        OpenAIImageUnit,
        ToolCallLLMWrapper,
        DefaultAzureCredential,
        EnvironmentCredential,
        # config objects
        ReplayConfig,
    ]
    return [_to_resource(maybe_tuple) for maybe_tuple in builtin_list if maybe_tuple]
