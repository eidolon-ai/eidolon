from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Dict, List

from .agent_program import AgentProgram


class Agent:
    agent_program: AgentProgram
    handlers: Dict[str, EidolonHandler]

    def __init__(self, agent_program: AgentProgram):
        self.agent_program = agent_program
        self.handlers = {handler.state: handler for handler in (
            getattr(getattr(self, method_name), 'eidolon_handler') for method_name in dir(self) if hasattr(getattr(self, method_name), 'eidolon_handler')
        )}


class CodeAgent(Agent):
    pass


@dataclass
class EidolonHandler:
    state: str
    transition_to: List[str]
    fn: callable


def register(state: str = 'idle', transition_to: List[str] = None):
    if state == 'terminated':
        raise ValueError("Cannot register a handler for the terminated state")

    def decorator(fn):
        if not inspect.iscoroutinefunction(fn):
            # todo, we need to support both async and normal functions to make people's lives easier
            raise ValueError("Handler must be an async function")

        setattr(fn, "eidolon_handler",
                EidolonHandler(state=state, transition_to=transition_to or ['terminated'], fn=fn))
        return fn

    return decorator
