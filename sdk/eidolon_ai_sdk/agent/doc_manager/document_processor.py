import logging

from pydantic import BaseModel

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import (
    FileInfo,
)
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser, DataBlob
from eidolon_ai_sdk.agent.doc_manager.transformer.document_transformer import DocumentTransformer
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class DocumentProcessorSpec(BaseModel):
    parser: AnnotatedReference[DocumentParser]
    splitter: AnnotatedReference[DocumentTransformer]


class DocumentProcessor(Specable[DocumentProcessorSpec]):
    last_reload = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)
        self.parser = self.spec.parser.instantiate()
        self.splitter = self.spec.splitter.instantiate()
        self.logger = logging.getLogger("eidolon")

    def parse(self, data: bytes, mimetype: str, path: str):
        return self.parser.parse(DataBlob.from_bytes(data=data, mimetype=mimetype, path=path))

    def split(self, docs):
        return self.splitter.transform_documents(docs)

    async def addFile(self, collection_name: str, file_info: FileInfo):
        try:
            parsedDocs = list(self.parser.parse(file_info.data))
            docs = list(self.splitter.transform_documents(parsedDocs))
            await AgentOS.symbolic_memory.insert_one(
                collection_name,
                {
                    "file_path": file_info.path,
                    "data": file_info.metadata,
                    "doc_ids": [doc.id for doc in docs],
                },
            )
            if len(docs) == 0:
                self.logger.warning(f"File contained no text {file_info.path}")
                return
            await AgentOS.similarity_memory.add(collection_name, docs)
            self.logger.info(f"Added file {file_info.path}")
        except Exception:
            self.logger.warning(f"Failed to parse file {file_info.path}", exc_info=True)

    async def removeFile(self, collection_name: str, path: str):
        # get the doc ids for the file
        file_info = await AgentOS.symbolic_memory.find_one(collection_name, {"file_path": path})
        if file_info is not None:
            doc_ids = file_info["doc_ids"]
            await AgentOS.similarity_memory.delete(collection_name, doc_ids)
            await AgentOS.symbolic_memory.delete(collection_name, {"file_path": path})

    async def replaceFile(self, collection_name: str, file_info: FileInfo):
        await self.removeFile(collection_name, file_info.path)
        await self.addFile(collection_name, file_info)
