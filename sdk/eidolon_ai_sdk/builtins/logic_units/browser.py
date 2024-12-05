from __future__ import annotations

import os
from typing import Optional

from pydantic import Field

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.system.tool_builder import ToolBuilder
from eidolon_browser_service.async_client import Browser


class BrowserV2(ToolBuilder):
    starting_url: Optional[str] = None
    browser_service_loc: str = Field(default=os.environ.get("BROWSER_SERVICE_URL", "http://localhost:7468"), description="The location of the playwright installation.", examples=["http://localhost:7468"])
    description: str = """
    This tool allows you to interact with a browser using playwright. You can go to a url or evaluate javascript on a page.
    The browser session (context) persists across the entire conversation.
    
    The current page content is:
    {page_content}
    """
    uninitialized_page_content: str = "[Page not initialized. No content available. Use go_to_url to initialize.]"


@BrowserV2.dynamic_contract
async def playwright_build(spec: BrowserV2, context: CallContext):
    context_str = f"pid/{context.process_id}/tid/{context.thread_id}"
    browser = Browser(location=spec.browser_service_loc).context(context_str)
    pages = await browser.list_pages()

    if len(pages) > 1:
        logger.warning("LLM found more than one page running in the browser. Using the last one.")
        page = pages[-1]
    elif len(pages) == 1:
        page = pages[0]
    elif spec.starting_url:
        page = await browser.create_page()
        page = await page.go_to_url(spec.starting_url)
    else:
        page = None

    current_page_content = await page.get_content() if page else spec.uninitialized_page_content

    @BrowserV2.tool(description=spec.description.format(page_content=current_page_content))
    async def browser_page(
            go_to_url: Optional[str] if page and page.url else str = Field(
                description="Go to a specified url. Will be performed prior to evaluating javascript if both are provided"
            ),
            evaluate_js: Optional[str] = Field(
                description="Evaluate JavaScript and return the response. Will be performed after going to a url if both are provided."
            ),
    ):
        page_ = page
        if not go_to_url and not evaluate_js:
            raise ValueError("Must include go_to_url or evaluate_js.")
        if not page_:
            if not go_to_url:
                raise ValueError("Must include go_to_url if no page is running.")
            else:
                page_ = await browser.create_page()
        response = dict()
        if go_to_url:
            page_ = await page_.go_to_url(go_to_url)
            response['went to url'] = go_to_url
        if evaluate_js:
            code_response = await page_.evaluate(evaluate_js)
            response['evaluated JavaScript result'] = code_response.result

        return response
