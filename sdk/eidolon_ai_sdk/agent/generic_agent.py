from datetime import datetime
from typing import Annotated, Dict, Any, Literal, Type, Union

from fastapi import Body
from jinja2 import Environment, StrictUndefined, meta
from pydantic import BaseModel, field_validator, Field, model_validator
from pydantic_core import to_jsonable_python

from eidolon_ai_client.events import AgentStateEvent
from eidolon_ai_sdk.agent.agent import (
    Agent,
    register_action,
    AgentState,
    AgentSpec,
    register_program,
)
from eidolon_ai_sdk.cpu.agent_io import UserTextAPUMessage, SystemAPUMessage
from eidolon_ai_sdk.system.fn_handler import FnHandler
from eidolon_ai_sdk.system.reference_model import Specable
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class GenericAgentSpec(AgentSpec):
    description: str
    system_prompt: str
    user_prompt: str = "{{ question }}"
    input_schema: Dict[str, Any] = Field(None, description="The json schema for the input model.")
    output_schema: Union[Literal["str"], Dict[str, Any]] = Field(
        default="str", description="The json schema for the output model or the literal 'str' for text output."
    )
    files: Literal["disable", "single", "single-optional", "multiple"] = "disable"

    @model_validator(mode="after")
    def _set_input_schema_default(self):
        if self.input_schema is None:
            env = Environment()
            system_vars = meta.find_undeclared_variables(env.parse(self.system_prompt))
            user_vars = meta.find_undeclared_variables(env.parse(self.user_prompt))
            self.input_schema = {v: dict(type="string") for v in system_vars.union(user_vars) if v != "datetime_iso"}
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


class LlmResponse(BaseModel):
    response: str


def make_description(agent: object, _handler: FnHandler) -> str:
    # noinspection PyUnresolvedReferences
    spec = agent.spec
    return spec.description


def make_input_schema(agent: object, handler: FnHandler) -> Type[BaseModel]:
    # noinspection PyUnresolvedReferences
    spec = agent.spec
    properties: Dict[str, Any] = {}
    if spec.input_schema:
        properties["body"] = dict(
            type="object",
            properties=spec.input_schema,
        )
    required = ["body"]
    schema = {"type": "object", "properties": properties, "required": required}
    return schema_to_model(schema, f"{handler.name.capitalize()}InputModel")


def make_output_schema(agent: object, handler: FnHandler) -> Type[Any]:
    # noinspection PyUnresolvedReferences
    spec = agent.spec
    if spec.output_schema == "str":
        return str
    elif spec.output_schema:
        return schema_to_model(spec.output_schema, f"{handler.name.capitalize()}OutputModel")
    else:
        raise ValueError("output_schema must be specified")


class GenericAgent(Agent, Specable[GenericAgentSpec]):
    @register_program(
        input_model=make_input_schema,
        output_model=make_output_schema,
        description=make_description,
    )
    async def question(self, process_id, **kwargs) -> AgentState[Any]:
        body = dict(datetime_iso=datetime.now().isoformat())
        body.update(kwargs.get("body") or {})
        body = to_jsonable_python(body)

        env = Environment(undefined=StrictUndefined)
        t = await self.cpu.main_thread(process_id)
        await t.set_boot_messages(
            prompts=[SystemAPUMessage(prompt=(env.from_string(self.spec.system_prompt).render(**body)))],
        )

        # pull out any kwargs that are UploadFile and put them in a list of UserImageCPUMessage
        image_messages = []

        response = t.stream_request(
            prompts=[
                UserTextAPUMessage(prompt=(env.from_string(self.spec.user_prompt).render(**body))),
                *image_messages,
            ],
            output_format=self.spec.output_schema,
        )
        async for event in response:
            yield event
        yield AgentStateEvent(state="idle")

    @register_action("idle", "http_error")
    async def respond(self, process_id, statement: Annotated[str, Body(embed=True)]) -> AgentState[Any]:
        t = await self.cpu.main_thread(process_id)
        response = await t.run_request([UserTextAPUMessage(prompt=statement)], self.spec.output_schema)
        return AgentState(name="idle", data=response)
