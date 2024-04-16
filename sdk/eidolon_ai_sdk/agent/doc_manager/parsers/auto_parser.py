from typing import Iterable

from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser, DataBlob, DocumentParserSpec
from eidolon_ai_sdk.agent.doc_manager.parsers.code_ast_parsers.programing_language_parser import LanguageParserSpec
from eidolon_ai_sdk.agent.doc_manager.parsers.pdf_parsers import PyPDFParserSpec
from eidolon_ai_sdk.agent.doc_manager.parsers.text_parsers import BS4HTMLParserSpec
from eidolon_ai_sdk.memory.document import Document


class AutoParser(DocumentParser):
    def parse(self, blob: DataBlob) -> Iterable[Document]:
        if blob.mimetype == "application/pdf":
            from eidolon_ai_sdk.agent.doc_manager.parsers.pdf_parsers import PyPDFParser

            yield from PyPDFParser(PyPDFParserSpec()).parse(blob)
        elif (
            blob.mimetype == "application/msword"
            or blob.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            from eidolon_ai_sdk.agent.doc_manager.parsers.ms_word_parser import MsWordParser

            yield from MsWordParser(DocumentParserSpec()).parse(blob)
        elif blob.mimetype == "text/html":
            from eidolon_ai_sdk.agent.doc_manager.parsers.text_parsers import BS4HTMLParser

            yield from BS4HTMLParser(BS4HTMLParserSpec()).parse(blob)
        elif blob.mimetype == "text/x-python":
            from eidolon_ai_sdk.agent.doc_manager.parsers.code_ast_parsers.programing_language_parser import (
                LanguageParser,
            )

            yield from LanguageParser(LanguageParserSpec(language="python")).parse(blob)
        elif blob.mimetype == "application/javascript":
            from eidolon_ai_sdk.agent.doc_manager.parsers.code_ast_parsers.programing_language_parser import (
                LanguageParser,
            )

            yield from LanguageParser(LanguageParserSpec(language="javascript")).parse(blob)
        elif blob.mimetype == "text/x-cobol":
            from eidolon_ai_sdk.agent.doc_manager.parsers.code_ast_parsers.programing_language_parser import (
                LanguageParser,
            )

            yield from LanguageParser(LanguageParserSpec(language="cobol")).parse(blob)
        elif (
            blob.mimetype
            and blob.mimetype.startswith("text/")
            or blob.mimetype == "application/json"
            or blob.mimetype == "application/xml"
            or blob.mimetype == "application/yaml"
            or blob.mimetype == "application/x-yaml"
            or blob.mimetype == "application/x-yml"
        ):
            from eidolon_ai_sdk.agent.doc_manager.parsers.text_parsers import TextParser

            yield from TextParser(DocumentParserSpec()).parse(blob)
        else:
            raise ValueError(f"Unsupported mimetype: {blob.mimetype}")
