import copy
import inspect
import types
from collections import namedtuple
from functools import wraps
from textwrap import dedent
from typing import TypeVar, Optional, Callable, Generic, Type, AsyncIterable, Tuple, List, Awaitable, Dict, Any

import sys
from pydantic import BaseModel, Field

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.apu.agents_logic_unit import AgentsLogicUnit
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.apu.logic_unit import LogicUnit
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Reference
from eidolon_ai_sdk.system.specable import Specable
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn


class DefaultAgentSpec(BaseModel):
    apu: AnnotatedReference[APU]
    references: List[str | Reference[LogicUnit]] = Field(
        default_factory=list,
        description="A list of references available to the agent. References can be another agent's name, or the definition of a [logic unit](https://www.eidolonai.com/docs/components/logicunit/overview).")

    def apu_instance(self) -> APU:
        logic_units = [r for r in self.references if isinstance(r, Reference)]
        agent_refs = [r for r in self.references if isinstance(r, str)]
        if agent_refs:
            logic_units.append(Reference(
                implementation=fqn(AgentsLogicUnit),
                agents=agent_refs,
            ))
        apu = copy.deepcopy(self.apu)
        apu.logic_units.extend(logic_units)
        return apu.instantiate()


T = TypeVar("T", bound=BaseModel)


_ActionState = namedtuple("_ActionState", ["title", "sub_title", "description", "allowed_states", "input_model", "output_model", "custom_user_input_event", "fn"])


class Agent(Generic[T]):
    _spec_type: Type[T]
    _dynamic_contracts: List[Callable[[T, Metadata], Awaitable[None] | None]]
    _actions: Tuple[Dict[str, _ActionState], Dict[str, _ActionState]]
    _create_process_hooks: Tuple[List[Callable[[str], Awaitable[None]]], List[Callable[[str], Awaitable[None]]]]
    _delete_process_hooks: List[Callable[[str], Awaitable[None]]]
    _initialized: bool

    def __init__(self, spec_type: Type[T] = DefaultAgentSpec):
        self._spec_type = spec_type
        self._dynamic_contracts = []
        self._actions = ({}, {})
        self._create_process_hooks = ([], [])
        self._delete_process_hooks = []
        self._locked = False
        self._specable = None

    def dynamic_contract(self, fn: Callable[[T, Metadata], Awaitable[None] | None]):
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
    ) -> Callable[[Callable[..., AsyncIterable[StreamEvent]]], Any]:
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
        self._delete_process_hooks.append(fn)
        return fn

    def _reset(self):
        self._actions[1].clear()
        self._create_process_hooks[1].clear()

    # Logic written to wrap legacy agent definition mechanism. We can remove this after ripping out the old mechanism.
    def specable(_self, name="AgentImpl"):  # Temporary wrapper for legacy mechanism for defining agents.
        if not _self._specable:
            _self._locked = True

            def __init__(self, spec: T, metadata: Metadata):
                self.spec = spec
                self.startup_tasks = []

                _self._reset()
                for builder in _self._dynamic_contracts:
                    sig = inspect.signature(builder)
                    has_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
                    kwargs = {}
                    if has_kwargs or 'spec' in sig.parameters:
                        kwargs["spec"] = spec
                    if has_kwargs or "metadata" in sig.parameters:
                        kwargs["metadata"] = metadata
                    built = builder(**kwargs)
                    if inspect.isawaitable(built):
                        self.startup_tasks.append(built)

                self.create_process_hooks = [*_self._create_process_hooks[0], *_self._create_process_hooks[1]]

                for action_name, (title, sub_title, description, allowed_states, input_model, output_model, custom_user_input_event, fn) in dict(**_self._actions[0], **_self._actions[1]).items():
                    sig = inspect.signature(fn)
                    has_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
                    kwargs = {}
                    if has_kwargs or 'spec' in sig.parameters:
                        kwargs["spec"] = spec
                    if has_kwargs or "metadata" in sig.parameters:
                        kwargs["metadata"] = metadata
                    setattr(
                        self,
                        action_name,
                        register_action(
                            *allowed_states,
                            name=action_name,
                            title=title,
                            sub_title=sub_title,
                            description=(lambda o, h, d=description: d) if description else None,
                            input_model=(lambda o, h, i=input_model: i) if input_model else None,
                            output_model=(lambda o, h, om=output_model: om) if output_model else None,
                            custom_user_input_event=custom_user_input_event,
                        )(partial(fn, **kwargs)),
                    )

            async def create_process(self, process_id: str):
                for hook in self.create_process_hooks:
                    await hook(process_id)

            @classmethod
            async def delete_process(cls, process_id: str):
                for hook in _self._delete_process_hooks:
                    await hook(process_id)

            async def start(self):
                for task in self.startup_tasks:
                    await task

            new_class = types.new_class(
                name,
                (Specable[_self._spec_type],),
                {},
                lambda ns: ns.update({
                    "__init__": __init__,
                    "create_process": create_process,
                    "delete_process": delete_process,
                    "start": start,
                    "built_with_agent_builder": True,
                })
            )
            _self._specable = new_class

        return _self._specable


#  funktools partial does not preserve the signature of the function it wraps, so we need to do it manually
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
        raise ValueError("Handler must be an async function")

    sig = inspect.signature(fn)
    parameters = [param for name, param in sig.parameters.items() if name not in partial_kwargs]
    wrapper.__signature__ = sig.replace(parameters=parameters, return_annotation=sig.return_annotation)
    wrapper.__annotations__ = {k: v for k, v in fn.__annotations__.items() if k not in partial_kwargs}

    return wrapper

