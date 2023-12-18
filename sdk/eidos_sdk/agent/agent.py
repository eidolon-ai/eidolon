from __future__ import annotations

import typing
from typing import List, TypeVar, Generic

from pydantic import BaseModel

from eidos_sdk.cpu.agent_cpu import AgentCPU
from eidos_sdk.cpu.conversational_agent_cpu import ConversationalAgentCPU
from eidos_sdk.cpu.conversational_logic_unit import (
    ConversationalLogicUnit,
    ConversationalSpec,
)
from eidos_sdk.system.eidos_handler import EidosHandler, register_handler
from eidos_sdk.system.reference_model import Specable, AnnotatedReference


class ProcessContext(BaseModel):
    process_id: str
    callback_url: typing.Optional[str]


class AgentSpec(BaseModel):
    cpu: AnnotatedReference[AgentCPU, ConversationalAgentCPU]
    agent_refs: List[str] = []


class Agent(Specable[AgentSpec]):
    cpu: AgentCPU

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cpu = self.spec.cpu.instantiate()
        if self.spec.agent_refs and hasattr(self.cpu, "logic_units"):
            self.cpu.logic_units.append(
                ConversationalLogicUnit(
                    processing_unit_locator=self.cpu,
                    spec=ConversationalSpec(agents=self.spec.agent_refs),
                )
            )


def register_program(
    name: typing.Optional[typing.Callable[[object, EidosHandler], str]] = None,
    description: typing.Optional[typing.Callable[[object, EidosHandler], str]] = None,
    input_model: typing.Optional[typing.Callable[[object, EidosHandler], typing.Type[BaseModel]]] = None,
    output_model: typing.Optional[typing.Callable[[object, EidosHandler], typing.Any]] = None,
):
    return register_handler(
        name=name,
        description=description,
        input_model=input_model,
        output_model=output_model,
        type="program",
    )


def register_action(
    *allowed_states: str,
    name: str = None,
    description: typing.Optional[typing.Callable[[object, EidosHandler], str]] = None,
    input_model: typing.Optional[typing.Callable[[object, EidosHandler], BaseModel]] = None,
    output_model: typing.Optional[typing.Callable[[object, EidosHandler], typing.Any]] = None,
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
        type="action",
    )


T = TypeVar("T")


class AgentState(BaseModel, Generic[T]):
    name: str
    data: T
