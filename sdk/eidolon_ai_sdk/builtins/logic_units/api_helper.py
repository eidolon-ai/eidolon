import os
import yaml
from urllib.parse import urljoin, quote_plus

from httpx import AsyncClient, Timeout
from jinja2 import Template

from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_client.util.logger import logger
from pydantic import BaseModel


async def get_content(url: str, headers=None, **kwargs):
    params = {"url": url}
    if headers:
        params["headers"] = headers
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        response = await client.get(**params, **kwargs)
        await AgentError.check(response)
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            return response.json()
        # Needs to include text/plain because some specs return text/plain for yaml like anything from github
        elif 'application/x-yaml' in content_type or 'text/yaml' in content_type or 'text/plain' in content_type or 'charset=utf-8' in content_type:
            return yaml.safe_load(response.text)
        else:
            raise ValueError(f"Unsupported content type {content_type} did not match accepted types: application/json, application/x-yaml, text/yaml, text/plain")


async def post_content(url: str, headers=None, **kwargs):
    params = {"url": url}
    if headers:
        params["headers"] = headers

    # Ensure the body is passed as JSON in the request
    body = kwargs.get("body", {})

    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        print(f"real body: {body}")
        response = await client.post(**params, json=body)  # Send the body as JSON
        await AgentError.check(response)
        return response.json()
    

async def patch_content(url: str, headers=None, **kwargs):
    params = {"url": url}
    if headers:
        params["headers"] = headers

    # Ensure the body is passed as JSON in the request
    body = kwargs.get("body", {})

    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        print(f"real body: {body}")
        response = await client.patch(**params, json=body)  # Send the body as JSON
        await AgentError.check(response)
        return response.json()


def _render_template_from_env(template_string):
    template = Template(template_string)
    rendered_template = template.render(os.environ)
    return rendered_template


def build_call(extra_header_params, extra_query_params, root_call_url):
    async def do_call(path_to_call, method, query_params, headers, body):
        nonlocal extra_header_params, extra_query_params, root_call_url
        path_to_call = path_to_call.lstrip("/")
        headers = headers or {}
        headers["Content-Type"] = "application/json"

        if extra_header_params:
            for k, v in extra_header_params.items():
                headers[k] = _render_template_from_env(v)

        if extra_query_params:
            for k, v in extra_query_params.items():
                query_params.append((k, _render_template_from_env(v)))

        if query_params and len(query_params) > 0:
            path_to_call += "?" + "&".join([f"{quote_plus(k)}={quote_plus(str(v))}" for k, v in query_params if v])

        url = urljoin(root_call_url + "/", path_to_call)
        logger.info(f"Calling API {url}")
        try:
            print(f"Headers: {headers}")
            if method == "get":
                return await get_content(url, headers=headers, **body)
            elif method == "post":
                if isinstance(body, BaseModel):  # Check if body is a Pydantic model
                    body = body.dict(exclude_none=True)  # Convert Pydantic model to a dictionary

                print(f"Body: {body}")
                return await post_content(url, headers=headers, body=body)
            elif method == "patch":
                if isinstance(body, BaseModel):
                    body = body.dict(exclude_none=True)
                
                print(f"Body: {body}")
                return await patch_content(url, headers=headers, body=body)
            else:
                logger.error(f"Unsupported method {method}")
                return {}
        except Exception as e:
            logger.error(f"Error calling {url}: {e}, body = {body}")
            raise e

    return do_call