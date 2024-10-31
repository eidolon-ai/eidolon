from collections import namedtuple
from typing import Optional, Callable, Awaitable, TypeVar, AsyncIterable, Any, List

from openai import BaseModel

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.system.fn_handler import FnHandler

T = TypeVar("T", bound=BaseModel)

_ToolUnitState = namedtuple("_ToolUnitState", ["dynamic_contracts", "tools"])
_ToolDefinition = namedtuple("_ToolDefinition", ["name", "description", "input_schema", "fn"])


class ToolUnit(BaseModel):
    @classmethod
    def _state(cls) -> _ToolUnitState:
        if not hasattr(cls, "_state"):
            cls._state = _ToolUnitState(
                dynamic_contracts=[],
                tools=([], []),
            )
        return cls._state

    @classmethod
    def _locked(cls) -> _ToolUnitState:
        return getattr(cls, "_locked", False)

    @classmethod
    def dynamic_contract(cls, fn: Callable[[T, CallContext], Awaitable[None] | None]):
        """
        A decorator to dynamically build a ToolUnit.
        Decorated function may be synchronous or asynchronous.
        
        ```python
        @tool_unit.dynamic_contract
        def fn(spec: MySpec, call_context: CallContext):
            @tool_unit.tool(description = spec.description)
            async def add(a: int, b: int):
                return a + b
        ```
        """
        cls._state().dynamic_contracts.append(fn)
        return fn

    @classmethod
    def tool(
            cls,
            name: str = None,
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
            name_ = name or fn.__name__
            if cls._locked():
                cls._state().tools[1].append(_ToolDefinition(name_, description, input_schema, fn))
            else:
                cls._state().tools[0].append(_ToolDefinition(name_, description, input_schema, fn))
            return fn

        return decorator

    def clone_thread(self, old_context: CallContext, new_context: CallContext):
        """
        Custom logic to execute when cloning a thread.

        :param old_context: context of the old thread
        :param new_context: context of the new thread
        """
        pass

    async def delete_process(self, process_id: str):  # async def fn(process_id: string)
        """
        Custom logic to execute when deleting a process.

        :param process_id: The process id being deleted
        """
        pass

    async def build_tools(self, call_context: CallContext) -> List[FnHandler]:
        ...
        # todo
