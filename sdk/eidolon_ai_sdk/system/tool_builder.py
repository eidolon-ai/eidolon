from typing import Optional, Callable, Generic, Awaitable

from eidolon_ai_sdk.apu.call_context import CallContext


class ToolUnit(Generic[T]):
    def __init__(self, spec_type: T):
        ...

    def tool(self, name: str, description: Optional[str] = None) -> Callable[[Callable[[T], Awaitable[None]]], None]:
        ...

    def dynamic_contract(self) -> Callable[[T, CallContext], Awaitable[None]]:  # async def fn(spec: T, call_context: CallContext)
        ...

    def create_process_hook(self, fn: Callable[[str], Awaitable[None]]):  # async def fn(process_id: string)
        ...

    def delete_process_hook(self, fn: Callable[[str], Awaitable[None]]):  # async def fn(process_id: string)
        ...

    async def clone_thread_hook(self, fn: Callable[[CallContext, CallContext], Awaitable[None]]):  # async def fn(old_context: CallContext, new_context: CallContext)
        ...
