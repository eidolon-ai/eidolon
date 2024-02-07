from __future__ import annotations

import copy
import logging
from abc import ABC, abstractmethod
from typing import Any, List, Callable, Optional, Iterable
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.memory.document import Document

logger = logging.getLogger("eidolon")


class DocumentTransformer(ABC):
    @abstractmethod
    def transform_documents(self, documents: Iterable[Document], **kwargs: Any) -> Iterable[Document]:
        """Transform a list of documents.

        Args:
            documents: A sequence of Documents to be transformed.

        Returns:
            A list of transformed Documents.
        """


class TextSplitterSpec(BaseModel):
    chunk_size: int = Field(default=4000, description="Maximum size of chunks to return")
    chunk_overlap: int = Field(default=200, description="Overlap in characters between chunks")
    keep_separator: bool = Field(default=False, description="Whether to keep the separator in the chunks")
    strip_whitespace: bool = Field(
        default=True,
        description="If `True`, strips whitespace from the start and end of every document",
    )

    # noinspection PyMethodParameters
    @field_validator("chunk_overlap")
    def validate_chunk_overlap(cls, chunk_overlap: int, info: ValidationInfo) -> None:
        if chunk_overlap > info.data["chunk_size"]:
            raise ValueError(
                f"Got a larger chunk overlap ({chunk_overlap}) than chunk size "
                f"({info.data['chunk_size']}), should be smaller."
            )


class TextSplitter(DocumentTransformer, ABC, Specable[TextSplitterSpec]):
    length_function: Callable[[str], int] = len

    def __init__(self, spec: TextSplitterSpec) -> None:
        super().__init__(spec)
        self._chunk_size = spec.chunk_size
        self._chunk_overlap = spec.chunk_overlap
        self._keep_separator = spec.keep_separator
        self._strip_whitespace = spec.strip_whitespace

    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        """Split text into multiple components."""

    def transform_documents(self, documents: Iterable[Document], **kwargs: Any) -> Iterable[Document]:
        """Transform sequence of documents by splitting them."""
        for doc in documents:
            index = -1
            for chunk in self.split_text(doc.page_content):
                metadata = copy.deepcopy(doc.metadata)
                index = doc.page_content.find(chunk, index + 1)
                metadata["start_index"] = index
                yield Document(id=uuid4().hex, page_content=chunk, metadata=metadata)

    def _join_docs(self, docs: List[str], separator: str) -> Optional[str]:
        text = separator.join(docs)
        if self._strip_whitespace:
            text = text.strip()
        if text == "":
            return None
        else:
            return text

    def _merge_splits(
        self,
        splits: Iterable[str],
        separator: str,
        length_function: Callable[[str], int],
    ) -> List[str]:
        # We now want to combine these smaller pieces into medium size
        # chunks to send to the LLM.
        separator_len = length_function(separator)

        docs = []
        current_doc: List[str] = []
        total = 0
        for d in splits:
            _len = length_function(d)
            if total + _len + (separator_len if len(current_doc) > 0 else 0) > self._chunk_size:
                if total > self._chunk_size:
                    logger.warning(
                        f"Created a chunk of size {total}, " f"which is longer than the specified {self._chunk_size}"
                    )
                if len(current_doc) > 0:
                    doc = self._join_docs(current_doc, separator)
                    if doc is not None:
                        docs.append(doc)
                    # Keep on popping if:
                    # - we have a larger chunk than in the chunk overlap
                    # - or if we still have any chunks and the length is long
                    while total > self._chunk_overlap or (
                        total + _len + (separator_len if len(current_doc) > 0 else 0) > self._chunk_size and total > 0
                    ):
                        total -= length_function(current_doc[0]) + (separator_len if len(current_doc) > 1 else 0)
                        current_doc = current_doc[1:]
            current_doc.append(d)
            total += _len + (separator_len if len(current_doc) > 1 else 0)
        doc = self._join_docs(current_doc, separator)
        if doc is not None:
            docs.append(doc)
        return docs
