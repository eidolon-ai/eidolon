from typing import List

from eidolon_examples.code_search.vector_search_directory_sync import VectorSearchDirSync
from eidos.memory.document import Document
from eidos.memory.parsers.base_parser import DataBlob, BaseParserSpec
from eidos.memory.parsers.code_ast_parsers.programing_language_parser import LanguageParser, LanguageParserSpec
from eidos.memory.parsers.text_parsers import TextParser
from eidos.memory.transformer.text_splitters import MarkdownTextSplitter, RecursiveCharacterTextSplitterSpec
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.memory.embeddings import OpenAIEmbedding, OpenAIEmbeddingSpec
from eidos_sdk.memory.parsers.base_parser import DataBlob
from eidos_sdk.memory.parsers.code_ast_parsers.programing_language_parser import LanguageParser, LanguageParserSpec
from watchdog.events import FileSystemEvent, FileSystemMovedEvent

from eidolon_examples.code_search.file_system_watcher import FileSystemWatcher


def hash_file(file_path, chunk_size=8192):
    """
    Hash the contents of a file using SHA-256.


class CodeSync(VectorSearchDirSync):
    language_parser = LanguageParser(LanguageParserSpec(language="python"))

    async def parse_file(self, data: DataBlob) -> List[Document]:
        return list(self.language_parser.parse(data))


class MarkdownSync(VectorSearchDirSync):
    parser = TextParser(BaseParserSpec())
    splitter = MarkdownTextSplitter(spec=RecursiveCharacterTextSplitterSpec())

    async def parse_file(self, data: DataBlob) -> List[Document]:
        docs = self.parser.parse(data)
        return list(self.splitter.transform_documents(docs))
