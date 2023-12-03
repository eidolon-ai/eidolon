from typing import Dict, Any, Iterable, Literal

from eidolon_sdk.reference_model import Specable
from eidolon_sdk.vector_store.base_parser import BaseParser, DataBlob, BaseParserSpec
from eidolon_sdk.vector_store.code_ast_parsers.cobol import CobolASTGenerator
from eidolon_sdk.vector_store.code_ast_parsers.javascript import JavaScriptASTGenerator
from eidolon_sdk.vector_store.code_ast_parsers.python import PythonASTGenerator
from eidolon_sdk.vector_store.document import Document
from eidolon_sdk.vector_store.text_splitters import Language

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


class LanguageParserSpec(BaseParserSpec):
    language: Literal["python", "javascript", "cobol"] = "python"
    parser_threshold: int = 0


class LanguageParser(BaseParser, Specable[LanguageParserSpec]):

    def __init__(self, spec: LanguageParserSpec):
        super().__init__(spec)
        self.language = spec.language
        self.parser_threshold = spec.parser_threshold

    def parse(self, blob: DataBlob) -> Iterable[Document]:
        code = blob.as_string()

        language = self.language or (
            LANGUAGE_EXTENSIONS.get(blob.source.rsplit(".", 1)[-1])
            if isinstance(blob.source, str)
            else None
        )

        if language is None:
            yield Document(
                page_content=code,
                metadata={
                    "source": blob.source,
                },
            )
            return

        if self.parser_threshold >= len(code.splitlines()):
            yield Document(
                page_content=code,
                metadata={
                    "source": blob.source,
                    "language": language,
                },
            )
            return

        generator = LANGUAGE_AST_GENERATORS[language](blob.as_string())
        if not generator.is_valid():
            yield Document(
                page_content=code,
                metadata={
                    "source": blob.source,
                },
            )
            return

        for functions_classes in generator.extract_functions_classes():
            yield Document(
                page_content=functions_classes,
                metadata={
                    "source": blob.source,
                    "content_type": "functions_classes",
                    "language": language,
                },
            )
        yield Document(
            page_content=generator.simplify_code(),
            metadata={
                "source": blob.source,
                "content_type": "simplified_code",
                "language": language,
            },
        )
