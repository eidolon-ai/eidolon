import os
from typing import Optional
from urllib.parse import urljoin

from httpx import AsyncClient
from pydantic import BaseModel, Field

from eidolon_ai_sdk.apu.logic_unit import LogicUnit, llm_function
from eidolon_ai_sdk.system.specable import Specable


class VectaraSearchSpec(BaseModel):
    """
    A logic unit for searching in Vectara. Requires the VECTARA_API_KEY environment variable to be set for authentication.
    """

    corpus_key: str = Field(description="The corpus key to search in.")
    description: str = Field("Search documents related to {corpus_key}.", description="Description of the tool presented to LLM. Will be formatted with corpus_key.")
    vectara_url: str = "https://api.vectara.io/"
    read_document_enabled: bool = Field(False, description="Enable read_document tool.")
    read_document_description: Optional[str] = Field("Read a document from {corpus_key}.", description="Description of the tool presented to LLM. Will be formatted with corpus_key.")


class VectaraSearch(Specable[VectaraSearchSpec], LogicUnit):
    async def build_tools(self, *args, **kwargs):
        handlers = await LogicUnit.build_tools(self, *args, **kwargs)
        if self.spec.read_document_enabled:
            return handlers
        else:
            return [h for h in handlers if h.name != "read_document"]

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

    @llm_function(description=lambda lu, _: lu.spec.description.format(corpus_key=lu.spec.corpus_key))
    async def query(self, query: str, limit: int = 10, offset: int = 0):
        async with AsyncClient() as client:
            response = await client.post(
                url=self._url(f"/v2/corpora/{self.spec.corpus_key}/query"),
                headers=self._headers,
                json=dict(
                    query=query,
                    search=dict(
                        limit=limit,
                        offset=offset,
                    )
                ),
            )
            response.raise_for_status()
            response_body = response.json()
            content = [dict(text=r.get("text"), document_id=r.get("document_id")) for r in response_body["search_results"]]
            documents = {r.get("document_id"): r.get("document_metadata", {}).get("title") for r in response_body["search_results"]}
            return dict(search_results=content, documents=documents)

    @llm_function(description=lambda lu, _: lu.spec.read_document_description.format(corpus_key=lu.spec.corpus_key))
    async def read_document(self, document_id: str):
        async with AsyncClient() as client:
            response = await client.get(
                url=self._url(f"/v2/corpora/{self.spec.corpus_key}/documents/{document_id}"),
                headers=self._headers,
            )
            response.raise_for_status()
            response_body = response.json()

            sections = []
            for part in response_body["parts"]:
                if part["metadata"].get("is_title", False):
                    sections.append((dict(title=part["text"], content=[])))
                    if "title_level" in part["metadata"]:
                        sections[-1]["title_level"] = part["metadata"]["title_level"]
                else:
                    if not sections:
                        sections.append(dict(title="", content=[]))
                    sections[-1]["content"].append(part["text"])
            for section in sections:
                section["content"] = "".join(section["content"])

            return dict(
                document_id=document_id,
                metadata=response_body["metadata"],
                sections=sections,
            )
