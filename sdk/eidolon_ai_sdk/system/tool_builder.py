import inspect
from collections import namedtuple
from contextlib import contextmanager
from inspect import Parameter
from typing import Optional, Callable, Awaitable, TypeVar, AsyncIterable, Any, List, cast, Type, get_type_hints

from pydantic import create_model, BaseModel

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_sdk.apu.call_context import CallContext
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.util.partial import partial, return_value

_ToolBuilderState = namedtuple("_ToolBuilderState", ["dynamic_contracts", "tools"])
_ToolDefinition = namedtuple("_ToolDefinition", ["name", "description", "parameter", "fn"])


T = TypeVar("T", bound="ToolBuilder")


class ToolBuilder(BaseModel):
    @classmethod
    def dynamic_contract(cls: Type[T], fn: Callable[[T, CallContext], Awaitable[None] | None]):
        """
        A decorator to dynamically build a ToolBuilder.
        Decorated function may be synchronous or asynchronous.
        Decorator function may take a spec and/or call_context argument.

        .. code-block:: python
            @MyToolBuilder.dynamic_contract
            def fn(spec: MyToolBuilder, call_context: CallContext):
                @MyToolBuilder.tool(description = spec.description)
                async def add(a: int, b: int):
                    return a + b
        """
        cls._state().dynamic_contracts.append(fn)
        return fn

    @classmethod
    def tool(
            cls: Type[T],
            name: str = None,
            description: Optional[str] = None,
            parameters: dict = None
    ) -> Callable[[Callable[..., Awaitable[Any] | AsyncIterable[StreamEvent]]], Callable]:
        """
        A decorator to define a tool.
        Decorated function must be asynchronous and may return a value or yield StreamEvent(s).

        .. code-block:: python
            @tool_unit.tool()
            async def add(a: int, b: int):
                \"\"\"Add two numbers together\"\"\"
                return a + b


        :param name: The name of the tool presented to the llm. Defaults to the function name.
        :param description: The description of the tool presented to the llm. Defaults to the function docstring.
        :param parameters: Json schema object to present to the llm. Default built from function signature using Pydantic.
        :return: A decorator
        """

        def decorator(fn: Callable[..., Awaitable[Any] | AsyncIterable[StreamEvent]]):
            name_ = name or fn.__name__
            if cls._is_locked():
                cls._state().tools[1].append(_ToolDefinition(name_, description, parameters, fn))
            else:
                cls._state().tools[0].append(_ToolDefinition(name_, description, parameters, fn))
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

    @classmethod
    def _state(cls) -> _ToolBuilderState:
        if not hasattr(cls, "_state_attr"):
            setattr(cls, "_state_attr", _ToolBuilderState(
                dynamic_contracts=[],
                tools=([], []),
            ))
        return cls._state_attr

    @classmethod
    def _is_locked(cls) -> bool:
        return getattr(cls, "_lock", False)

    @classmethod
    @contextmanager
    def _locked(cls):
        if cls._is_locked():
            raise ValueError("Cannot define tools while building tools")
        setattr(type(cls), "_lock", True)
        try:
            yield
        finally:
            setattr(type(cls), "_lock", False)

    async def build_tools(self, call_context: CallContext) -> List[FnHandler]:
        with self._locked():
            try:
                for builder in self._state().dynamic_contracts:
                    sig = inspect.signature(builder)
                    has_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
                    kwargs = {}
                    if has_kwargs or 'spec' in sig.parameters:
                        kwargs["spec"] = self
                    if has_kwargs or "call_context" in sig.parameters:
                        kwargs["call_context"] = call_context
                    built = builder(**kwargs)
                    if inspect.isawaitable(built):
                        await built
            finally:
                tools: List[_ToolDefinition] = [*self._state().tools[0], *self._state().tools[1]]
                cast(list, self._state().tools[1]).clear()

            acc = []
            for tool in tools:
                # todo, logic to grab docs, input model, etc should happen when registering the tool, not when building
                sig = inspect.signature(tool.fn)
                has_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
                kwargs = {}
                if has_kwargs or 'spec' in sig.parameters:
                    kwargs["spec"] = self
                tool_fn = partial(tool.fn, **kwargs)
                acc.append(
                    FnHandler(
                        name=tool.name,
                        description=return_value(tool.description or tool.fn.__doc__ or f"Execute function {tool.name}"),
                        input_model_fn=return_value(tool.parameter or _model_from_sig(tool_fn)),
                        output_model_fn=_output_model_fn,
                        fn=lambda self, **kwargs: tool_fn(**kwargs),
                        extra=dict(title=tool.name),
                    )
                )
            return acc


def _output_model_fn(*args, **kwargs):
    raise NotImplementedError("output_model_fn not implemented")


def _model_from_sig(fn: callable) -> dict:
    sig = inspect.signature(fn)
    type_hints = get_type_hints(fn)

    fields = {}
    for param_name, param in sig.parameters.items():
        if param.kind == Parameter.VAR_POSITIONAL:
            raise ValueError("Cannot create a json schema from a function with *args")
        else:
            field_type = type_hints.get(param_name, None)
            if param.default is Parameter.empty:
                fields[param_name] = (field_type, ...)
            else:
                fields[param_name] = (field_type, param.default)

    return create_model(f"{fn.__name__.title()}Model", **fields)
