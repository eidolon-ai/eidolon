from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional, Union, Dict, Any, AsyncIterable

from fastapi import Body
from jinja2 import Environment, meta, StrictUndefined
from openai import BaseModel
from pydantic import field_validator
from pydantic_core import to_jsonable_python

from eidolon_ai_sdk.agent.agent import AgentSpec, Agent, register_action
from eidolon_ai_sdk.cpu.agent_io import SystemCPUMessage, ImageCPUMessage, UserTextCPUMessage
from eidolon_ai_client.events import AgentStateEvent, StreamEvent
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class ActionDefinition(BaseModel):
    name: str = "converse"
    description: Optional[str] = None
    user_prompt: str = "{{ body }}"
    input_schema: dict = None
    output_schema: Union[Literal["str"], Dict[str, Any]] = "str"
    files: Literal["disable", "single-optional", "single", "multiple"] = "disable"
    allowed_states: List[str] = ["initialized", "idle", "http_error"]
    output_state: str = "idle"

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

    def make_input_schema(self, agent, handler):
        properties: Dict[str, Any] = {}
        required = []
        user_vars = meta.find_undeclared_variables(Environment().parse(self.user_prompt))
        if self.input_schema is not None:
            properties["body"] = dict(type="object", properties=self.input_schema)
            required.append("body")
        elif len(user_vars) == 1 and "body" in user_vars:
            properties["body"] = dict(type="string", default=Body(..., media_type="text/plain"))
            required.append("body")
        elif user_vars:
            props = {v: dict(type="string") for v in user_vars if v != "datetime_iso" and v != "body"}
            properties["body"] = dict(type="object", properties=props)
            required.append("body")

        if self.files == "single-optional":
            properties["file"] = dict(type="string", format="binary")
        elif self.files == "single":
            properties["file"] = dict(type="string", format="binary")
            required.append("file")
        elif self.files == "multiple":
            properties["file"] = dict(type="array", items=dict(type="string", format="binary"))
        schema = {"type": "object", "properties": properties, "required": required}
        return schema_to_model(schema, f"{handler.name.capitalize()}{self.name.capitalize()}InputModel")

    def make_output_schema(self, agent, handler):
        if not self.output_schema:
            raise ValueError("output_schema must be specified")
        model_name = f"{handler.name.capitalize()}{self.name.capitalize()}OutputModel"
        return str if self.output_schema == "str" else schema_to_model(self.output_schema, model_name)


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
                    input_model=action.make_input_schema,
                    output_model=action.make_output_schema,
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

    async def _act(self, action: ActionDefinition, process_id, **kwargs) -> AsyncIterable[StreamEvent]:
        request_body = to_jsonable_python(kwargs.get("body") or {})
        body = dict(datetime_iso=datetime.now().isoformat(), body=str(request_body))
        if isinstance(request_body, dict):
            body.update(request_body)

        files = kwargs.get("file", []) or []
        if not isinstance(files, list):
            files = [files]

        image_messages = [ImageCPUMessage(image=file.file, prompt=file.filename) for file in files if file]

        env = Environment(undefined=StrictUndefined)
        text_message = UserTextCPUMessage(prompt=env.from_string(action.user_prompt).render(**body))

        thread = await self.cpu.main_thread(process_id)
        response = thread.stream_request(output_format=action.output_schema, prompts=[*image_messages, text_message])

        async for event in response:
            yield event
        yield AgentStateEvent(state=action.output_state)
