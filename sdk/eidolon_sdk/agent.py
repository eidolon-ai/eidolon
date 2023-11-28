from __future__ import annotations

import contextvars
import inspect
import typing
from asyncio import Future
from dataclasses import dataclass
from typing import Dict, List, TypeVar, Generic

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

from .agent_memory import AgentMemory
from .cpu.agent_cpu import AgentCPU, ResponseHandler
from .cpu.agent_io import UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage


class ProcessContext(BaseModel):
    process_id: str
    callback_url: typing.Optional[str]


class AgentResponseHandler(ResponseHandler):
    def __init__(self):
        self.listeners = {}

    async def handle(self, ret_p_id: str, response: Dict[str, typing.Any]):
        try:
            self.listeners[ret_p_id].set_result(response)
        except KeyError:
            pass

    def add_listener(self, ret_p_id: str) -> Future:
        future = Future()
        self.listeners[ret_p_id] = future
        return future


class Agent:
    cpu_response_handler: AgentResponseHandler
    action_handlers: Dict[str, EidolonHandler]
    agent_machine: AgentMemory
    process_context: contextvars.ContextVar
    cpu: AgentCPU

    def __init__(self, agent_machine: 'AgentMachine', cpu: AgentCPU, spec=None):
        self.cpu = cpu
        self.spec = spec
        self.agent_memory = agent_machine.agent_memory
        self.agent_machine = agent_machine
        self.action_handlers = {
            handler.name: handler
            for method_name in dir(self) if hasattr(getattr(self, method_name), 'eidolon_handlers')
            for handler in getattr(getattr(self, method_name), 'eidolon_handlers')
        }
        self.process_context = contextvars.ContextVar('process_state', default=None)
        self.cpu_response_handler = AgentResponseHandler()

    def get_context(self) -> ProcessContext:
        return self.process_context.get()

    def get_input_model(self, action):
        sig = inspect.signature(self.action_handlers[action].fn).parameters
        hints = typing.get_type_hints(self.action_handlers[action].fn, include_extras=True)
        fields = {}
        for param, hint in filter(lambda tu: tu[0] != 'return', hints.items()):
            if hasattr(hint, '__metadata__') and isinstance(hint.__metadata__[0], FieldInfo):
                field: FieldInfo = hint.__metadata__[0]
                field.default = sig[param].default
                fields[param] = (hint.__origin__, field)
            else:
                # _empty default isn't being handled by create_model properly (still optional when it should be required)
                default = ... if getattr(sig[param].default, "__name__", None) == '_empty' else sig[param].default
                fields[param] = (hint, default)

        input_model = create_model(f'{action.capitalize()}InputModel', **fields)
        return input_model

    def get_response_model(self, action: str):
        return typing.get_type_hints(self.action_handlers[action].fn, include_extras=True).get('return', typing.Any)

    async def cpu_request(
            self,
            prompts: List[typing.Union[UserTextCPUMessage, ImageURLCPUMessage, SystemCPUMessage]],
            input_data: Dict[str, typing.Any] = None,
            output_format: Dict[str, typing.Any] = None,
    ):
        return await self.cpu.schedule_request(
            self.get_context().process_id, prompts,
            input_data or {},
            output_format or dict(type="str")
        )


class CodeAgent(Agent):
    pass


@dataclass
class EidolonHandler:
    name: str
    allowed_states: List[str]
    fn: callable


def initializer(fn):
    return _add_handler(fn, EidolonHandler(name='INIT', allowed_states=['UNINITIALIZED'], fn=fn))


def register_action(*allowed_states: str, name: str = None):
    if not allowed_states:
        raise ValueError("Must specify at least one valid state")
    if 'terminated' in allowed_states:
        raise ValueError("Action cannot transform terminated state")

    return lambda fn: _add_handler(fn, EidolonHandler(name=name or fn.__name__, allowed_states=list(allowed_states), fn=fn))


def _add_handler(fn, handler):
    if not inspect.iscoroutinefunction(fn):
        raise ValueError("Handler must be an async function")
    try:
        handlers = getattr(fn, "eidolon_handlers")
    except AttributeError:
        handlers = []
        setattr(fn, "eidolon_handlers", handlers)
    handlers.append(handler)
    return fn


T = TypeVar('T')


class AgentState(BaseModel, Generic[T]):
    name: str
    data: T
