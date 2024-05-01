from __future__ import annotations

import copy
from asyncio import Semaphore
from typing import Optional

from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from eidolon_ai_client.client import Agent
from eidolon_ai_client.events import ObjectOutputEvent, AgentStateEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_client.util.stream_collector import merge_streams
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.builtins.logic_units.web_search import Browser
from eidolon_ai_sdk.cpu.agent_cpu import APU
from eidolon_ai_sdk.cpu.agent_io import SystemAPUMessage, UserTextAPUMessage
from eidolon_ai_sdk.system.processes import MongoDoc
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


class CrawlBody(BaseModel):
    url: str | list[str]
    maximum_pages: int = 5
    deduplication_key: Optional[str] = None


class WebsiteContent(BaseModel):
    url: str
    content: str


class CrawlResponse(BaseModel):
    content: str | None = None
    relevant_urls: list[str] = []


class CrawlerSpec(BaseModel):
    description: str = "General Purpose Web Crawler"
    system_prompt: str = """You are a research assistant helping a user do research on a topic.
    The user will come to you with the content of a website and you are responsible for extracting any content that 
    may be relevant. You are also responsible for finding links in the website are worth researching further. 
    Only return relevant urls and ignore irrelevant ones.
    Only return content if there is relevant content to extract.
    
    Topic:
    {{ topic }}"""
    user_prompt: str = "{{ content }}"
    prompt_args: dict = dict(topic="General Information")
    apu: AnnotatedReference[APU]
    browser: AnnotatedReference[Browser]
    json_schema_override: dict = None
    parallelism: int = 10
    throttle: AnnotatedReference[Semaphore, fqn(Semaphore)]  # todo, this is not stateless


def make_description(agent: WebCrawler, *args, **kwargs) -> str:
    return agent.spec.description


class WebCrawler(Specable[CrawlerSpec]):
    metadata: Metadata
    spec: CrawlerSpec
    apu: APU
    browser: Browser
    env: Environment
    semaphore: Semaphore

    def __init__(self, spec: CrawlerSpec, metadata: Metadata):
        super().__init__(spec=spec)
        self.metadata = metadata
        self.apu = self.spec.apu.instantiate()
        self.browser = self.spec.browser.instantiate(processing_unit_locator=self.apu)
        self.env = Environment(undefined=StrictUndefined)
        self.semaphore = self.spec.throttle.instantiate(self.spec.parallelism)

    @register_action("initialized", "idle", description=make_description)
    async def crawl(self, body: CrawlBody):
        pages = 0
        if isinstance(body.url, list):
            resp = CrawlResponse(content=None, relevant_urls=body.url)
        else:
            await self.semaphore.acquire()
            try:
                resp = await self._crawl(body)
            finally:
                self.semaphore.release()
        if resp.content:
            content = WebsiteContent(url=body.url, content=resp.content)
            yield ObjectOutputEvent(content=content)
            pages += 1
        if pages < body.maximum_pages:
            agent = Agent.get(self.metadata.name)
            streams = [agent.stream_program(action_name="crawl", body=CrawlBody(url=url, maximum_pages=body.maximum_pages)) for url in resp.relevant_urls]
            async for event in merge_streams(streams):
                if event.is_root_and_type(ObjectOutputEvent):
                    yield event
                    pages += 1
                    if pages >= body.maximum_pages:
                        for stream in streams:
                            stream.aclose()
                        break
                else:
                    logger.debug(f"Skipping event: {event}")
        yield AgentStateEvent(state="idle")

    async def _crawl(self, body: CrawlBody) -> CrawlResponse:
        pid = RequestContext.get('process_id')
        dedup_prefix = body.deduplication_key or pid
        try:
            await CrawlRecord.create(
                _id=dedup_prefix + ":" + body.url,
                dedup_key=dedup_prefix,
                url=body.url,
                crawling_agent=self.metadata.name,
                crawling_process=pid
            )
            kwargs = copy.deepcopy(self.spec.prompt_args)
            kwargs["content"] = await self.browser.go_to_url(body.url)

            thread = await self.apu.new_thread()
            system_message = SystemAPUMessage(prompt=self.env.from_string(self.spec.system_prompt).render(**kwargs))
            user_message = UserTextAPUMessage(prompt=self.env.from_string(self.spec.user_prompt).render(**kwargs))
            if self.spec.json_schema_override:
                resp = await thread.run_request(prompts=[system_message, user_message], output_format=self.spec.json_schema_override)
                response = CrawlResponse(**resp)
            else:
                response = await thread.run_request(prompts=[system_message, user_message], output_format=CrawlResponse)
            if not response.content:
                logger.info(f"No relevant content found for url: {body.url}")
            return response
        except DuplicateKeyError:
            logger.info(f"Skipping duplicate url: {body.url}")
            return CrawlResponse()


class CrawlRecord(MongoDoc):
    collection = "web_crawl_records"
    url: str
    crawling_agent: str
    crawling_process: str
