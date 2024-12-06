from __future__ import annotations

import os
from textwrap import dedent
from typing import Optional, Literal

from bs4 import BeautifulSoup
from pydantic import Field, BaseModel

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.system.tool_builder import ToolBuilder
from eidolon_browser_service.async_client import Browser, EvaluationError


class Summarizer(BaseModel):
    tool_description: str = "Summarize the current page (Current url: {url})"
    mode: Literal["BeautifulSoup", "noop"]

    def clean_html(self, soup, tag):
        """Strip away everything except essential attributes and structure"""
        keep_attrs = ['id', 'class', 'href', 'type', 'name']

        # Create new tag with only desired attributes
        attrs = {k: v for k, v in tag.attrs.items() if k in keep_attrs}
        new_tag = soup.new_tag(tag.name, attrs=attrs)

        # Recursively process child elements
        for child in tag.children:
            if isinstance(child, str):
                if child.strip():
                    new_tag.append(child.strip())
            elif child.name:
                new_tag.append(BeautifulSoup(self.clean_html(soup, child), 'lxml').find(child.name))

        return str(new_tag)

    def summarize(self, text: str):
        if self.mode == "BeautifulSoup":
            soup = BeautifulSoup(text, "lxml")

            # Remove unwanted elements
            for tag in soup.find_all(['head', 'style', 'script', 'svg', 'noscript']):
                tag.decompose()

            # Clean and collect main sections
            cleaned_html = []

            # Process body
            body = soup.find('body')
            if body:
                cleaned_html.append(self.clean_html(soup, body))
                body.decompose()

            # Process footer (now no risk of duplication)
            footer = soup.find('footer')
            if footer:
                cleaned_html.append(self.clean_html(soup, footer))

            return "\n".join(cleaned_html)
        else:
            return text


class BrowserV2(ToolBuilder):
    starting_url: Optional[str] = None
    browser_service_loc: str = Field(default=os.environ.get("BROWSER_SERVICE_URL", "http://localhost:7468"), description="The location of the playwright installation.", examples=["http://localhost:7468"])
    go_to_url_description: str = "Go to a specified url"
    go_to_url_summarizer: Optional[Summarizer] = Summarizer(mode="BeautifulSoup")
    evaluate_description: str = dedent("""
    Evaluate javascript on the current page and return the last expression. This is how you interact with the DOM including retrieving structure, filling out forms, clicking buttons, etc.
    
    Will return immediately after the last expression is evaluated, so the page may not have fully loaded yet. If you need to wait for the page to load, do so explicitly or poll the page state.
    
    Current url: {url}
    """).strip()


@BrowserV2.dynamic_contract
async def browser_build(spec: BrowserV2, call_context: CallContext):
    context_str = f"pid-{call_context.process_id}"
    browser = Browser(location=spec.browser_service_loc).context(context_str)
    pages = await browser.list_pages()

    if len(pages) > 1:
        logger.warning("LLM found more than one page running in the browser. Using the last one.")
        page = pages[-1]
    elif len(pages) == 1:
        page = pages[0]
    elif spec.starting_url:
        page = await browser.create_page()
        page = await page.navigate(spec.starting_url)
    else:
        page = None

    @BrowserV2.tool(description=spec.go_to_url_description)
    async def go_to_url(url: str):
        page_ = page or await browser.create_page()
        await page_.navigate(url)
        if spec.go_to_url_summarizer:
            return spec.go_to_url_summarizer.summarize(await page_.get_content())
        else:
            return f"Successfully went to {url}"

    if page and page.url:
        @BrowserV2.tool(description=spec.evaluate_description.format(url=page.url))
        async def evaluate(javascript: str):
            try:
                return await page.evaluate(javascript)
            except EvaluationError as e:
                logger.warning(f"Error evaluating agent javascript: {e}")
                return str(e)
