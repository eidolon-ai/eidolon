import functools
from contextlib import contextmanager

try:
    from unittest.mock import patch
except ImportError:
    patch = None

from eidolon_ai_sdk.agent.doc_manager.transformer import document_transformer
from eidolon_ai_sdk.system import agent_controller, process_file_system


@contextmanager
def vcr_patch(test_name):
    with patched_vcr_aiohttp_url_encoded(), patched_vcr_object_handling(), deterministic_ids(test_name):
        yield


@contextmanager
def deterministic_ids(id_prefix):
    if patch is None:
        raise ImportError("unittest.mock.patch is required for this helper")

    pid_generator = _deterministic_id_generator(id_prefix)
    fid_generator = _deterministic_id_generator(id_prefix + "_file")

    def patched_pid(*args, **kwargs):
        return next(pid_generator)

    def patched_fid(*args, **kwargs):
        return next(fid_generator)

    with (
        patch.object(agent_controller, "ObjectId", new=patched_pid),  # process_id
        patch.object(process_file_system, "ObjectId", new=patched_fid),  # file_id
        patch.object(document_transformer, "ObjectId", new=patched_fid)  # document_id
    ):
        yield


@contextmanager
def patched_vcr_aiohttp_url_encoded():
    """
    vcr has a bug around how it handles multipart requests, and it is wired in for everything,
    even the fake test client requests, so we need to pipe the body through ourselves
    """

    from vcr.stubs import aiohttp_stubs
    import urllib.parse
    if patch is None:
        raise ImportError("unittest.mock.patch is required for this helper")

    original = aiohttp_stubs.vcr_request

    def my_custom_function(cassette, real_request):
        fn = original(cassette, real_request)

        @functools.wraps(real_request)
        async def new_request(self, method, url, **kwargs):
            data = kwargs.get("data")
            if "Content-Type" in kwargs.get("headers", {}):
                if "application/x-www-form-urlencoded" in kwargs["headers"]["Content-Type"] and isinstance(data, dict):
                    # url encode the data
                    kwargs["data"] = urllib.parse.urlencode(data)

            return await fn(self, method, url, **kwargs)

        return new_request

    with patch.object(aiohttp_stubs, "vcr_request", new=my_custom_function):
        yield


@contextmanager
def patched_vcr_object_handling():
    """
    VCR prematurely reads/decodes response body
    """

    from vcr.request import Request as VcrRequest
    if patch is None:
        raise ImportError("unittest.mock.patch is required for this helper")

    def my_custom_function(httpx_request, **kwargs):
        uri = str(httpx_request.url)
        headers = dict(httpx_request.headers)
        return VcrRequest(httpx_request.method, uri, httpx_request, headers)

    from vcr.stubs import httpx_stubs
    with patch.object(httpx_stubs, "_make_vcr_request", new=my_custom_function):
        yield


def _deterministic_id_generator(prefix):
    count = 0
    while True:
        yield f"{prefix}_{count}"
        count += 1
