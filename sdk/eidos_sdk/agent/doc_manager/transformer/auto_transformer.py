import json
from typing import Any, Iterable

from eidos_sdk.agent.doc_manager.transformer.document_transformer import BaseDocumentTransformer
from eidos_sdk.agent.doc_manager.transformer.text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
    RecursiveCharacterTextSplitterSpec,
)
from eidos_sdk.memory.document import Document


def is_json_nl(text: str) -> bool:
    endOfLine = text.find("\n")
    if endOfLine == -1:
        return False
    elif endOfLine == 0 or endOfLine > 7000:
        return False
    else:
        try:
            json.loads(text[:endOfLine])
            return True
        except json.JSONDecodeError:
            return False


class AutoTransformer(BaseDocumentTransformer):
    def transform_documents(self, documents: Iterable[Document], **kwargs: Any) -> Iterable[Document]:
        for document in documents:
            progLang = Language.from_mimetype(document.metadata["mime_type"])
            # if progLang is none then we will use the defaults
            if progLang is None:
                spec = RecursiveCharacterTextSplitterSpec()
            else:
                spec = RecursiveCharacterTextSplitterSpec(
                    separators=RecursiveCharacterTextSplitter.get_separators_for_language(progLang)
                )
            yield from RecursiveCharacterTextSplitter(spec).transform_documents([document])
