import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse

from eidolon_browser_service.api import PageInfo, EvaluateRequest, EvaluateInfo, NavigateRequest
from eidolon_browser_service.service import BrowserService

logger = logging.getLogger("browser-service")
browser_service = BrowserService()


@asynccontextmanager
async def lifespan(app):
    await browser_service.start()
    yield
    await browser_service.stop()


app = FastAPI(lifespan=lifespan)


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


@app.post("/contexts/{context_id}/pages/{page_id}/evaluate")
async def evaluate_script(context_id: str, page_id: str, request: EvaluateRequest):
    context = await browser_service.get_or_create_context(context_id)
    page = context.get_page(page_id)
    try:
        result = await page.page.evaluate(request.script)
    except Exception as e:
        if logger.isEnabledFor(logging.DEBUG):
            logger.warning(f"Error executing script:\n{request.script}", exc_info=True)
        else:
            logger.warning("Error executing script")
        raise HTTPException(status_code=422, detail=f"{type(e).__name__}: {e}")
    return EvaluateInfo(result=str(result) if result is not None else None)


@app.post("/contexts/{context_id}/pages/{page_id}/navigate")
async def navigate(context_id: str, page_id: str, request: NavigateRequest):
    context = await browser_service.get_or_create_context(context_id)
    page = context.get_page(page_id)
    await page.page.goto(request.url)


@app.get("/contexts/{context_id}/pages/{page_id}/content", response_class=HTMLResponse)
async def get_page_content(
        context_id: str,
        page_id: str,
):
    context = await browser_service.get_or_create_context(context_id)
    page = context.get_page(page_id)
    return await page.page.content()
