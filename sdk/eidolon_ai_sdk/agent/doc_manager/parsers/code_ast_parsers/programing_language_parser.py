from typing import Dict, Any, Literal, Iterable, Optional

from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParserSpec, DocumentParser, DataBlob
from eidolon_ai_sdk.agent.doc_manager.parsers.code_ast_parsers.cobol import CobolASTGenerator
from eidolon_ai_sdk.agent.doc_manager.parsers.code_ast_parsers.javascript import JavaScriptASTGenerator
from eidolon_ai_sdk.agent.doc_manager.parsers.code_ast_parsers.python import PythonASTGenerator
from eidolon_ai_sdk.agent.doc_manager.transformer.text_splitters import Language
from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.system.reference_model import Specable

LANGUAGE_EXTENSIONS: Dict[str, str] = {
    "py": Language.PYTHON,
    "js": Language.JS,
    "cobol": Language.COBOL,
}

LANGUAGE_AST_GENERATORS: Dict[str, Any] = {
    Language.PYTHON: PythonASTGenerator,
    Language.JS: JavaScriptASTGenerator,
    Language.COBOL: CobolASTGenerator,
}


class LanguageParserSpec(DocumentParserSpec):
    language: Optional[Literal["python", "javascript", "cobol"]] = None
    parser_threshold: int = 0


class LanguageParser(DocumentParser, Specable[LanguageParserSpec]):
    def __init__(self, spec: LanguageParserSpec):
        super().__init__(spec)
        self.language = spec.language
        self.parser_threshold = spec.parser_threshold

    def parse(self, blob: DataBlob) -> Iterable[Document]:
        code = blob.as_string()

        language = self.language or (
            LANGUAGE_EXTENSIONS.get(blob.path.rsplit(".", 1)[-1]) if isinstance(blob.path, str) else None
        )

        if language is None:
            yield Document(
                page_content=code,
                metadata={
                    "source": blob.path,
                    "mime_type": blob.mimetype,
                },
            )
            return

        if self.parser_threshold >= len(code.splitlines()):
            yield Document(
                page_content=code,
                metadata={
                    "source": blob.path,
                    "language": language,
                    "mime_type": blob.mimetype,
                },
            )
            return

        generator = LANGUAGE_AST_GENERATORS[language](blob.as_string())
        if not generator.is_valid():
            yield Document(
                page_content=code,
                metadata={
                    "source": blob.path,
                    "mime_type": blob.mimetype,
                },
            )
            return

        for functions_classes in generator.extract_functions_classes():
            yield Document(
                page_content=functions_classes,
                metadata={
                    "source": blob.path,
                    "content_type": "functions_classes",
                    "language": language,
                    "mime_type": blob.mimetype,
                },
            )
        yield Document(
            page_content=generator.simplify_code(),
            metadata={
                "source": blob.path,
                "content_type": "simplified_code",
                "language": language,
                "mime_type": blob.mimetype,
            },
        )
