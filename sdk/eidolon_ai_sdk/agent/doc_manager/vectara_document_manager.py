import base64
import os
from typing import Optional, Iterable
from urllib.parse import urljoin

from httpx import AsyncClient

from eidolon_ai_sdk.agent.doc_manager.document_processor import DocumentProcessor, DocumentProcessorSpec
from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import FileInfo
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser
from eidolon_ai_sdk.agent.doc_manager.transformer.document_transformer import DocumentTransformer
from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.system.reference_model import Reference, AnnotatedReference, Specable


class VectaraDocumentProcessorSpec(DocumentProcessorSpec):
    corpus_key: str
    vectara_url: str = "https://api.vectara.io/"
    parser: AnnotatedReference[DocumentParser]
    splitter: Optional[Reference[DocumentTransformer]] = None


class VectaraDocumentProcessor(Specable[VectaraDocumentProcessorSpec], DocumentProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.spec.parser.instantiate()
        self.splitter = self.spec.splitter.instantiate() if self.spec.splitter else None

    @property
    def _token(self):
        return os.environ["VECTARA_API_KEY"]

    @property
    def _headers(self):
        return {
            'Accept': 'application/json',
            'x-api-key': self._token
        }

    def _url(self, suffix):
        return urljoin(self.spec.vectara_url, suffix)

    def _id(self, path: str):
        return base64.urlsafe_b64encode(path.encode()).decode()

    async def split(self, docs: Iterable[Document]):
        if self.splitter:
            return await super().split(docs)
        else:
            return docs

    async def addFile(self, collection_name: str, file_info: FileInfo):
        parsedDocs = await self.parse(file_info.data)
        docs: Iterable[Document] = await self.split(parsedDocs)

        async with AsyncClient() as client:
            response = await client.post(
                url=self._url(f"/v2/corpora/{self.spec.corpus_key}/documents"),
                headers=self._headers,
                json=dict(
                    id=self._id(file_info.path),
                    type='core',
                    metadata=dict(path=file_info.path, **file_info.metadata.items()),
                    document_parths=[dict(
                        text=doc.text,
                        metadata=doc.metadata,
                        custom_dimensions={},
                    ) for doc in docs]
                ),
            )
            response.raise_for_status()

    async def removeFile(self, collection_name: str, path: str):
        async with AsyncClient() as client:
            response = await client.delete(
                url=self._url(f"/v2/corpora/{self.spec.corpus_key}/documents/{self._id(path)}"),
                headers=self._headers,
            )
            response.raise_for_status()
