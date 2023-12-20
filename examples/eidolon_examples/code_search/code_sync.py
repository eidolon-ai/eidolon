from typing import List

from eidolon_examples.code_search.vector_search_directory_sync import VectorSearchDirSync
from eidos_sdk.memory.document import Document
from eidos_sdk.memory.parsers.base_parser import BaseParserSpec, DataBlob
from eidos_sdk.memory.parsers.code_ast_parsers.programing_language_parser import LanguageParser, LanguageParserSpec
from eidos_sdk.memory.parsers.text_parsers import TextParser
from eidos_sdk.memory.transformer.text_splitters import MarkdownTextSplitter, RecursiveCharacterTextSplitterSpec


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
