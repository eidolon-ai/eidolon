from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Dict, List, TypeVar, Generic, Any

from pydantic import BaseModel

from .agent_memory import AgentMemory
from .agent_program import AgentProgram


class Agent:
    agent_program: AgentProgram
    action_handlers: Dict[str, EidolonHandler]
    agent_memory: AgentMemory

    def __init__(self, agent_program: AgentProgram, agent_memory: AgentMemory):
        self.agent_program = agent_program
        self.agent_memory = agent_memory
        self.action_handlers = {
            handler.name: handler
            for method_name in dir(self) if hasattr(getattr(self, method_name), 'eidolon_handlers')
            for handler in getattr(getattr(self, method_name), 'eidolon_handlers')
        }


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
