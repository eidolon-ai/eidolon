from typing import Any, Iterable

from eidos_sdk.agent.doc_manager.transformer.document_transformer import BaseDocumentTransformer
from eidos_sdk.agent.doc_manager.transformer.text_splitters import Language, RecursiveCharacterTextSplitter, RecursiveCharacterTextSplitterSpec
from eidos_sdk.memory.document import Document


class AutoTransformer(BaseDocumentTransformer):
    def transform_documents(self, documents: Iterable[Document], **kwargs: Any) -> Iterable[Document]:
        for document in documents:
            if document.metadata["mime_type"] == "application/pdf" or \
                    document.metadata["mime_type"] == "application/msword" or \
                    document.metadata["mime_type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or \
                    document.metadata["mime_type"] == "application/json":
                yield document
            else:
                progLang = Language.from_mimetype(document.metadata["mime_type"])
                # if progLang is none then we will use the defaults
                if progLang is None:
                    spec = RecursiveCharacterTextSplitterSpec()
                else:
                    spec = RecursiveCharacterTextSplitterSpec(separators=RecursiveCharacterTextSplitter.get_separators_for_language(Language("text")))
                yield RecursiveCharacterTextSplitter(spec).transform_documents([document])
