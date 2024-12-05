from typing import Dict, Optional
import uuid

from fastapi import HTTPException
from playwright.async_api import Page


class ManagedPage:
    page_id: str
    page: Page

    def __init__(self, page_id: str, page: Page):
        self.page_id = page_id
        self.page = page


class BrowserContext:
    def __init__(self, context, browser):
        self.context = context
        self.browser = browser
        self.pages: Dict[str, ManagedPage] = {}

    async def create_page(self) -> ManagedPage:
        page = await self.context.new_page()
        page_id = str(uuid.uuid4())
        managed_page = ManagedPage(page_id, page)
        self.pages[page_id] = managed_page
        return managed_page

    async def cleanup(self):
        await self.context.close()
        await self.browser.close()

    def get_page(self, page_id: str) -> ManagedPage:
        page = self.pages.get(page_id)
        if not page:
            raise HTTPException(status_code=404, detail="Page not found")
        return page
