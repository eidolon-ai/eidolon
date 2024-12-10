import inspect
import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse, RedirectResponse

from eidolon_browser_service.api import PageInfo, PlaywrightActionRequest, PlaywrightActionResponse
from eidolon_browser_service.service import BrowserService

logger = logging.getLogger("browser-service")
browser_service = BrowserService()


@asynccontextmanager
async def lifespan(app):
    await browser_service.start()
    yield
    await browser_service.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.post("/contexts/{context_id}/pages")
async def create_page(context_id: str):
    context = await browser_service.get_or_create_context(context_id)
    page = await context.create_page()
    return PageInfo(page_id=page.page_id, url=None)


@app.get("/contexts/{context_id}/pages")
async def list_pages(context_id: str):
    context = await browser_service.get_or_create_context(context_id)
    return {
        "pages": [
            PageInfo(page_id=page.page_id, url=page.page.url if page.page.url != "about:blank" else None)
            for page in context.pages.values()
        ]
    }


@app.delete("/contexts/{context_id}")
async def delete_context(context_id: str):
    await browser_service.delete_context(context_id)
    return {"status": "deleted"}


@app.post("/contexts/{context_id}/pages/{page_id}/actions/{action}")
async def do_action(context_id: str, page_id: str, action: str, request: PlaywrightActionRequest) -> PlaywrightActionResponse:
    context = await browser_service.get_or_create_context(context_id)
    page = context.get_page(page_id)
    if not hasattr(page.page, action):
        raise HTTPException(status_code=404, detail="action not found")
    method = getattr(page.page, action)
    if not callable(method):
        raise HTTPException(status_code=404, detail="action is not callable")
    try:
        maybe_awaitable = method(*request.args, **request.kwargs)
        result = await maybe_awaitable if inspect.isawaitable(maybe_awaitable) else maybe_awaitable
        try:
            json.dumps(result)  # janky serialization check
            return PlaywrightActionResponse(result=result)
        except Exception:
            logger.debug(f"Action returned unserializable result")
            return PlaywrightActionResponse(result=None)
    except Exception as e:
        if logger.isEnabledFor(logging.DEBUG):
            logger.warning(f"Error executing action:\n{request.action} {request.args} {request.kwargs}", exc_info=True)
        else:
            logger.warning(f"Error executing action: {type(e).__name__}: {e}")
        raise HTTPException(status_code=422, detail=f"{type(e).__name__}: {e}")


@app.get("/contexts/{context_id}/pages/{page_id}/content", response_class=HTMLResponse)
async def get_page_content(
        context_id: str,
        page_id: str,
):
    context = await browser_service.get_or_create_context(context_id)
    page = context.get_page(page_id)
    return await page.page.content()
