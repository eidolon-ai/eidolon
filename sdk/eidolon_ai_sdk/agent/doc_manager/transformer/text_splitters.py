from __future__ import annotations

import pathlib
import re
from dataclasses import dataclass
from enum import Enum
from io import BytesIO, StringIO
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
    cast,
    Iterable,
)

import requests
from pydantic import Field

from eidolon_ai_sdk.agent.doc_manager.transformer.document_transformer import TextSplitterSpec, TextSplitter
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.memory.document import Document

TS = TypeVar("TS", bound="TextSplitter")


def _make_spacy_pipeline_for_splitting(pipeline: str, *, max_length: int = 1_000_000) -> Any:  # avoid importing spacy
    try:
        import spacy
    except ImportError:
        raise ImportError("Spacy is not installed, please install it with `pip install spacy`.")
    if pipeline == "sentencizer":
        from spacy.lang.en import English

        sentencizer = English()
        sentencizer.add_pipe("sentencizer")
    else:
        sentencizer = spacy.load(pipeline, exclude=["ner", "tagger"])
        sentencizer.max_length = max_length
    return sentencizer


def _split_text_with_regex(text: str, separator: str, keep_separator: bool) -> List[str]:
    # Now that we have the separator, split the text
    if separator:
        if keep_separator:
            # The parentheses in the pattern keep the delimiters in the result.
            _splits = re.split(f"({separator})", text)
            splits = [_splits[i] + _splits[i + 1] for i in range(1, len(_splits), 2)]
            if len(_splits) % 2 == 0:
                splits += _splits[-1:]
            splits = [_splits[0]] + splits
        else:
            splits = re.split(separator, text)
    else:
        splits = list(text)
    return [s for s in splits if s != ""]


class CharacterTextSplitterSpec(TextSplitterSpec):
    separator: str = Field(default="\n\n", description="Separator to split on")
    is_separator_regex: bool = Field(default=False, description="Whether the separator is a regex")


class CharacterTextSplitter(TextSplitter, Specable[CharacterTextSplitterSpec]):
    """Splitting text that looks at characters."""

    def __init__(self, spec: CharacterTextSplitterSpec, **kwargs: Any) -> None:
        """Create a new TextSplitter."""
        super().__init__(**kwargs)
        self._separator = spec.separator
        self._is_separator_regex = spec.is_separator_regex

    def split_text(self, text: str) -> Iterable[str]:
        """Split incoming text and return chunks."""
        # First we naively split the large input into a bunch of smaller ones.
        separator = self._separator if self._is_separator_regex else re.escape(self._separator)
        splits = _split_text_with_regex(text, separator, self._keep_separator)
        _separator = "" if self._keep_separator else self._separator
        return self._merge_splits(splits, _separator, len)


class LineType(TypedDict):
    """Line type as typed dict."""

    metadata: Dict[str, str]
    content: str


class HeaderType(TypedDict):
    """Header type as typed dict."""

    level: int
    name: str
    data: str


def aggregate_lines_to_chunks(lines: List[LineType]) -> List[Document]:
    """Combine lines with common metadata into chunks
    Args:
        lines: Line of text / associated header metadata
    """
    aggregated_chunks: List[LineType] = []

    for line in lines:
        if aggregated_chunks and aggregated_chunks[-1]["metadata"] == line["metadata"]:
            # If the last line in the aggregated list
            # has the same metadata as the current line,
            # append the current content to the last lines's content
            aggregated_chunks[-1]["content"] += "  \n" + line["content"]
        else:
            # Otherwise, append the current line to the aggregated list
            aggregated_chunks.append(line)

    return [Document(page_content=chunk["content"], metadata=chunk["metadata"]) for chunk in aggregated_chunks]


class MarkdownHeaderTextSplitterSpec(TextSplitterSpec):
    headers_to_split_on: List[Tuple[str, str]] = Field(
        description="Headers we want to track, e.g., #, ##, etc.",
    )
    return_each_line: bool = Field(
        default=False,
        description="Return each line w/ associated headers",
    )


class MarkdownHeaderTextSplitter(TextSplitter, Specable[MarkdownHeaderTextSplitterSpec]):
    """Splitting markdown files based on specified headers."""

    def __init__(self, spec: MarkdownHeaderTextSplitterSpec, **kwargs: Any):
        """Create a new MarkdownHeaderTextSplitter.

        Args:
            headers_to_split_on: Headers we want to track
            return_each_line: Return each line w/ associated headers
        """
        super().__init__(**kwargs)
        # Output line-by-line or aggregated into chunks w/ common headers
        self.return_each_line = spec.return_each_line
        # Given the headers we want to split on,
        # (e.g., "#, ##, etc") order by length
        self.headers_to_split_on = sorted(spec.headers_to_split_on, key=lambda split: len(split[0]), reverse=True)

    def split_text(self, text: str) -> List[Document]:
        """Split markdown file
        Args:
            text: Markdown file"""

        # Split the input text by newline character ("\n").
        lines = text.split("\n")
        # Final output
        lines_with_metadata: List[LineType] = []
        # Content and metadata of the chunk currently being processed
        current_content: List[str] = []
        current_metadata: Dict[str, str] = {}
        # Keep track of the nested header structure
        # header_stack: List[Dict[str, Union[int, str]]] = []
        header_stack: List[HeaderType] = []
        initial_metadata: Dict[str, str] = {}

        in_code_block = False
        opening_fence = ""

        for line in lines:
            stripped_line = line.strip()

            if not in_code_block:
                # Exclude inline code spans
                if stripped_line.startswith("```") and stripped_line.count("```") == 1:
                    in_code_block = True
                    opening_fence = "```"
                elif stripped_line.startswith("~~~"):
                    in_code_block = True
                    opening_fence = "~~~"
            else:
                if stripped_line.startswith(opening_fence):
                    in_code_block = False
                    opening_fence = ""

            if in_code_block:
                current_content.append(stripped_line)
                continue

            # Check each line against each of the header types (e.g., #, ##)
            for sep, name in self.headers_to_split_on:
                # Check if line starts with a header that we intend to split on
                if stripped_line.startswith(sep) and (
                    # Header with no text OR header is followed by space
                    # Both are valid conditions that sep is being used a header
                    len(stripped_line) == len(sep) or stripped_line[len(sep)] == " "
                ):
                    # Ensure we are tracking the header as metadata
                    if name is not None:
                        # Get the current header level
                        current_header_level = sep.count("#")

                        # Pop out headers of lower or same level from the stack
                        while header_stack and header_stack[-1]["level"] >= current_header_level:
                            # We have encountered a new header
                            # at the same or higher level
                            popped_header = header_stack.pop()
                            # Clear the metadata for the
                            # popped header in initial_metadata
                            if popped_header["name"] in initial_metadata:
                                initial_metadata.pop(popped_header["name"])

                        # Push the current header to the stack
                        header: HeaderType = {
                            "level": current_header_level,
                            "name": name,
                            "data": stripped_line[len(sep) :].strip(),
                        }
                        header_stack.append(header)
                        # Update initial_metadata with the current header
                        initial_metadata[name] = header["data"]

                    # Add the previous line to the lines_with_metadata
                    # only if current_content is not empty
                    if current_content:
                        lines_with_metadata.append(
                            {
                                "content": "\n".join(current_content),
                                "metadata": current_metadata.copy(),
                            }
                        )
                        current_content.clear()

                    break
            else:
                if stripped_line:
                    current_content.append(stripped_line)
                elif current_content:
                    lines_with_metadata.append(
                        {
                            "content": "\n".join(current_content),
                            "metadata": current_metadata.copy(),
                        }
                    )
                    current_content.clear()

            current_metadata = initial_metadata.copy()

        if current_content:
            lines_with_metadata.append({"content": "\n".join(current_content), "metadata": current_metadata})

        # lines_with_metadata has each line with associated header metadata
        # aggregate these into chunks based on common metadata
        if not self.return_each_line:
            return aggregate_lines_to_chunks(lines_with_metadata)
        else:
            return [Document(page_content=chunk["content"], metadata=chunk["metadata"]) for chunk in lines_with_metadata]


class ElementType(TypedDict):
    """Element type as typed dict."""

    url: str
    xpath: str
    content: str
    metadata: Dict[str, str]


class HTMLHeaderTextSplitterSpec(TextSplitterSpec):
    headers_to_split_on: List[Tuple[str, str]] = Field(
        description="Headers we want to track, e.g., h1, h2, etc.",
    )
    return_each_element: bool = Field(
        default=False,
        description="Return each element w/ associated headers",
    )


class HTMLHeaderTextSplitter(TextSplitter, Specable[HTMLHeaderTextSplitterSpec]):
    """
    Splitting HTML files based on specified headers.
    Requires lxml package.
    """

    def __init__(self, spec: HTMLHeaderTextSplitterSpec, **kwargs: Any):
        """Create a new HTMLHeaderTextSplitter.

        Args:
            headers_to_split_on: list of tuples of headers we want to track mapped to
                (arbitrary) keys for metadata. Allowed header values: h1, h2, h3, h4,
                h5, h6 e.g. [("h1", "Header 1"), ("h2", "Header 2)].
            return_each_element: Return each element w/ associated headers.
        """
        # Output element-by-element or aggregated into chunks w/ common headers
        super().__init__(**kwargs)
        self.return_each_element = spec.return_each_element
        self.headers_to_split_on = sorted(spec.headers_to_split_on)

    def split_text_from_url(self, url: str) -> List[Document]:
        """Split HTML from web URL

        Args:
            url: web URL
        """
        r = requests.get(url)
        return self.split_text_from_file(BytesIO(r.content))

    def split_text(self, text: str) -> List[Document]:
        """Split HTML text string

        Args:
            text: HTML text
        """
        return self.split_text_from_file(StringIO(text))

    def split_text_from_file(self, file: Any) -> List[Document]:
        """Split HTML file

        Args:
            file: HTML file
        """
        try:
            from lxml import etree
        except ImportError as e:
            raise ImportError("Unable to import lxml, please install with `pip install lxml`.") from e
        # use lxml library to parse html document and return xml ElementTree
        parser = etree.HTMLParser()
        tree = etree.parse(file, parser)

        # document transformation for "structure-aware" chunking is handled with xsl.
        # see comments in html_chunks_with_headers.xslt for more detailed information.
        xslt_path = pathlib.Path(__file__).parent / "document_transformers/xsl/html_chunks_with_headers.xslt"
        xslt_tree = etree.parse(xslt_path)
        transform = etree.XSLT(xslt_tree)
        result = transform(tree)
        result_dom = etree.fromstring(str(result))

        # create filter and mapping for header metadata
        header_filter = [header[0] for header in self.headers_to_split_on]
        header_mapping = dict(self.headers_to_split_on)

        # map xhtml namespace prefix
        ns_map = {"h": "http://www.w3.org/1999/xhtml"}

        # build list of elements from DOM
        elements = []
        for element in result_dom.findall("*//*", ns_map):
            if element.findall("*[@class='headers']") or element.findall("*[@class='chunk']"):
                elements.append(
                    ElementType(
                        url=file,
                        xpath="".join([node.text for node in element.findall("*[@class='xpath']", ns_map)]),
                        content="".join([node.text for node in element.findall("*[@class='chunk']", ns_map)]),
                        metadata={
                            # Add text of specified headers to metadata using header
                            # mapping.
                            header_mapping[node.tag]: node.text
                            for node in filter(
                                lambda x: x.tag in header_filter,
                                element.findall("*[@class='headers']/*", ns_map),
                            )
                        },
                    )
                )

        if not self.return_each_element:
            return aggregate_lines_to_chunks(elements)
        else:
            return [Document(page_content=chunk["content"], metadata=chunk["metadata"]) for chunk in elements]


@dataclass(frozen=True, kw_only=True, slots=True)
class Tokenizer:
    """Tokenizer data class."""

    chunk_overlap: int
    """Overlap in tokens between chunks"""
    tokens_per_chunk: int
    """Maximum number of tokens per chunk"""
    decode: Callable[[List[int]], str]
    """ Function to decode a list of token ids to a string"""
    encode: Callable[[str], List[int]]
    """ Function to encode a string to a list of token ids"""


def split_text_on_tokens(*, text: str, tokenizer: Tokenizer) -> List[str]:
    """Split incoming text and return chunks using tokenizer."""
    splits: List[str] = []
    input_ids = tokenizer.encode(text)
    start_idx = 0
    cur_idx = min(start_idx + tokenizer.tokens_per_chunk, len(input_ids))
    chunk_ids = input_ids[start_idx:cur_idx]
    while start_idx < len(input_ids):
        splits.append(tokenizer.decode(chunk_ids))
        start_idx += tokenizer.tokens_per_chunk - tokenizer.chunk_overlap
        cur_idx = min(start_idx + tokenizer.tokens_per_chunk, len(input_ids))
        chunk_ids = input_ids[start_idx:cur_idx]
    return splits


class TokenTextSplitterSpec(TextSplitterSpec):
    encoding_name: str = Field(default="gpt2", description="Encoding name")
    model: Optional[str] = Field(default=None, description="Model name")
    allowed_special: Union[Literal["all"], List[str]] = Field(default=set(), description="Allowed special tokens")
    disallowed_special: Union[Literal["all"], List[str]] = Field(default="all", description="Disallowed special tokens")


class TokenTextSplitter(TextSplitter, Specable[TokenTextSplitterSpec]):
    """Splitting text to tokens using model tokenizer."""

    def __init__(
        self,
        spec: TokenTextSplitterSpec,
        **kwargs: Any,
    ) -> None:
        """Create a new TextSplitter."""
        super().__init__(**kwargs)
        try:
            import tiktoken
        except ImportError:
            raise ImportError(
                "Could not import tiktoken python package. "
                "This is needed in order to for TokenTextSplitter. "
                "Please install it with `pip install tiktoken`."
            )

        if spec.model is not None:
            enc = tiktoken.encoding_for_model(spec.model)
        else:
            enc = tiktoken.get_encoding(spec.encoding_name)
        self._tokenizer = enc
        self._allowed_special = spec.allowed_special
        self._disallowed_special = spec.disallowed_special

    def split_text(self, text: str) -> List[str]:
        def _encode(_text: str) -> List[int]:
            return self._tokenizer.encode(
                _text,
                allowed_special=self._allowed_special,
                disallowed_special=self._disallowed_special,
            )

        tokenizer = Tokenizer(
            chunk_overlap=self._chunk_overlap,
            tokens_per_chunk=self._chunk_size,
            decode=self._tokenizer.decode,
            encode=_encode,
        )

        return split_text_on_tokens(text=text, tokenizer=tokenizer)


class SentenceTransformersTokenTextSplitterSpec(TextSplitterSpec):
    model: str = Field(
        default="sentence-transformers/all-mpnet-base-v2",
        description="Model name",
    )
    tokens_per_chunk: Optional[int] = Field(
        default=None,
        description="Number of tokens per chunk",
    )
    chunk_overlap: int = 50


class SentenceTransformersTokenTextSplitter(TextSplitter, Specable[SentenceTransformersTokenTextSplitterSpec]):
    """Splitting text to tokens using sentence model tokenizer."""

    def __init__(
        self,
        spec: SentenceTransformersTokenTextSplitterSpec,
        **kwargs: Any,
    ) -> None:
        """Create a new TextSplitter."""
        super().__init__(**kwargs)

        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "Could not import sentence_transformer python package. "
                "This is needed in order to for SentenceTransformersTokenTextSplitter. "
                "Please install it with `pip install sentence-transformers`."
            )

        self.model_name = spec.model
        self._model = SentenceTransformer(self.model_name)
        self.tokenizer = self._model.tokenizer
        self._initialize_chunk_configuration(tokens_per_chunk=spec.tokens_per_chunk)

    def _initialize_chunk_configuration(self, *, tokens_per_chunk: Optional[int]) -> None:
        self.maximum_tokens_per_chunk = cast(int, self._model.max_seq_length)

        if tokens_per_chunk is None:
            self.tokens_per_chunk = self.maximum_tokens_per_chunk
        else:
            self.tokens_per_chunk = tokens_per_chunk

        if self.tokens_per_chunk > self.maximum_tokens_per_chunk:
            raise ValueError(
                f"The token limit of the models '{self.model_name}'"
                f" is: {self.maximum_tokens_per_chunk}."
                f" Argument tokens_per_chunk={self.tokens_per_chunk}"
                f" > maximum token limit."
            )

    def split_text(self, text: str) -> List[str]:
        def encode_strip_start_and_stop_token_ids(s_text: str) -> List[int]:
            return self._encode(s_text)[1:-1]

        tokenizer = Tokenizer(
            chunk_overlap=self._chunk_overlap,
            tokens_per_chunk=self.tokens_per_chunk,
            decode=self.tokenizer.decode,
            encode=encode_strip_start_and_stop_token_ids,
        )

        return split_text_on_tokens(text=text, tokenizer=tokenizer)

    def count_tokens(self, *, text: str) -> int:
        return len(self._encode(text))

    _max_length_equal_32_bit_integer: int = 2**32

    def _encode(self, text: str) -> List[int]:
        token_ids_with_start_and_end_token_ids = self.tokenizer.encode(
            text,
            max_length=self._max_length_equal_32_bit_integer,
            truncation="do_not_truncate",
        )
        return token_ids_with_start_and_end_token_ids


class Language(str, Enum):
    """Enum of the programming languages."""

    CPP = "cpp"
    GO = "go"
    JAVA = "java"
    KOTLIN = "kotlin"
    JS = "js"
    TS = "ts"
    PHP = "php"
    PROTO = "proto"
    PYTHON = "python"
    RST = "rst"
    RUBY = "ruby"
    RUST = "rust"
    SCALA = "scala"
    SWIFT = "swift"
    MARKDOWN = "markdown"
    JSON = "json"
    LATEX = "latex"
    HTML = "html"
    SOL = "sol"
    CSHARP = "csharp"
    COBOL = "cobol"

    @classmethod
    def from_mimetype(cls, mimetype: str) -> Optional[Language]:
        if mimetype == "text/x-python" or mimetype == "text/x-python-code":
            return cls.PYTHON
        elif mimetype == "application/javascript":
            return cls.JS
        elif mimetype == "text/x-cobol":
            return cls.COBOL
        elif (
            mimetype == "text/x-c++src"
            or mimetype == "text/x-c++hdr"
            or mimetype == "text/x-csrc"
            or mimetype == "text/x-chdr"
        ):
            return cls.CPP
        elif mimetype == "text/x-csharp":
            return cls.CSHARP
        elif mimetype == "text/x-go":
            return cls.GO
        elif mimetype == "text/x-java-source":
            return cls.JAVA
        elif mimetype == "text/x-kotlin":
            return cls.KOTLIN
        elif mimetype == "text/x-php":
            return cls.PHP
        elif mimetype == "text/x-protobuf":
            return cls.PROTO
        elif mimetype == "text/x-ruby":
            return cls.RUBY
        elif mimetype == "text/x-rust":
            return cls.RUST
        elif mimetype == "text/x-scala":
            return cls.SCALA
        elif mimetype == "text/x-swift":
            return cls.SWIFT
        elif mimetype == "text/x-markdown":
            return cls.MARKDOWN
        elif mimetype == "text/x-latex":
            return cls.LATEX
        elif mimetype == "text/html":
            return cls.HTML
        elif mimetype == "text/x-solidity":
            return cls.SOL
        elif mimetype == "application/json":
            return cls.JSON
        else:
            return None


class RecursiveCharacterTextSplitterSpec(TextSplitterSpec):
    separators: Optional[List[str]] = Field(
        default=None,
        description="Separators to split on",
    )
    is_separator_regex: bool = Field(
        default=False,
        description="Whether the separator is a regex",
    )


class RecursiveCharacterTextSplitter(TextSplitter, Specable[RecursiveCharacterTextSplitterSpec]):
    """Splitting text by recursively look at characters.

    Recursively tries to split by different characters to find one
    that works.
    """

    def __init__(
        self,
        spec: RecursiveCharacterTextSplitterSpec,
        **kwargs: Any,
    ) -> None:
        """Create a new TextSplitter."""
        super().__init__(spec, **kwargs)
        self._separators = spec.separators or ["\n\n", "\n", " ", ""]
        self._is_separator_regex = spec.is_separator_regex
        self._length_function = len

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        """Split incoming text and return chunks."""
        final_chunks = []
        # Get appropriate separator to use
        separator = separators[-1]
        new_separators = []
        for i, _s in enumerate(separators):
            _separator = _s if self._is_separator_regex else re.escape(_s)
            if _s == "":
                separator = _s
                break
            if re.search(_separator, text):
                separator = _s
                new_separators = separators[i + 1 :]
                break

        _separator = separator if self._is_separator_regex else re.escape(separator)
        splits = _split_text_with_regex(text, _separator, self._keep_separator)

        # Now go merging things, recursively splitting longer texts.
        _good_splits = []
        _separator = "" if self._keep_separator else separator
        for s in splits:
            if self._length_function(s) < self._chunk_size:
                _good_splits.append(s)
            else:
                if _good_splits:
                    merged_text = self._merge_splits(_good_splits, _separator, self._length_function)
                    final_chunks.extend(merged_text)
                    _good_splits = []
                if not new_separators:
                    final_chunks.append(s)
                else:
                    other_info = self._split_text(s, new_separators)
                    final_chunks.extend(other_info)
        if _good_splits:
            merged_text = self._merge_splits(_good_splits, _separator, self._length_function)
            final_chunks.extend(merged_text)
        return final_chunks

    def split_text(self, text: str) -> List[str]:
        return self._split_text(text, self._separators)

    @staticmethod
    def get_separators_for_language(language: Language) -> List[str]:
        if language == Language.CPP:
            return [
                # Split along class definitions
                "\nclass ",
                # Split along function definitions
                "\nvoid ",
                "\nint ",
                "\nfloat ",
                "\ndouble ",
                # Split along control flow statements
                "\nif ",
                "\nfor ",
                "\nwhile ",
                "\nswitch ",
                "\ncase ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.GO:
            return [
                # Split along function definitions
                "\nfunc ",
                "\nvar ",
                "\nconst ",
                "\ntype ",
                # Split along control flow statements
                "\nif ",
                "\nfor ",
                "\nswitch ",
                "\ncase ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.JAVA:
            return [
                # Split along class definitions
                "\nclass ",
                # Split along method definitions
                "\npublic ",
                "\nprotected ",
                "\nprivate ",
                "\nstatic ",
                # Split along control flow statements
                "\nif ",
                "\nfor ",
                "\nwhile ",
                "\nswitch ",
                "\ncase ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.KOTLIN:
            return [
                # Split along class definitions
                "\nclass ",
                # Split along method definitions
                "\npublic ",
                "\nprotected ",
                "\nprivate ",
                "\ninternal ",
                "\ncompanion ",
                "\nfun ",
                "\nval ",
                "\nvar ",
                # Split along control flow statements
                "\nif ",
                "\nfor ",
                "\nwhile ",
                "\nwhen ",
                "\ncase ",
                "\nelse ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.JS:
            return [
                # Split along function definitions
                "\nfunction ",
                "\nconst ",
                "\nlet ",
                "\nvar ",
                "\nclass ",
                # Split along control flow statements
                "\nif ",
                "\nfor ",
                "\nwhile ",
                "\nswitch ",
                "\ncase ",
                "\ndefault ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.TS:
            return [
                "\nenum ",
                "\ninterface ",
                "\nnamespace ",
                "\ntype ",
                # Split along class definitions
                "\nclass ",
                # Split along function definitions
                "\nfunction ",
                "\nconst ",
                "\nlet ",
                "\nvar ",
                # Split along control flow statements
                "\nif ",
                "\nfor ",
                "\nwhile ",
                "\nswitch ",
                "\ncase ",
                "\ndefault ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.PHP:
            return [
                # Split along function definitions
                "\nfunction ",
                # Split along class definitions
                "\nclass ",
                # Split along control flow statements
                "\nif ",
                "\nforeach ",
                "\nwhile ",
                "\ndo ",
                "\nswitch ",
                "\ncase ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.PROTO:
            return [
                # Split along message definitions
                "\nmessage ",
                # Split along service definitions
                "\nservice ",
                # Split along enum definitions
                "\nenum ",
                # Split along option definitions
                "\noption ",
                # Split along import statements
                "\nimport ",
                # Split along syntax declarations
                "\nsyntax ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.PYTHON:
            return [
                # First, try to split along class definitions
                "\nclass ",
                "\ndef ",
                "\n\tdef ",
                # Now split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.RST:
            return [
                # Split along section titles
                "\n=+\n",
                "\n-+\n",
                "\n\\*+\n",
                # Split along directive markers
                "\n\n.. *\n\n",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.RUBY:
            return [
                # Split along method definitions
                "\ndef ",
                "\nclass ",
                # Split along control flow statements
                "\nif ",
                "\nunless ",
                "\nwhile ",
                "\nfor ",
                "\ndo ",
                "\nbegin ",
                "\nrescue ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.RUST:
            return [
                # Split along function definitions
                "\nfn ",
                "\nconst ",
                "\nlet ",
                # Split along control flow statements
                "\nif ",
                "\nwhile ",
                "\nfor ",
                "\nloop ",
                "\nmatch ",
                "\nconst ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.SCALA:
            return [
                # Split along class definitions
                "\nclass ",
                "\nobject ",
                # Split along method definitions
                "\ndef ",
                "\nval ",
                "\nvar ",
                # Split along control flow statements
                "\nif ",
                "\nfor ",
                "\nwhile ",
                "\nmatch ",
                "\ncase ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.SWIFT:
            return [
                # Split along function definitions
                "\nfunc ",
                # Split along class definitions
                "\nclass ",
                "\nstruct ",
                "\nenum ",
                # Split along control flow statements
                "\nif ",
                "\nfor ",
                "\nwhile ",
                "\ndo ",
                "\nswitch ",
                "\ncase ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.MARKDOWN:
            return [
                # First, try to split along Markdown headings (starting with level 2)
                "\n#{1,6} ",
                # Note the alternative syntax for headings (below) is not handled here
                # Heading level 2
                # ---------------
                # End of code block
                "```\n",
                # Horizontal lines
                "\n\\*\\*\\*+\n",
                "\n---+\n",
                "\n___+\n",
                # Note that this splitter doesn't handle horizontal lines defined
                # by *three or more* of ***, ---, or ___, but this is not handled
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.JSON:
            return [
                # First, try to split along newlines to handle json-nl
                "\n\n",
                "\n",
                # then by commas
                ",",
                # then by spaces, which really, really sucks
                " " "",
            ]
        elif language == Language.LATEX:
            return [
                # First, try to split along Latex sections
                "\n\\\\chapter{",
                "\n\\\\section{",
                "\n\\\\subsection{",
                "\n\\\\subsubsection{",
                # Now split by environments
                "\n\\\\begin{enumerate}",
                "\n\\\\begin{itemize}",
                "\n\\\\begin{description}",
                "\n\\\\begin{list}",
                "\n\\\\begin{quote}",
                "\n\\\\begin{quotation}",
                "\n\\\\begin{verse}",
                "\n\\\\begin{verbatim}",
                # Now split by math environments
                "\n\\\begin{align}",
                "$$",
                "$",
                # Now split by the normal type of lines
                " ",
                "",
            ]
        elif language == Language.HTML:
            return [
                # First, try to split along HTML tags
                "<body",
                "<div",
                "<p",
                "<br",
                "<li",
                "<h1",
                "<h2",
                "<h3",
                "<h4",
                "<h5",
                "<h6",
                "<span",
                "<table",
                "<tr",
                "<td",
                "<th",
                "<ul",
                "<ol",
                "<header",
                "<footer",
                "<nav",
                # Head
                "<head",
                "<style",
                "<script",
                "<meta",
                "<title",
                "",
            ]
        elif language == Language.CSHARP:
            return [
                "\ninterface ",
                "\nenum ",
                "\nimplements ",
                "\ndelegate ",
                "\nevent ",
                # Split along class definitions
                "\nclass ",
                "\nabstract ",
                # Split along method definitions
                "\npublic ",
                "\nprotected ",
                "\nprivate ",
                "\nstatic ",
                "\nreturn ",
                # Split along control flow statements
                "\nif ",
                "\ncontinue ",
                "\nfor ",
                "\nforeach ",
                "\nwhile ",
                "\nswitch ",
                "\nbreak ",
                "\ncase ",
                "\nelse ",
                # Split by exceptions
                "\ntry ",
                "\nthrow ",
                "\nfinally ",
                "\ncatch ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.SOL:
            return [
                # Split along compiler information definitions
                "\npragma ",
                "\nusing ",
                # Split along contract definitions
                "\ncontract ",
                "\ninterface ",
                "\nlibrary ",
                # Split along method definitions
                "\nconstructor ",
                "\ntype ",
                "\nfunction ",
                "\nevent ",
                "\nmodifier ",
                "\nerror ",
                "\nstruct ",
                "\nenum ",
                # Split along control flow statements
                "\nif ",
                "\nfor ",
                "\nwhile ",
                "\ndo while ",
                "\nassembly ",
                # Split by the normal type of lines
                "\n\n",
                "\n",
                " ",
                "",
            ]
        elif language == Language.COBOL:
            return [
                # Split along divisions
                "\nIDENTIFICATION DIVISION.",
                "\nENVIRONMENT DIVISION.",
                "\nDATA DIVISION.",
                "\nPROCEDURE DIVISION.",
                # Split along sections within DATA DIVISION
                "\nWORKING-STORAGE SECTION.",
                "\nLINKAGE SECTION.",
                "\nFILE SECTION.",
                # Split along sections within PROCEDURE DIVISION
                "\nINPUT-OUTPUT SECTION.",
                # Split along paragraphs and common statements
                "\nOPEN ",
                "\nCLOSE ",
                "\nREAD ",
                "\nWRITE ",
                "\nIF ",
                "\nELSE ",
                "\nMOVE ",
                "\nPERFORM ",
                "\nUNTIL ",
                "\nVARYING ",
                "\nACCEPT ",
                "\nDISPLAY ",
                "\nSTOP RUN.",
                # Split by the normal type of lines
                "\n",
                " ",
                "",
            ]

        else:
            raise ValueError(f"Language {language} is not supported! " f"Please choose from {list(Language)}")


class NLTKTextSplitterSpec(TextSplitterSpec):
    separator: str = Field(
        default="\n\n",
        description="Separator to split on",
    )
    language: str = Field(
        default="english",
        description="Language to use for tokenization",
    )


class NLTKTextSplitter(TextSplitter, Specable[NLTKTextSplitterSpec]):
    """Splitting text using NLTK package."""

    def __init__(self, spec: NLTKTextSplitterSpec, **kwargs: Any) -> None:
        """Initialize the NLTK splitter."""
        super().__init__(**kwargs)
        try:
            from nltk.tokenize import sent_tokenize

            self._tokenizer = sent_tokenize
        except ImportError:
            raise ImportError("NLTK is not installed, please install it with `pip install nltk`.")
        self._separator = spec.separator
        self._language = spec.language

    def split_text(self, text: str) -> List[str]:
        """Split incoming text and return chunks."""
        # First we naively split the large input into a bunch of smaller ones.
        splits = self._tokenizer(text, language=self._language)
        return self._merge_splits(splits, self._separator, len)


class SpacyTextSplitterSpec(TextSplitterSpec):
    separator: str = Field(
        default="\n\n",
        description="Separator to split on",
    )
    pipeline: str = Field(
        default="en_core_web_sm",
        description="Spacy pipeline to use",
    )
    max_length: int = Field(
        default=1_000_000,
        description="Maximum length of characters to process",
    )


class SpacyTextSplitter(TextSplitter, Specable[SpacyTextSplitterSpec]):
    """Splitting text using Spacy package.


    Per default, Spacy's `en_core_web_sm` model is used and
    its default max_length is 1000000 (it is the length of maximum character
    this model takes which can be increased for large files). For a faster, but
    potentially less accurate splitting, you can use `pipeline='sentencizer'`.
    """

    def __init__(
        self,
        spec: SpacyTextSplitterSpec,
        **kwargs: Any,
    ) -> None:
        """Initialize the spacy text splitter."""
        super().__init__(**kwargs)
        self._tokenizer = _make_spacy_pipeline_for_splitting(spec.pipeline, max_length=spec.max_length)
        self._separator = spec.separator

    def split_text(self, text: str) -> List[str]:
        """Split incoming text and return chunks."""
        splits = (s.text for s in self._tokenizer(text).sents)
        return self._merge_splits(splits, self._separator, len)


# For backwards compatibility
class PythonCodeTextSplitter(RecursiveCharacterTextSplitter):
    """Attempts to split the text along Python syntax."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a PythonCodeTextSplitter."""
        super().__init__(**kwargs)
        self._separators = self.get_separators_for_language(Language.PYTHON)


class MarkdownTextSplitter(RecursiveCharacterTextSplitter):
    """Attempts to split the text along Markdown-formatted headings."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a MarkdownTextSplitter."""
        super().__init__(**kwargs)
        self._separators = self.get_separators_for_language(Language.MARKDOWN)


class LatexTextSplitter(RecursiveCharacterTextSplitter):
    """Attempts to split the text along Latex-formatted layout elements."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a LatexTextSplitter."""
        super().__init__(**kwargs)
        self._separators = self.get_separators_for_language(Language.LATEX)
