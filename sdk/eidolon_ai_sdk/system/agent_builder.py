import inspect
import types
from textwrap import dedent
from typing import TypeVar, Optional, Callable, Generic, Type, AsyncIterable, Tuple, List, Awaitable, Dict, Any

import sys
from pydantic import BaseModel

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.system.resources.resources_base import Metadata

T = TypeVar("T", bound=BaseModel)


class Agent(Generic[T]):
    _kind: str
    _spec_type: Type[T]
    _dynamic_contracts: List[Callable[[T, Metadata], Awaitable[None] | None]]
    _actions: Tuple[Dict[str, Tuple[str, Optional[str], Optional[str], List[str], Type[BaseModel], Type, bool, Callable[..., AsyncIterable[StreamEvent]]]], Dict[str, Tuple[str, Optional[str], Optional[str], List[str], Type[BaseModel], Type, bool, Callable[..., AsyncIterable[StreamEvent]]]]]
    _create_process_hooks: Tuple[List[Callable[[str], Awaitable[None]]], List[Callable[[str], Awaitable[None]]]]
    _delete_process_hooks: Tuple[List[Callable[[str], Awaitable[None]]], List[Callable[[str], Awaitable[None]]]]
    _initialized: bool

    def __init__(self, kind: str, spec: Type[T]):
        self._kind = kind
        self._spec_type = spec
        self._dynamic_contracts = []
        self._actions = ({}, {})
        self._create_process_hooks = ([], [])
        self._delete_process_hooks = ([], [])
        self._locked = False
        self._specable = None

    @property
    def __name__(self):
        return self._kind

    def dynamic_contract(self, fn: Callable[[T], Awaitable[None] | None]):
        if self._locked:
            raise ValueError("Cannot add dynamic contracts after agent has been initialized")
        self._dynamic_contracts.append(fn)
        return fn

    def action(
            self,
            name: Optional[str] = None,
            title: Optional[str] = None,
            sub_title: Optional[str] = None,
            description: Optional[str] = None,
            allowed_states: List[str] = None,
            input_model: Optional[Type[BaseModel]] = None,
            output_model: Type = Any,
            custom_user_input_event: bool = False,
    ) -> Callable[[Callable[..., AsyncIterable[StreamEvent]]], ...]:
        """
        Registers an action with the agent.

        @agent.action(description="This is my action")
        async def my_action(self, input: MyInputModel) -> MyOutputModel:
            yield StringOutputEvent(content="Here is your output!")
            yield AgentStateEvent(state="idle")

        :param name: Name of the action. If not provided, the name of the function will be used.
        :param title: Title of the action for openapi documentation
        :param sub_title: Subtitle of the action for openapi documentation
        :param description: Description of the action for openapi documentation
        :param allowed_states: Allowed states the action can process. Default is ["initialized"]
        :param input_model: Override the input model for the action. If not provided, the input model will be generated from the function signature.
        :param output_model: Override the output model for the action. If not provided, the output model will be Any.
        :param custom_user_input_event: Does the action return a custom user input event? Default is False.
        """

        def decorator(fn: Callable[..., AsyncIterable[StreamEvent]]):
            name_ = name or fn.__name__
            description_ = description or dedent(fn.__doc__ or "").strip() or None
            allowed_states_ = allowed_states or ["initialized"]
            if name_ in self._actions[0] or name_ in self._actions[1]:
                raise ValueError(f"Action with name {name_} already exists")
            if not input_model:
                raise ValueError("todo: automatically generate input model from type signature")
            actions = self._actions[1] if self._locked else self._actions[0]
            actions[name_] = (title, sub_title, description_, allowed_states_, input_model, output_model, custom_user_input_event, fn)
            return fn

        return decorator

    def create_process_hook(self, fn: Callable[[str], Awaitable[None]]):
        """
        Registers a function to be called when a process is created.

        @agent.create_process_hook
        async def on_process_created(process_id: str):
            print(f"Process {process_id} created")
        """
        hooks = self._create_process_hooks[1] if self._locked else self._create_process_hooks[0]
        hooks.append(fn)
        return fn

    def delete_process_hook(self, fn: Callable[[str], Awaitable[None]]):
        """
        Registers a function to be called when a process is deleted.

        @agent.delete_process_hook
        async def on_process_deleted(process_id: str):
            print(f"Process {process_id} deleted")
        """
        hooks = self._delete_process_hooks[1] if self._locked else self._delete_process_hooks[0]
        hooks.append(fn)
        return fn

    def _reset(self):
        self._actions[1].clear()
        self._create_process_hooks[1].clear()
        self._delete_process_hooks[1].clear()

    # super fucked up logic written to transition support to Agent mechanism. todo, remove before merging
    def specable(_self):  # Temporary wrapper for legacy mechanism for defining agents.
        if not _self._specable:
            _self._locked = True

            def __init__(self, spec: T, metadata: Metadata):
                self.spec = spec
                self.startup_tasks = []

                _self._reset()
                for builder in _self._dynamic_contracts:
                    built = builder(spec, metadata)
                    if inspect.isawaitable(built):
                        self.startup_tasks.append(built)

                self.create_process_hooks = [*_self._create_process_hooks[0], *_self._create_process_hooks[1]]
                self.delete_process_hooks = [*_self._delete_process_hooks[0], *_self._delete_process_hooks[1]]

                for action_name, (title, sub_title, description, allowed_states, input_model, output_model, custom_user_input_event, fn) in dict(**_self._actions[0], **_self._actions[1]).items():
                    def _build(_fn):
                        async def _fn_wrap(self, process_id, **kwargs):
                            async for e in _fn(process_id, **kwargs):
                                yield e
                        return _fn_wrap

                    setattr(
                        self,
                        action_name,
                        register_action(
                            *allowed_states,
                            name=action_name,
                            title=title,
                            sub_title=sub_title,
                            description=lambda o, h, d=description: d,
                            input_model=lambda o, h, i=input_model: i,
                            output_model=lambda o, h, om=output_model: om,
                            custom_user_input_event=custom_user_input_event,
                        )(_build(fn)),
                    )

            async def create_process(self, process_id: str):
                for hook in self.create_process_hooks:
                    await hook(process_id)

            async def delete_process(self, process_id: str):
                for hook in self.delete_process_hooks:
                    await hook(process_id)

            async def start(self):
                for task in self.startup_tasks:
                    await task

            # Create registry module
            if _self._kind in sys.modules[__name__].__dict__:
                raise ValueError(f"Agent with name {_self._kind} already exists")

            # Create metaclass that handles init_subclass without kwargs
            class NoKwargsMeta(type):
                @classmethod
                def __prepare__(metacls, name, bases, **kwds):
                    return {}

                def __new__(metacls, name, bases, namespace, **kwds):
                    return super().__new__(metacls, name, bases, namespace)

                def __init__(cls, name, bases, namespace, **kwds):
                    super().__init__(name, bases, namespace)

            new_class = types.new_class(
                _self._kind,
                (Specable[_self._spec_type],),
                {"__module__": __name__, "metaclass": NoKwargsMeta},
                lambda ns: ns.update({
                    "__init__": __init__,
                    "create_process": create_process,
                    "delete_process": delete_process,
                    "start": start,
                    "built_with_agent_builder": True,
                })
            )

            setattr(sys.modules[__name__], _self._kind, new_class)
            _self._specable = new_class

        return _self._specable
