import copy
import json
import os
from typing import Annotated
from urllib.parse import urljoin

from fastapi import Body
from httpx import AsyncClient
from httpx_sse import EventSource
from pydantic import BaseModel, Field

from eidolon_ai_client.events import StringOutputEvent, StartStreamContextEvent, ObjectOutputEvent, \
    EndStreamContextEvent, AgentStateEvent
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.system.processes import MongoDoc
from eidolon_ai_sdk.system.reference_model import Specable


os.environ.setdefault("VECTARA_API_KEY", "test")


class VectaraAgentSpec(BaseModel):
    """
    An agent backed by Vectara. Requires the VECTARA_API_KEY environment variable to be set for authentication.
    """

    corpus_key: str
    description: str = "Search documents related to {{ corpus_key }}"
    vectara_url: str = "https://api.vectara.io/"
    body_overrides: dict = Field({}, description="Arguments to use when creating / continuing a chat. See https://docs.vectara.com/docs/rest-api/create-chat for more information.")


# We need to store chatid / processid mappings since vectara doesn't have metatdata / query concepts
class VectaraDoc(MongoDoc):
    collection = "vectara_docs"
    process_id: str
    vectara_chat_id: str
    metadata: dict = {}


class VectaraAgent(Specable[VectaraAgentSpec]):
    @property
    def _token(self):
        return os.environ["VECTARA_API_KEY"]

    @property
    def _headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream',
            'x-api-key': self._token
        }

    def _url(self, suffix):
        return urljoin(self.spec.vectara_url, suffix)

    @register_action("initialized", "idle", description=lambda agent, _: agent.spec.description)
    async def converse(self, process_id, question: Annotated[str, Body()]):
        body = copy.deepcopy(self.spec.body_overrides)
        body.setdefault("search", {}).setdefault("corpora", [{}])
        for corpus in body["search"]["corpora"]:
            corpus.setdefault("corpus_key", self.spec.corpus_key)
        body["query"] = question
        body["stream_response"] = True

        doc = await VectaraDoc.find_one(query=dict(process_id=process_id))
        async with AsyncClient() as client:
            response = await client.post(
                url=self._url("/v2/chats" if not doc else f"/v2/chats/{doc.vectara_chat_id}/turns"),
                headers=self._headers,
                json=body,
            )
        response.raise_for_status()

        yield StartStreamContextEvent(context_id="response_info", title="Response Information")
        try:
            async for sse_event in EventSource(response).aiter_sse():
                if sse_event.event == "chat_info":
                    if not doc:
                        data = json.loads(sse_event.data)
                        doc = await VectaraDoc.create(process_id=process_id, vectara_chat_id=data['chat_id'])
                elif sse_event.event == "generation_chunk":
                    data = json.loads(sse_event.data)
                    yield StringOutputEvent(content=data['generation_chunk'])
                elif sse_event.event == "search_results":
                    for result in json.loads(sse_event.data)["search_results"]:
                        yield ObjectOutputEvent(stream_context="response_info", content=result)
                elif sse_event.event == "factual_consistency_score":
                    yield ObjectOutputEvent(stream_context="response_info", content=json.loads(sse_event.data))
        finally:
            yield EndStreamContextEvent(context_id="response_info")

        yield AgentStateEvent(state="idle")
