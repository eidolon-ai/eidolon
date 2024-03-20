from contextlib import AsyncExitStack
from typing import AsyncContextManager

from fastapi import FastAPI
from openai import BaseModel

from eidolon_ai_sdk.system.reference_model import Reference, Specable


class LifecycleManager(AsyncContextManager):
    app: FastAPI

    def __init__(self, app: FastAPI):
        self.app = app

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass


class MultiLifecycleSpec(BaseModel):
    managers: list[Reference[LifecycleManager]] = []


class MultiLifecycleManager(LifecycleManager, Specable[MultiLifecycleSpec]):
    stack = AsyncExitStack()
    managers: list[LifecycleManager]

    def __init__(self, app: FastAPI, spec: MultiLifecycleSpec):
        LifecycleManager.__init__(self, app=app)
        Specable.__init__(self, spec=spec)

        self.managers = [ref.instantiate(app=app) for ref in spec.managers]
        self.stack = AsyncExitStack()

    async def __aenter__(self, **kwargs):
        await self.stack.__aenter__()
        for manager in self.managers:
            await self.stack.enter_async_context(manager)

    async def __aexit__(self, exc_type, exc_value, traceback):
        return await self.stack.__aexit__(exc_type, exc_value, traceback)

