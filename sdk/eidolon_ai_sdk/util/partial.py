import inspect
import typing
from functools import wraps
from typing import TypeVar


#  functools partial does not preserve the signature of the function it wraps, so we need to do it manually
def partial(fn, **partial_kwargs):
    if inspect.iscoroutinefunction(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            merged_kwargs = {**partial_kwargs, **kwargs}
            return await fn(*args, **merged_kwargs)
    elif inspect.isasyncgenfunction(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            merged_kwargs = {**partial_kwargs, **kwargs}
            async for item in fn(*args, **merged_kwargs):
                yield item
    else:
        def wrapper(*args, **kwargs):
            merged_kwargs = {**partial_kwargs, **kwargs}
            return fn(*args, **merged_kwargs)

    sig = inspect.signature(fn)
    parameters = [param for name, param in sig.parameters.items() if name not in partial_kwargs]
    wrapper.__signature__ = sig.replace(parameters=parameters, return_annotation=sig.return_annotation)
    wrapper.__annotations__ = {k: v for k, v in fn.__annotations__.items() if k not in partial_kwargs}

    return wrapper


T = TypeVar("T")


def return_value(value: T) -> typing.Callable[[typing.Any, typing.Any], T]:
    return lambda *args, **kwargs: value
