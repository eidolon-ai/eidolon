from contextlib import AsyncExitStack
from typing import AsyncContextManager

from openai import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.system.reference_model import Reference, Specable


class FlexibleManager(AsyncContextManager):
    def __init__(self, *args, **kwargs):
        pass

    async def __aexit__(self, *args, **kwargs):
        pass


class DynamicMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        async with AgentOS.get_instance(AsyncContextManager, "MiddlewareManager", request=request):
            return await call_next(request)


class MultiManagerSpec(BaseModel):
    managers: list[Reference[AsyncContextManager]] = []


class MultiContextManager(FlexibleManager, Specable[MultiManagerSpec]):
    stack = AsyncExitStack()
    managers: list[AsyncContextManager]

    def __init__(self, spec: MultiManagerSpec, **kwargs):
        Specable.__init__(self, spec=spec)

        self.managers = [ref.instantiate(**kwargs) for ref in spec.managers]
        self.stack = AsyncExitStack()

    async def __aenter__(self):
        await self.stack.__aenter__()
        for manager in self.managers:
            await self.stack.enter_async_context(manager)

    async def __aexit__(self, exc_type, exc_value, traceback):
        return await self.stack.__aexit__(exc_type, exc_value, traceback)
