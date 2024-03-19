from abc import abstractmethod
from typing import ContextManager, AsyncContextManager

from openai import BaseModel

from eidolon_ai_sdk.system.reference_model import Reference


class LifecycleManager(AsyncContextManager):
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

class MultiLifecycleManager(LifecycleManager, BaseModel):
    managers: list[Reference[LifecycleManager]]

    async def __aenter__(self, __exc_type, __exc_value, __traceback):
        pass
