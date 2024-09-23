import logging
from typing import Iterable

from opentelemetry import trace
from pydantic import BaseModel

from eidolon_ai_sdk.agent.doc_manager.loaders.base_loader import (
    FileInfo,
)
from eidolon_ai_sdk.agent.doc_manager.parsers.base_parser import DocumentParser, DataBlob
from eidolon_ai_sdk.agent.doc_manager.transformer.document_transformer import DocumentTransformer
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
from eidolon_ai_sdk.util.async_wrapper import make_async

tracer = trace.get_tracer(__name__)
logger = logging.getLogger("eidolon")


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

    @make_async
    def parse(self, data: bytes, mimetype: str, path: str) -> Iterable[Document]:
        return self.parser.parse(DataBlob.from_bytes(data=data, mimetype=mimetype, path=path))

    @make_async
    def split(self, docs) -> Iterable[Document]:
        return self.splitter.transform_documents(docs)

    async def addFile(self, collection_name: str, file_info: FileInfo):
        with tracer.start_as_current_span("add file"):
            try:
                with tracer.start_as_current_span("parsing"):
                    parsedDocs = await make_async(lambda d: list(self.parser.parse(d)))(file_info.data)
                with tracer.start_as_current_span("transforming"):
                    docs = await make_async(lambda pd: list(self.splitter.transform_documents(pd)))(parsedDocs)
                with tracer.start_as_current_span("record symbolic"):
                    await AgentOS.symbolic_memory.insert_one(
                        collection_name,
                        {
                            "file_path": file_info.path,
                            "data": file_info.metadata,
                            "doc_ids": [doc.id for doc in docs],
                        },
                    )
                if len(docs) == 0:
                    logger.debug(f"File contained no text {file_info.path}")
                    return
                with tracer.start_as_current_span("record similarity"):
                    await AgentOS.similarity_memory.add(collection_name, docs)
                logger.debug(f"Added file {file_info.path}")
            except Exception as e:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.warning(f"Failed to parse file {file_info.path}", exc_info=True)
                else:
                    logger.warning(f"Failed to parse file {file_info.path} ({e})")

    async def removeFile(self, collection_name: str, path: str):
        with tracer.start_as_current_span("remove file"):
            file_info = await AgentOS.symbolic_memory.find_one(collection_name, {"file_path": path})
            if file_info is not None:
                doc_ids = file_info["doc_ids"]
                await AgentOS.similarity_memory.delete(collection_name, doc_ids)
                await AgentOS.symbolic_memory.delete(collection_name, {"file_path": path})

    async def replaceFile(self, collection_name: str, file_info: FileInfo):
        with tracer.start_as_current_span("replace file"):
            await self.removeFile(collection_name, file_info.path)
            await self.addFile(collection_name, file_info)
