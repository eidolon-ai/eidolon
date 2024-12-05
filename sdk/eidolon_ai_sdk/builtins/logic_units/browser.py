from __future__ import annotations

import os
from typing import Optional

from pydantic import Field

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.system.tool_builder import ToolBuilder
from eidolon_browser_service.async_client import Browser, Page


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
async def browser_build(spec: BrowserV2, call_context: CallContext):
    context_str = f"pid-{call_context.process_id}-tid-{call_context.thread_id}"
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

    tool_desc = spec.description.format(page_content=current_page_content)
    url_desc = "Go to a specified url. Will be performed prior to evaluating javascript if both are provided"
    js_desc = "Evaluate JavaScript and return the response. Will be performed after going to a url if both are provided."

    if page and page.url:
        @BrowserV2.tool(description=tool_desc)
        async def browser_page(
                go_to_url: Optional[str] = Field(None, description=url_desc),
                evaluate_js: Optional[str] = Field(None, description=js_desc),
        ):
            return await _browser_page(go_to_url, evaluate_js, page)
    else:
        @BrowserV2.tool(description=tool_desc)
        async def browser_page(
                go_to_url: str = Field(description=url_desc),
                evaluate_js: Optional[str] = Field(None, description=js_desc),
        ):
            return await _browser_page(go_to_url, evaluate_js, page if page else await browser.create_page())


async def _browser_page(go_to_url: Optional[str], evaluate_js: Optional[str], page: Page):
    if not go_to_url and not evaluate_js:
        raise ValueError("Must include go_to_url or evaluate_js.")
    if not page.url and not go_to_url:
        raise ValueError("Must include go_to_url if no page is running.")
    response = dict()
    if go_to_url:
        page = await page.go_to_url(go_to_url)
        response['went to url'] = go_to_url
    if evaluate_js:
        code_response = await page.evaluate(evaluate_js)
        response['evaluated JavaScript result'] = code_response.result

    return response
