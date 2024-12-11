# Eidolon Browser Service
This is a playwright wrapper that allows you to run browser automation for AI Agents. It exposes a restapi to create new 
pages, execute javascript code on a page, and get the page content. It supports OpenAPI and hosts a swagger UI on /docs.

To use this service as a client pip install. There is an optional extra 'server' that includes the dependencies needed 
to run the server, keeping this library as a lightweight client.

## Running the service
```shell
docker run -p 7468:7468 eidolonai/browser_service:latest
```

> Note: The dockerfile has the CMD ["uvicorn", "eidolon_browser_service.main:app", "--host", "0.0.0.0", "--port", "7468"]

## Customization
```.dotenv
BROWSER_SERVICE_CONTEXT_LIMIT=20  # the maximum number of browser contexts that can be created. Can be disabled by setting to -1
BROWSER_SERVICE_CONTEXT_TTL=3600  # the ttl time in seconds of a browser context. Can be disabled by setting to -1
```

## Usage
```python
from eidolon_browser_service.async_client import Browser

async def main():
    context = Browser().context("context_id")
    page = await context.new_page()
    await page.goto("https://google.com")
    await page.actions(action="fill", kwargs=dict(selector="textarea[name='q']", value="Eidolon AI"))
    await page.actions(action="click", kwargs=dict(selector="input[name='btnK']"))
    print(await page.content())
    await context.delete()
```
