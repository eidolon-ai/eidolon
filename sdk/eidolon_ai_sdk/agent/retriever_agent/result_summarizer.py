from typing import AsyncIterable

from pydantic import BaseModel

from eidolon_ai_sdk.memory.document import Document
from eidolon_ai_sdk.system.specable import Specable


class DocSummary(BaseModel):
    id: str
    file_name: str
    file_path: str
    text: str


class ResultSummarizerSpec(BaseModel):
    pass


class ResultSummarizer(Specable[ResultSummarizerSpec]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Specable.__init__(self, **kwargs)

    async def summarize(self, docs: AsyncIterable[Document]) -> AsyncIterable[DocSummary]:
        async for doc in docs:
            file_path = doc.metadata["source"]
            yield DocSummary(id=doc.id, file_name=file_path.split("/")[-1], file_path=file_path, text=doc.page_content)
