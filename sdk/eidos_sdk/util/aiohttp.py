from aiohttp import ClientSession as _ClientSession

from eidos_sdk.system.request_context import RequestContext


class ClientSession(_ClientSession):
    def __init__(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers'].update(RequestContext.headers)
        super().__init__(*args, **kwargs)