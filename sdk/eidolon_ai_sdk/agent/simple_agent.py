from __future__ import annotations

import asyncio
from datetime import datetime
from typing import List, Literal, Optional, Union, Dict, Any

from fastapi import Body
from jinja2 import Environment, meta, StrictUndefined
from pydantic import field_validator, model_validator, BaseModel
from pydantic_core import to_jsonable_python, SchemaError

from eidolon_ai_client.events import AgentStateEvent, StringOutputEvent, UserInputEvent, FileHandle, \
    StartStreamContextEvent, EndStreamContextEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.apu.agent_io import SystemAPUMessage, UserTextAPUMessage, AttachedFileMessage, FileHandleWithInclude
from eidolon_ai_sdk.apu.agents_logic_unit import AgentsLogicUnitSpec, AgentsLogicUnit
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.system.agent_builder import AgentBuilder
from eidolon_ai_sdk.system.processes import ProcessDoc
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from eidolon_ai_sdk.system.resources.resources_base import Metadata
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class ActionDefinition(BaseModel):
    name: str = "converse"
    title: Optional[str] = None
    sub_title: Optional[str] = None
    description: Optional[str] = None
    user_prompt: str = "{{ body }}"
    input_schema: Dict[str, dict] = {}
    output_schema: Union[Literal["str"], Dict[str, Any]] = "str"
    allow_file_upload: bool = False
    # allow all types for text, image, audio, word, pdf, json, etc
    supported_mime_types: List[str] = []  # an empty list means all types are supported
    allowed_states: List[str] = ["initialized", "idle", "http_error"]
    output_state: str = "idle"

    @field_validator("input_schema")
    def validate_prompt_properties(cls, input_dict):
        if not isinstance(input_dict, dict):
            raise ValueError("input_schema must be a dict")
        for k, v in input_dict.items():
            if isinstance(v, dict):
                if v.get("format") == "binary":
                    raise ValueError("input_schema cannot contain format = 'binary' fields.")
        return input_dict

    @field_validator("supported_mime_types")
    def validate_supported_mime_types(cls, supported_mime_types):
        if not isinstance(supported_mime_types, list):
            raise ValueError("supported_mime_types must be a List[str]")
        if not supported_mime_types:
            return supported_mime_types

        all_mime_types = {
            "application/json",
            "text/plain",
            "image/*",
            "audio/*",
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        }
        bad_types = []
        for mime_type in supported_mime_types:
            if mime_type not in all_mime_types:
                bad_types.append(mime_type)
        if bad_types:
            raise ValueError(f"supported_mime_types contains unsupported entries: {bad_types}")

        return supported_mime_types


class NamedAPU(BaseModel):
    title: Optional[str] = None
    apu: AnnotatedReference[APU]
    default: bool = False


class SimpleAgent(AgentBuilder):
    """
    agent is designed to be a flexible, modular component that can interact with various processing units and perform a
    range of actions based on its configuration.
    """

    description: Optional[str] = None
    system_prompt: str = (
        "You are a helpful assistant. Always use the provided tools, if appropriate, to complete the task."
    )
    agent_refs: List[str] = []
    actions: List[ActionDefinition] = [ActionDefinition()]
    apu: AnnotatedReference[APU]
    apus: List[NamedAPU] = []
    title_generation_mode: Literal["none", "on_request", "auto"] = "none"

    @model_validator(mode="before")
    def validate_apu(cls, value):
        if "cpu" in value:
            logger.warning("cpu is deprecated, use apu instead")
            value["apu"] = value.pop("cpu")
        if "apu" in value and "apus" in value:
            raise ValueError("Cannot specify both apu and apus")
        return value

    # noinspection PyTypeChecker
    @model_validator(mode="after")
    def validate_apus(self):
        if self.apus:
            self.apu = None
        if not self.apu and not self.apus:
            raise ValueError("Must specify either apu or apus")
        return self

    async def create_process(self, process_id: str):
        if self.apu:
            default_apu_ref = self.apu
        else:
            default_apu_ref = ([apu.apu for apu in self.apus if apu.default] or [self.apus[0].apu])[0]
        default_apu = default_apu_ref.instantiate()
        t = default_apu.main_thread(process_id)
        await t.set_boot_messages(prompts=[SystemAPUMessage(prompt=self.system_prompt)])


# todo, this should be in spec
generate_title_message = (
    "Generating a title for this conversation. Consider the context and content of the discussion or text. "
    "Create a concise, relevant, and accurate representation of the main topic or theme in the content."
    "Create a title that draws inspiration from key phrases or ideas in the content. "
    "Do not use any tools to generate the title. "
    "The title should be no longer than 5 words. Do not wrap the title in quotes. Answer only with the title."
)


@SimpleAgent.dynamic_contract
def fn(spec: SimpleAgent, metadata: Metadata):
    apus: Dict[str, APU] = {}
    for apu_spec in spec.apus or [NamedAPU(apu=spec.apu, default=True)]:
        apu = apu_spec.apu.instantiate()
        apu.title = apu_spec.title or apu.__class__.__name__
        _register_refs_logic_unit(apu, spec.agent_refs, spec.tools)
        apus[apu_spec.title] = apu
    default_apu: APU = apus[(list(filter(lambda apu: apu.default, spec.apus)) or [NamedAPU(apu=spec.apu, default=True)])[0].title]

    if spec.title_generation_mode == "on_request":
        @SimpleAgent.action(description="Generate a title for the conversation", allowed_states=["initialized", "idle"])
        async def generate_title(process_id: str):
            last_state = RequestContext.get("__last_state__")
            title_message = UserTextAPUMessage(prompt=generate_title_message)
            response = await (await apu.clone_thread(process_id)).run_request(prompts=[title_message])

            process_obj = await ProcessDoc.find_one(query={"_id": process_id})
            await process_obj.update(title=response)

            yield StartStreamContextEvent(context_id="title_generation", title="GeneratingTitle")
            yield StringOutputEvent(stream_context="title_generation", content=response)
            yield EndStreamContextEvent(context_id="title_generation")
            yield AgentStateEvent(state=last_state)

    for a in spec.actions:
        if not a.output_schema:
            raise ValueError("output_schema must be specified")
        model_name = f"{metadata.name.capitalize()}{a.name.capitalize()}OutputModel"
        try:
            output_schema = str if a.output_schema == "str" else schema_to_model(a.output_schema, model_name)
        except SchemaError as e:
            raise ValueError(f"Invalid output_schema for action '{a.name}'") from e
        input_schema = _make_input_schema(spec, a, metadata)

        @SimpleAgent.action(
            a.name,
            a.title,
            a.sub_title,
            a.description,
            a.allowed_states,
            input_schema,
            output_schema,
            custom_user_input_event=True,
            partials=dict(action=a)
        )
        async def action_fn(process_id, action, **kwargs):
            execute_on_apu = None
            request_body = to_jsonable_python(kwargs.get("body") or {})
            if isinstance(request_body, dict) and "execute_on_apu" in request_body:
                execute_on_apu = request_body.pop("execute_on_apu")

            attached_files: List[FileHandle] = []
            attached_files_messages = []
            if isinstance(request_body, dict) and "attached_files" in request_body:
                # add a new file handle message
                attached_files_list = request_body.pop("attached_files") or []
                for file in attached_files_list:
                    include_directly = file.pop("include_directly", False)
                    fh = FileHandle(**file)
                    attached_files_messages.append(AttachedFileMessage(file=fh, include_directly=include_directly))
                    attached_files.append(fh)

            body = dict(datetime_iso=datetime.now().isoformat(), body=str(request_body))
            if isinstance(request_body, dict):
                body.update(request_body)

            env = Environment(undefined=StrictUndefined)
            text_message = UserTextAPUMessage(prompt=env.from_string(action.user_prompt).render(**body))

            if execute_on_apu and execute_on_apu in apus:
                apu = apus[execute_on_apu]
            elif execute_on_apu:
                logger.warning(f"APU {execute_on_apu} not found, using default APU")
                apu = default_apu
            else:
                apu = default_apu

            yield UserInputEvent(input=request_body, files=attached_files)

            # generate the tile if it is not generated
            gen_title_task = None
            process_obj = await ProcessDoc.find_one(query={"_id": process_id})

            if spec.title_generation_mode == "auto" and not process_obj.title:
                async def genTitle():
                    title_message = UserTextAPUMessage(prompt=generate_title_message)
                    new_thread = await apu.main_thread(process_id).clone()
                    title_response = await new_thread.run_request(prompts=[title_message])
                    await process_obj.update(title=title_response)

                gen_title_task = asyncio.create_task(genTitle())

            thread = apu.main_thread(process_id)
            response = thread.stream_request(
                output_format=action.output_schema, prompts=[*attached_files_messages, text_message]
            )

            async for event in response:
                yield event
            yield AgentStateEvent(state=action.output_state)
            if gen_title_task:
                try:
                    await gen_title_task
                except Exception:
                    logger.exception("Error generating title")


def _register_refs_logic_unit(apu, agent_refs, extra_tools=None):
    if hasattr(apu, "logic_units"):
        if agent_refs:
            apu.logic_units.append(
                AgentsLogicUnit(
                    processing_unit_locator=apu,
                    spec=AgentsLogicUnitSpec(agents=agent_refs),
                )
            )
        if extra_tools:
            apu.logic_units.extend([t.instantiate() for t in extra_tools])


def _make_input_schema(spec: SimpleAgent, action: ActionDefinition, metadata: Metadata):
    properties: Dict[str, Any] = {}
    required = []
    user_vars = meta.find_undeclared_variables(Environment().parse(action.user_prompt))
    # pop out any reserved keywords we will inject
    if "datetime_iso" in user_vars:
        user_vars.remove("datetime_iso")
    if len(user_vars) == 1 and "body" in user_vars and not spec.apus and not action.allow_file_upload:
        properties["body"] = dict(type="string", default=Body(..., media_type="text/plain"))
        required.append("body")
    elif user_vars:
        props = {v: action.input_schema.get(v, dict(type="string")) for v in user_vars}
        properties["body"] = dict(type="object", properties=props)
        required.append("body")

    if action.allow_file_upload:
        properties["body"]["properties"]["attached_files"] = dict(type="array", items=FileHandleWithInclude.model_json_schema())

    if spec.apus:
        apu_names = [apu.title for apu in spec.apus]
        default = (list(filter(lambda apu: apu.default, spec.apus)) or spec.apus)[0].title
        properties["body"]["properties"]["execute_on_apu"] = dict(type="string", enum=apu_names, default=default)
        if "required" not in properties["body"]:
            properties["body"]["required"] = []
        properties["body"]["required"].append("execute_on_apu")

    schema = {"type": "object", "properties": properties, "required": required}
    return schema_to_model(schema, f"{metadata.name.capitalize()}{action.name.capitalize()}InputModel")
