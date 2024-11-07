from __future__ import annotations

import typing
from pydantic import BaseModel
from typing import TypeVar, Generic

from eidolon_ai_sdk.system.fn_handler import FnHandler, register_handler


def register_program(
    name: typing.Optional[str] = None,
    title: typing.Optional[str] = None,
    sub_title: typing.Optional[str] = None,
    description: typing.Optional[typing.Callable[[object, FnHandler], str] | str] = None,
    input_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Type[BaseModel]]] = None,
    output_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Any]] = None,
):
    extra = {}
    if title:
        extra["title"] = title
    if sub_title:
        extra["sub_title"] = sub_title
    return register_handler(
        name=name,
        description=description,
        input_model=input_model,
        output_model=output_model,
        allowed_states=["initialized"],
        **extra
    )


def register_action(
    *allowed_states: str,
    name: str = None,
    title: typing.Optional[str] = None,
    sub_title: typing.Optional[str] = None,
    description: typing.Optional[typing.Callable[[object, FnHandler], str]] = None,
    input_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Type[BaseModel]]] = None,
    output_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Any]] = None,
    custom_user_input_event: bool = False,
    **extra,
):
    if not allowed_states:
        raise ValueError("Must specify at least one valid state")
    if "terminated" in allowed_states:
        raise ValueError("Action cannot transform terminated state")

    if title:
        extra["title"] = title
    if sub_title:
        extra["sub_title"] = sub_title

    return register_handler(
        name=name,
        description=description,
        input_model=input_model,
        output_model=output_model,
        allowed_states=allowed_states,
        custom_user_input_event=custom_user_input_event,
        **extra,
    )


T = TypeVar("T")


class AgentState(BaseModel, Generic[T]):
    name: str
    data: T
