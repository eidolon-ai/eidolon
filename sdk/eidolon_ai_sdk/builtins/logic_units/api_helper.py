import os
from urllib.parse import urljoin, quote_plus

from httpx import AsyncClient, Timeout

from eidolon_ai_client.util.aiohttp import AgentError
from eidolon_ai_client.util.logger import logger


async def get_content(url: str, headers=None, **kwargs):
    params = {"url": url}
    if headers:
        params["headers"] = headers
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        response = await client.get(**params, **kwargs)
        await AgentError.check(response)
        return response.json()


async def post_content(url: str, headers=None, **kwargs):
    params = {"url": url}
    if headers:
        params["headers"] = headers
    async with AsyncClient(timeout=Timeout(5.0, read=600.0)) as client:
        response = await client.post(**params, **kwargs)
        await AgentError.check(response)
        return response.json()


def build_call(key_env_var, key_query_param, put_key_as_bearer_token, root_call_url):
    async def do_call(path_to_call, method, query_params, headers, body):
        nonlocal key_env_var, key_query_param, put_key_as_bearer_token, root_call_url
        path_to_call = path_to_call.lstrip('/')
        api_key = os.environ.get(key_env_var, None) if key_env_var else None
        headers = headers or {}
        headers["Content-Type"] = "application/json"
        if put_key_as_bearer_token and api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        if api_key and key_query_param:
            query_params.append((key_query_param, api_key))

        if query_params and len(query_params) > 0:
            path_to_call += "?" + "&".join([f"{quote_plus(k)}={quote_plus(str(v))}" for k, v in query_params if v])

        url = urljoin(root_call_url + "/", path_to_call)
        try:
            if method == "get":
                return await get_content(url, headers=headers, **body)
            elif method == "post":
                return await post_content(url, headers=headers, **body)
            else:
                logger.error(f"Unsupported method {method}")
                return {}
        except Exception as e:
            logger.error(f"Error calling {url}: {e}, body = {body}")
            raise e

    return do_call
