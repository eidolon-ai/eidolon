import asyncio
import os
from typing import Optional

import time
from playwright.async_api import async_playwright, Browser, Playwright

from eidolon_browser_service.browser import BrowserContext
from eidolon_browser_service.browser_logging import logger


class BrowserService:
    def __init__(self):
        self.max_size = int(os.environ.get("BROWSER_SERVICE_CONTEXT_LIMIT", "20"))
        self.max_ttl = int(os.environ.get("BROWSER_SERVICE_CONTEXT_TTL", str(60 * 60)))
        self.contexts: dict[str, _ContextWrapper] = {}
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.background_task: Optional[asyncio.Task] = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.background_task = asyncio.create_task(background_ttl_check(self))

    async def stop(self):
        if self.background_task:
            self.background_task.cancel()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.playwright = None
        self.browser = None
        self.background_task = None

    async def get_or_create_context(self, context_id: str) -> BrowserContext:
        if context_id not in self.contexts:
            if self.max_size > 0 and len(self.contexts) >= self.max_size:
                sorted_contexts = sorted(self.contexts.values(), reverse=True)
                while len(sorted_contexts) >= self.max_size:
                    last = sorted_contexts.pop()
                    last.background_cleanup()
                    logger.info(
                        "Context limit exceeded. Cleaning up oldest context %s",
                        last.context_id,
                    )
            context = BrowserContext(await self.browser.new_context())
            self.contexts[context_id] = _ContextWrapper(
                context_id, context, time.perf_counter()
            )
        return self.contexts[context_id].context

    async def delete_context(self, context_id: str):
        if context_id in self.contexts:
            await self.contexts[context_id].context.cleanup()
            del self.contexts[context_id]


class _ContextWrapper:
    def __init__(self, context_id: str, context: BrowserContext, last_used: float):
        self.context_id = context_id
        self.context = context
        self.last_used = last_used

    def __lt__(self, other):
        return self.last_used < other.last_used

    def background_cleanup(self):
        asyncio.create_task(self._cleanup())

    async def _cleanup(self):
        try:
            await self.context.cleanup()
        except Exception:
            logger.exception(f"Failed to cleanup context, {self.context_id}")


async def background_ttl_check(service: BrowserService):
    while True:
        try:
            await asyncio.sleep(60)
            current_time = time.perf_counter()
            sorted_contexts = sorted(service.contexts.values(), reverse=True)
            acc = []
            while sorted_contexts and sorted_contexts[-1].last_used + service.max_ttl < current_time:
                to_clean = sorted_contexts.pop()
                del service.contexts[to_clean.context_id]
                acc.append(to_clean)
            for record in acc:
                try:
                    await record.context.cleanup()
                    logger.info(f"Removed context due to TTL: {record.context_id}")
                except Exception:
                    logger.exception(f"Error cleaning context: {record.context_id}")
        except asyncio.CancelledError:
            break
        except Exception:
            logger.exception("Context TTL check failed")
