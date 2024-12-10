from __future__ import annotations

import os
from datetime import datetime
from textwrap import dedent
from typing import Optional, Literal, Union

import tiktoken
from bs4 import BeautifulSoup
from pydantic import Field, BaseModel, TypeAdapter, ConfigDict

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.system.tool_builder import ToolBuilder
from eidolon_browser_service.async_client import Browser, Page, BrowserError


class Summarizer(BaseModel):
    tool_description: str = "Summarize the current page (Current url: {url})"
    mode: Literal["BeautifulSoup", "noop"]
    encoding: str = Field("o200k_base", description="tiktoken encoding to use when counting tokens")
    token_limit: Optional[int] = Field(8000, description="The maximum number of message tokens to sent respond with")

    def clean_html(self, soup, tag):
        """Strip away everything except essential attributes and structure"""
        keep_attrs = {'id', 'class', 'href', 'type', 'name', 'value', 'src', 'alt', 'title', 'role'}

        # Create new tag with only desired attributes
        attrs = {k: v for k, v in tag.attrs.items() if k in keep_attrs or k.startswith("aria") or k.startswith("data")}
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

            return_string = "\n".join(cleaned_html)
        elif self.mode == "noop":
            return_string = text
        else:
            raise ValueError(f"Unknown summarizer mode: {self.mode}")

        encoding = tiktoken.get_encoding(self.encoding)
        encoded = encoding.encode(return_string)
        if self.token_limit and len(encoded) > self.token_limit:
            truncated = len(encoded) - self.token_limit
            encoded = encoded[:self.token_limit]
            logger.info(f"Truncated {truncated} tokens from summary")
            return_string = encoding.decode(encoded) + f"\n...truncated {truncated} tokens..."

        return return_string


class BrowserV2(ToolBuilder):
    """
    A tool for interacting with a browser instance.

    Requires a running browser service.

    Exposes two tools to an Agent, one for navigating to a url and another for evaluating javascript on the current page.
    Browser sessions are durable throughout a process, but each process has its own browser, isolating browsers between agents.
    """

    starting_url: Optional[str] = None
    browser_service_loc: str = Field(default=os.environ.get("BROWSER_SERVICE_URL", "http://localhost:7468"), description="The location of the playwright installation.", examples=["http://localhost:7468"])
    operation_description: str = dedent("""
    Perform the specified operation on the current page. The operation is executed using a playwright "Page" object.
    
    Prefer using fill / click to interact with the page over executing raw javascript when possible.
    
    REMEMBER: A selector can match multiple elements, and that the first element found will be interacted with. Be sure 
    to specify an index if you are using a selector that could have multiple matches. For example, to find the second 
    div with class "foo", you could use "(//div[contains(@class, 'foo')])[2]".
    
    The current page url as of {datetime} is "{url}"
    """).strip()
    content_summarizer: Optional[Summarizer] = Summarizer(mode="BeautifulSoup")


class Click(BaseModel):
    model_config = ConfigDict(json_schema_extra=dict(description=dedent("""
    Click on an element on the current page.
    """).strip()))

    operation_name: Literal["click"]
    selector: str


class Fill(BaseModel):
    model_config = ConfigDict(json_schema_extra=dict(description=dedent("""
    Fill in a form element on the current page.
    """).strip()))

    operation_name: Literal["fill"]
    selector: str
    value: str


class Evaluate(BaseModel):
    model_config = ConfigDict(json_schema_extra=dict(description=dedent("""
    Evaluate a javascript expression on the current page.
    
    Example:
    operation = "evaluate"
    expression = "() => document.title"
    """).strip()))

    operation_name: Literal["evaluate"]
    expression: str


class GoTo(BaseModel):
    model_config = ConfigDict(json_schema_extra=dict(description=dedent("""
    Navigate to a new page. Will wait for the page to load.
    """).strip()))

    operation_name: Literal["goto"]
    url: str


class GetContent(BaseModel):
    model_config = ConfigDict(json_schema_extra=dict(description=dedent("""
    Get the HTML content of the current page. Content will be summarized to skip head, scripts, and some attributes to reduce size.
    """).strip()))

    operation_name: Literal["get_content"]


@BrowserV2.dynamic_contract
async def browser_build(spec: BrowserV2, call_context: CallContext):
    context_str = f"pid-{call_context.process_id}"
    browser = Browser(location=spec.browser_service_loc).context(context_str)
    pages = await browser.list_pages()
    datetime.utcnow()

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

    format_args = dict(datetime=str(datetime.utcnow()), url=str(page.url if page else None))

    adapter = TypeAdapter(Union[Click, Fill, Evaluate, GoTo, GetContent]) if page and page.url else TypeAdapter(GoTo)
    adapter_schema = adapter.json_schema()
    parameters = dict(
        type="object",
        properties=dict(kwargs=adapter_schema),
    )
    if "$defs" in adapter_schema:
        parameters["$defs"] = adapter_schema.pop("$defs")

    @BrowserV2.tool(description=spec.operation_description.format(**format_args), parameters=parameters)
    async def operation(kwargs: dict):
        op: Click | Fill | Evaluate | GoTo | GetContent = adapter.validate_python(kwargs)
        page_: Page = page or await browser.create_page()
        if isinstance(op, GetContent):
            utcnow = datetime.utcnow()
            text = await page_.get_content()
            if spec.content_summarizer:
                text = spec.content_summarizer.summarize(text)
            return f"Page content as of {utcnow}:\n{text}"
        else:
            try:
                result = await page_.actions(action=op.operation_name, kwargs=op.model_dump(exclude={"operation_name"}))
                rtn = result.model_dump(exclude={"result"} if result.result is None else {})
                rtn["end_time"] = str(datetime.utcnow())
                return rtn
            except BrowserError as e:
                logger.warning(f"Browser error: {e}")
                return str(e)
