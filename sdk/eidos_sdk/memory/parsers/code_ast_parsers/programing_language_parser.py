from typing import Dict, Any, Literal, Sequence

from eidos_sdk.system.reference_model import Specable
from eidos_sdk.memory.parsers.base_parser import BaseParser, DataBlob, BaseParserSpec
from eidos_sdk.memory.parsers.code_ast_parsers.cobol import CobolASTGenerator
from eidos_sdk.memory.parsers.code_ast_parsers.javascript import JavaScriptASTGenerator
from eidos_sdk.memory.parsers.code_ast_parsers.python import PythonASTGenerator
from eidos_sdk.memory.document import Document
from eidos_sdk.memory.transformer.text_splitters import Language

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

    def parse(self, blob: DataBlob) -> Sequence[Document]:
        code = blob.as_string()

        language = self.language or (
            LANGUAGE_EXTENSIONS.get(blob.path.rsplit(".", 1)[-1]) if isinstance(blob.path, str) else None
        )

        if language is None:
            yield Document(
                page_content=code,
                metadata={
                    "file_path": blob.path,
                },
            )
            return

        if self.parser_threshold >= len(code.splitlines()):
            yield Document(
                page_content=code,
                metadata={
                    "file_path": blob.path,
                    "language": language,
                },
            )
            return

        generator = LANGUAGE_AST_GENERATORS[language](blob.as_string())
        if not generator.is_valid():
            yield Document(
                page_content=code,
                metadata={
                    "file_path": blob.path,
                },
            )
            return

        for functions_classes in generator.extract_functions_classes():
            yield Document(
                page_content=functions_classes,
                metadata={
                    "file_path": blob.path,
                    "content_type": "functions_classes",
                    "language": language,
                },
            )
        yield Document(
            page_content=generator.simplify_code(),
            metadata={
                "file_path": blob.path,
                "content_type": "simplified_code",
                "language": language,
            },
        )
