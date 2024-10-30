from collections import namedtuple
from typing import Optional, Callable, Generic, Awaitable, TypeVar, AsyncIterable, Any

from openai import BaseModel

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_sdk.apu.call_context import CallContext


T = TypeVar("T", bound=BaseModel)


_ToolDefinition = namedtuple("_ToolDefinition", ["name", "description", "input_schema", "fn"])


class DefaultToolSpec(BaseModel):
    pass


class ToolUnit(Generic[T]):
    def __init__(self, spec_type: T = DefaultToolSpec):
        self._spec_type = spec_type
        self._tools = []
        self._dynamic_contracts = []
        self._clone_thread_hooks = []
        self._delete_process_hooks = []

    def dynamic_contract(self, fn: Callable[[T, CallContext], Awaitable[None] | None]):
        """
        A decorator to dynamically build a ToolUnit.
        Decorated function may be synchronous or asynchronous.

        @tool_unit.dynamic_contract
        def fn(spec: MySpec, call_context: CallContext):
            @tool_unit.tool(description = spec.description)
            async def add(a: int, b: int):
                return a + b
        """
        self._dynamic_contracts.append(fn)
        return fn

    def tool(
            self,
            name: str,
            description: Optional[str] = None,
            input_schema: dict = None
    ) -> Callable[[Callable[..., Awaitable[Any] | AsyncIterable[StreamEvent]]], Callable]:
        """
        A decorator to define a tool.
        Decorated function must be asynchronous and may return a value or yield StreamEvent(s).

        @tool_unit.tool(description = "add two numbers")
        async def add(a: int, b: int):
            return a + b

        :param name: The name of the tool presented to the llm
        :param description: The description of the tool presented to the llm
        :param input_schema: Optional input schema to present to the llm. Dynamically built from the function signature if not provided.
        :return: A decorator
        """

        def decorator(fn: Callable[..., Awaitable[Any] | AsyncIterable[StreamEvent]]):
            self._tools.append(_ToolDefinition(name, description, input_schema, fn))
            return fn

        return decorator

    def clone_thread_hook(self, fn: Callable[[CallContext, CallContext], Awaitable[None]]):
        """
        A decorator to define a hook that is called when a thread is cloned.
        Decorated function must be asynchronous.
        """

        self._clone_thread_hooks.append(fn)
        return fn

    def delete_process_hook(self, fn: Callable[[str], Awaitable[None]]):  # async def fn(process_id: string)
        """
        A decorator to define a hook that is called when a process is deleted.
        Decorated function must be asynchronous.
        """
        self._delete_process_hooks.append(fn)
        return fn

