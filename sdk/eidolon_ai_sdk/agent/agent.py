from __future__ import annotations

import typing
from pydantic import BaseModel
from typing import List, TypeVar, Generic

from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.apu.agents_logic_unit import (
    AgentsLogicUnit,
    AgentsLogicUnitSpec,
)
from eidolon_ai_sdk.system.fn_handler import FnHandler, register_handler
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference


class AgentSpec(BaseModel):
    apu: AnnotatedReference[APU]
    agent_refs: List[str] = []


class Agent(Specable[AgentSpec]):
    apu: APU

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apu = self.spec.apu.instantiate()
        if self.spec.agent_refs and hasattr(self.apu, "logic_units"):
            self.apu.logic_units.append(
                AgentsLogicUnit(
                    processing_unit_locator=self.apu,
                    spec=AgentsLogicUnitSpec(agents=self.spec.agent_refs),
                )
            )


def register_program(
    name: typing.Optional[typing.Callable[[object, FnHandler], str]] = None,
    description: typing.Optional[typing.Callable[[object, FnHandler], str]] = None,
    input_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Type[BaseModel]]] = None,
    output_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Any]] = None,
):
    return register_handler(
        name=name,
        description=description,
        input_model=input_model,
        output_model=output_model,
        allowed_states=["initialized"],
    )


def register_action(
    *allowed_states: str,
    name: str = None,
    description: typing.Optional[typing.Callable[[object, FnHandler], str]] = None,
    input_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Type[BaseModel]]] = None,
    output_model: typing.Optional[typing.Callable[[object, FnHandler], typing.Any]] = None,
    **extra,
):
    if not allowed_states:
        raise ValueError("Must specify at least one valid state")
    if "terminated" in allowed_states:
        raise ValueError("Action cannot transform terminated state")

    return register_handler(
        name=name,
        description=description,
        input_model=input_model,
        output_model=output_model,
        allowed_states=allowed_states,
        **extra,
    )


T = TypeVar("T")


class AgentState(BaseModel, Generic[T]):
    name: str
    data: T
