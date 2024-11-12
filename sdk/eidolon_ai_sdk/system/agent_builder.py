import copy
import inspect
from collections import namedtuple
from contextlib import contextmanager
from textwrap import dedent
from typing import TypeVar, Optional, Callable, Type, AsyncIterable, List, Awaitable, Any, Dict

from pydantic import BaseModel, Field

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.apu.agents_logic_unit import AgentsLogicUnit
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.apu.logic_unit import LogicUnit
from eidolon_ai_sdk.system.fn_handler import get_input_model, get_output_model, FnHandler
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Reference
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.class_utils import fqn
from eidolon_ai_sdk.util.partial import partial, return_value

T = TypeVar("T", bound=BaseModel)


_ActionState = namedtuple("_ActionState", ["name", "title", "sub_title", "description", "allowed_states", "input_model", "output_model", "custom_user_input_event", "fn"])
_AgentState = namedtuple("_AgentState", ["dynamic_contracts", "actions"])


class AgentBuilderBase(BaseModel):
    _metadata: Metadata = None
    _handlers: List[FnHandler] = None

    @classmethod
    def dynamic_contract(cls, fn: Callable[[T, Metadata], Awaitable[None] | None]):
        """
        A decorator used to build an agent template dynamically based on the spec and metadata.
        Decorated function may be synchronous or asynchronous.

        @agent.dynamic_contract
        async def fn(spec: MySpec, metadata: Metadata):
            @agent.action(description=spec.description)
            async def my_action(process_id):
                thread = await spec.apu_instance().main_thread(process_id)
                yield StringOutputEvent(content="Hmm, let me think about that...")
                async for event in thread.stream_request(...)
                    yield event
                yield AgentStateEvent(state="idle")
        """
        if cls._is_locked():
            raise ValueError("Cannot nest dynamic contracts")
        cls._state().dynamic_contracts.append(fn)
        return fn

    @classmethod
    def action(
            cls,
            name: Optional[str] = None,
            title: Optional[str] = None,
            sub_title: Optional[str] = None,
            description: Optional[str] = None,
            allowed_states: List[str] = None,
            input_model: Optional[Type[BaseModel]] = None,
            output_model: Type = Any,
            custom_user_input_event: bool = False,
            partials: Dict[str, Any] = None
    ) -> Callable[[Callable[..., Awaitable[Any] | AsyncIterable[StreamEvent]]], Callable]:
        """
        A decorator to registers an action with the agent.
        Decorated function must be asynchronous and may return a value or yield StreamEvent(s).

        @agent.action(description="This is my action")
        def my_action(process_id):
            thread = await spec.apu_instance().main_thread(process_id)
            yield StringOutputEvent(content="Hmm, let me think about that...")
            async for event in thread.stream_request(...)
                yield event
            yield AgentStateEvent(state="idle")

        :param name: Name of the action. If not provided, the name of the function will be used.
        :param title: Title of the action for openapi documentation
        :param sub_title: Subtitle of the action for openapi documentation
        :param description: Description of the action for openapi documentation
        :param allowed_states: Allowed states the action can process. Default is ["initialized"]
        :param input_model: Override the input model for the action. If not provided, the input model will be generated from the function signature.
        :param output_model: Override the output model for the action. If not provided, the output model will be Any.
        :param custom_user_input_event: Does the action return a custom user input event? Default is False.
        :param partials: A dictionary of partials to pass to the action. Helpful to keep arguments out of API definition.
        """

        def decorator(fn: Callable[..., AsyncIterable[StreamEvent]]):
            fn = partial(fn, **(partials or {}))
            name_ = name or fn.__name__
            description_ = description or dedent(fn.__doc__ or "").strip() or None
            allowed_states_ = allowed_states or ["initialized"]
            if name_ in cls._state().actions[0] or name_ in cls._state().actions[1]:
                raise ValueError(f"Action with name {name_} already exists")

            actions = cls._state().actions[1] if cls._is_locked() else cls._state().actions[0]
            actions.append(_ActionState(name_, title, sub_title, description_, allowed_states_, input_model, output_model, custom_user_input_event, fn))
            return fn

        return decorator

    async def create_process(self, process_id: str) -> None:
        """
        A function called when a process is created.
        """
        pass

    @classmethod
    async def delete_process(cls, process_id: str) -> None:
        """
        A function to be called when a process is deleted.
        """
        pass

    @classmethod
    def _is_locked(cls) -> bool:
        return getattr(cls, "_lock", False)

    @classmethod
    @contextmanager
    def _locked(cls):
        if cls._is_locked():
            raise ValueError("Cannot define tools while building tools")
        setattr(type(cls), "_lock", True)
        try:
            yield
        finally:
            setattr(type(cls), "_lock", False)

    def set_metadata(self, metadata: Metadata):
        self._metadata = metadata

    @classmethod
    def _state(cls):
        if not hasattr(cls, "_state_attr"):
            cls._state_attr = _AgentState(
                dynamic_contracts=[],
                actions=([], []),
            )
        return cls._state_attr

    async def start(self):
        with self._locked():
            state = self._state()
            try:
                for builder in state.dynamic_contracts:
                    sig = inspect.signature(builder)
                    has_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
                    kwargs = {}
                    if has_kwargs or 'spec' in sig.parameters:
                        kwargs["spec"] = self
                    if has_kwargs or "metadata" in sig.parameters:
                        kwargs["metadata"] = self._metadata
                    built = builder(**kwargs)
                    if inspect.isawaitable(built):
                        await built
            finally:
                actions: List[_ActionState] = [*state.actions[0], *state.actions[1]]
                state.actions[1].clear()

        handlers_acc = []
        for action in actions:
            sig = inspect.signature(action.fn)
            has_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
            kwargs = {}
            if has_kwargs or 'spec' in sig.parameters:
                kwargs["spec"] = self
            if has_kwargs or "metadata" in sig.parameters:
                kwargs["metadata"] = self._metadata
            if not inspect.iscoroutinefunction(action.fn) and not inspect.isasyncgenfunction(action.fn):
                raise ValueError("action must be an async function")
            if hasattr(self, action.name):
                logger.warning(f"Action with name {action.name} already exists, overwriting...")
            handlers_acc.append(FnHandler(
                name=action.name,
                fn=partial(action.fn, **kwargs),
                description=return_value(action.description or action.fn.__doc__),
                input_model_fn=return_value(action.input_model) if action.input_model else get_input_model,
                output_model_fn=return_value(action.output_model) if action.output_model else get_output_model,
                extra=dict(
                    allowed_states=action.allowed_states,
                    custom_user_input_event=action.custom_user_input_event,
                    title=action.title,
                    sub_title=action.sub_title,
                ),
            ))
        self._handlers = handlers_acc

    async def get_handlers(self) -> List[FnHandler]:
        return self._handlers


class AgentBuilder(AgentBuilderBase):
    apu: AnnotatedReference[APU]
    agent_refs: List[str] = Field(
        default=[],
        description="A list of agents this agent can communicate with. Agents are referenced by name (metadata.name)."
    )
    tools: List[Reference[LogicUnit]] = Field(
        default=[],
        description="A list of [tools](https://www.eidolonai.com/docs/components/logicunit/overview) available to the agent.")

    def apu_instance(self) -> APU:
        logic_units = copy.copy(self.tools) if self.tools else []
        if self.agent_refs:
            logic_units.append(Reference(
                implementation=fqn(AgentsLogicUnit),
                agents=self.agent_refs,
            ))
        apu = copy.deepcopy(self.apu)
        if logic_units:
            apu.setdefault('logic_units', []).extend(logic_units)
        return apu.instantiate()
