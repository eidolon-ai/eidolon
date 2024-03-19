from __future__ import annotations

import inspect
import typing
from dataclasses import dataclass

from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo


@dataclass
class FnHandler:
    name: str
    fn: callable
    description: typing.Callable[[object, FnHandler], str]
    input_model_fn: typing.Callable[[object, FnHandler], typing.Type[BaseModel]]
    output_model_fn: typing.Callable[[object, FnHandler], type]
    extra: dict


def register_handler(
    name: str = None,
    description: str | typing.Optional[typing.Callable[[object, FnHandler], str]] = None,
    input_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Type[BaseModel]]] = None,
    output_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Any]] = None,
    **extra,
):
    if isinstance(description, str):
        docs_fn = lambda fn: lambda self, handler: description  # noqa: E731
    elif description is None:
        docs_fn = lambda fn: lambda self, handler: fn.__doc__  # noqa: E731
    else:
        docs_fn = lambda fn: description  # noqa: E731
    return lambda fn: _add_handler(
        fn,
        FnHandler(
            name=name or fn.__name__,
            description=docs_fn(fn),
            fn=fn,
            input_model_fn=input_model or get_input_model,
            output_model_fn=output_model or get_output_model,
            extra=extra,
        ),
    )


def _add_handler(fn, handler):
    if not (inspect.iscoroutinefunction(fn) or inspect.isasyncgenfunction(fn)):
        raise ValueError("Handler must be an async function")
    try:
        handlers = getattr(fn, "eidolon_handlers")
    except AttributeError:
        handlers = []
        setattr(fn, "eidolon_handlers", handlers)
    handlers.append(handler)
    return fn


def get_input_model(_obj, handler: FnHandler) -> typing.Type[BaseModel]:
    sig = inspect.signature(handler.fn).parameters
    hints = typing.get_type_hints(handler.fn, include_extras=True)
    fields = {}
    for param, hint in filter(lambda tu: tu[0] != "return", hints.items()):
        if hasattr(hint, "__metadata__") and isinstance(hint.__metadata__[0], FieldInfo):
            field: FieldInfo = hint.__metadata__[0]
            if getattr(sig[param].default, "__name__", None) != "_empty":
                field.default = sig[param].default
            fields[param] = (hint.__origin__, field)
        elif isinstance(sig[param].default, FieldInfo):
            fields[param] = (hint, sig[param].default)
        else:
            # _empty default isn't being handled by create_model properly (still optional when it should be required)
            field = (
                Field()
                if getattr(sig[param].default, "__name__", None) == "_empty"
                else Field(default=sig[param].default)
            )
            fields[param] = (hint, field)
    input_model = create_model(
        f"{handler.name.capitalize()}InputModel", **fields, __config__=dict(arbitrary_types_allowed=True)
    )
    return input_model


def get_output_model(_obj, handler: FnHandler):
    return typing.get_type_hints(handler.fn, include_extras=True).get("return", typing.Any)


def get_handlers(obj) -> typing.List[FnHandler]:
    acc = []
    for name in dir(obj):
        if hasattr(getattr(obj, name), "eidolon_handlers"):
            acc.extend(getattr(getattr(obj, name), "eidolon_handlers"))
    return acc
