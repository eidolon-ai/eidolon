from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional, Union, Dict, Any, Type

from jinja2 import Environment, meta, StrictUndefined
from openai import BaseModel
from pydantic import model_validator, field_validator
from pydantic_core import to_jsonable_python

from eidolon_ai_sdk.agent.agent import AgentSpec, Agent, AgentState, register_action
from eidolon_ai_sdk.cpu.agent_io import SystemCPUMessage, ImageCPUMessage, UserTextCPUMessage
from eidolon_ai_sdk.io.events import AgentStateEvent
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class ActionDefinition(BaseModel):
    name: str = "converse"
    description: Optional[str] = None
    user_prompt: str = "{{ statement }}"
    input_schema: dict = None
    output_schema: Union[Literal["str"], Dict[str, Any]] = "str"
    files: Literal["disable", "single-optional", "single", "multiple"] = "disable"
    allowed_states: List[str] = ["initialized", "idle", "http_error"]
    output_state: str = "idle"

    @model_validator(mode="after")
    def _set_input_schema_default(self):
        if self.input_schema is None:
            env = Environment()
            user_vars = meta.find_undeclared_variables(env.parse(self.user_prompt))
            self.input_schema = {v: dict(type="string") for v in user_vars if v != "datetime_iso"}
        return self

    @field_validator("input_schema")
    def validate_prompt_properties(cls, input_dict):
        if not isinstance(input_dict, dict):
            raise ValueError("prompt_properties must be a dict")
        for k, v in input_dict.items():
            if isinstance(v, dict):
                if v.get("format") == "binary":
                    raise ValueError(
                        "prompt_properties cannot contain format = 'binary' fields. Use the files option instead"
                    )
        return input_dict


class SimpleAgentSpec(AgentSpec):
    description: Optional[str] = None
    system_prompt: str = "You are a helpful assistant"
    actions: List[ActionDefinition] = [ActionDefinition()]


class SimpleAgent(Agent, Specable[SimpleAgentSpec]):
    def __init__(self, spec):
        super().__init__(spec=spec)
        for action in self.spec.actions:
            setattr(
                self,
                action.name,
                register_action(
                    *action.allowed_states,
                    name=action.name,
                    input_model=_make_input_schema(action),
                    output_model=_make_output_schema(action),
                    description=action.description,
                )(self._act_wrapper(action)),
            )

    async def create_process(self, process_id):
        t = await self.cpu.main_thread(process_id)
        await t.set_boot_messages(prompts=[SystemCPUMessage(prompt=self.spec.system_prompt)])

    @staticmethod
    def _act_wrapper(action):
        async def fn(self, process_id, **kwargs):
            async for e in SimpleAgent._act(self, action, process_id, **kwargs):
                yield e

        return fn

    async def _act(self, action: ActionDefinition, process_id, **kwargs) -> AgentState[Any]:
        body = dict(datetime_iso=datetime.now().isoformat())
        body.update(kwargs.get("body") or {})
        body = to_jsonable_python(body)

        files = kwargs.get("file", [])
        files = files if isinstance(files, list) else [files]
        image_messages = [ImageCPUMessage(image=file.file, prompt=file.filename) for file in files if file]

        env = Environment(undefined=StrictUndefined)
        text_message = UserTextCPUMessage(prompt=env.from_string(action.user_prompt).render(**body))

        thread = await self.cpu.main_thread(process_id)
        response = thread.stream_request(output_format=action.output_schema, prompts=[*image_messages, text_message])

        async for event in response:
            yield event
        yield AgentStateEvent(state=action.output_state)


def _make_input_schema(action: ActionDefinition):
    def fn(agent: object, handler: FnHandler) -> Type[BaseModel]:
        properties: Dict[str, Any] = {}
        if action.input_schema:
            properties["body"] = dict(type="object", properties=action.input_schema)

        required = ["body"]
        if action.files == "single" or action.files == "single-optional":
            properties["file"] = dict(type="string", format="binary")
            if action.files == "single":
                required.append("file")
        elif action.files == "multiple":
            properties["file"] = dict(type="array", items=dict(type="string", format="binary"))
            required.append("file")
        elif "files" in properties:
            del properties["file"]
        schema = {"type": "object", "properties": properties, "required": required}
        return schema_to_model(schema, f"{handler.name.capitalize()}{action.name.capitalize()}InputModel")

    return fn


def _make_output_schema(action: ActionDefinition):
    def fn(agent: object, handler: FnHandler) -> Type[Any]:
        # noinspection PyUnresolvedReferences
        if not action.output_schema:
            raise ValueError("output_schema must be specified")

        if action.output_schema == "str":
            return str
        else:
            return schema_to_model(
                action.output_schema, f"{handler.name.capitalize()}{action.name.capitalize()}OutputModel"
            )

    return fn
