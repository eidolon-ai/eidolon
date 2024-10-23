import asyncio
from textwrap import dedent
from typing import TypeVar, Optional, Callable, Generic, Type, AsyncIterable, Tuple, List, Awaitable, Dict, Any

from pydantic import BaseModel

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.system.reference_model import Specable

T = TypeVar("T", bound=BaseModel)


class Agent(Generic[T], Specable[T]):
    _kind: str
    _spec_type: Type[T]
    _dynamic_contracts: List[Callable[[T], Awaitable[None]]]
    _actions: Dict[str, Tuple[str, Optional[str], Optional[str], List[str], Type[BaseModel], Type, bool, Callable[..., AsyncIterable[StreamEvent]]]]
    _create_process_hooks: List[Callable[[str], Awaitable[None]]]
    _delete_process_hooks: List[Callable[[str], Awaitable[None]]]
    _initialized: bool

    def __init__(self, kind: str, spec: Type[T]):
        self._kind = kind
        self._spec_type = spec
        self._dynamic_contracts = []
        self._actions = {}
        self._create_process_hooks = []
        self._delete_process_hooks = []
        self._initialized = False

    def __name__(self):
        return self._kind

    def dynamic_contract(self, fn: Callable[[T], Awaitable[None]]):
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
            if name_ in self._actions:
                raise ValueError(f"Action with name {name_} already exists")
            if not input_model:
                raise ValueError("todo: automatically generate input model from type signature")
            self._actions[name_] = (title, sub_title, description_, allowed_states_, input_model, output_model, custom_user_input_event, fn)
            return fn

        return decorator

    async def create_process_hook(self, fn: Callable[[str], Awaitable[None]]):
        """
        Registers a function to be called when a process is created.

        @agent.create_process_hook
        async def on_process_created(process_id: str):
            print(f"Process {process_id} created")
        """
        self._create_process_hooks.append(fn)
        return fn

    async def delete_process_hook(self, fn: Callable[[str], Awaitable[None]]):
        """
        Registers a function to be called when a process is deleted.

        @agent.delete_process_hook
        async def on_process_deleted(process_id: str):
            print(f"Process {process_id} deleted")
        """

        self._delete_process_hooks.append(fn)
        return fn

    async def __call__(_self, spec: T):  # Temporary wrapper for legacy mechanism for defining agents.
        if not _self._initialized:
            for builder in _self._dynamic_contracts:
                asyncio.run(builder(spec))
            _self._initialized = True

        class Translator(Specable[type[spec]]):
            def __name__(self):
                return _self._kind

            def __init__(self, spec):
                super().__init__(spec)
                for action_name, (title, sub_title, description, allowed_states, input_model, output_model, custom_user_input_event, fn) in _self._actions.items():
                    setattr(
                        self,
                        action_name,
                        register_action(
                            *allowed_states,
                            name=action_name,
                            title=title,
                            sub_title=sub_title,
                            description=lambda o, h: description,
                            input_model=lambda o, h: input_model,
                            output_model=lambda o, h: output_model,
                            custom_user_input_event=custom_user_input_event,
                        )(fn),
                    )

            async def create_process(self, process_id: str):
                for hook in _self._create_process_hooks:
                    await hook(process_id)

            async def delete_process(self, process_id: str):
                for hook in _self._delete_process_hooks:
                    await hook(process_id)

        return Translator(spec=spec)
