from typing import Dict
from playwright.async_api import async_playwright
from .browser import BrowserContext


class BrowserService:
    def __init__(self):
        self.contexts: Dict[str, BrowserContext] = {}
        self.playwright = None
        self.browser = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()

    async def stop(self):
        if self.playwright:
            await self.playwright.stop()
        self.playwright = None
        self.browser = None

    async def get_or_create_context(self, context_id: str) -> BrowserContext:
        if context_id not in self.contexts:
            context = await self.browser.new_context()
            self.contexts[context_id] = BrowserContext(context, self.browser)
        return self.contexts[context_id]

    async def delete_context(self, context_id: str):
        if context_id in self.contexts:
            await self.contexts[context_id].cleanup()
            del self.contexts[context_id]
