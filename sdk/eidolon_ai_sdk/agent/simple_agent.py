from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional, Union, Dict, Any, AsyncIterable

from fastapi import Body
from jinja2 import Environment, meta, StrictUndefined
from openai import BaseModel
from pydantic import field_validator, model_validator
from pydantic_core import to_jsonable_python

from eidolon_ai_client.events import AgentStateEvent, StreamEvent, StringOutputEvent, UserInputEvent, FileHandle
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.agent.doc_manager.document_processor import DocumentProcessor
from eidolon_ai_sdk.cpu.agent_cpu import APU
from eidolon_ai_sdk.cpu.agent_io import SystemAPUMessage, UserTextAPUMessage, AttachedFileMessage
from eidolon_ai_sdk.cpu.agents_logic_unit import AgentsLogicUnitSpec, AgentsLogicUnit
from eidolon_ai_sdk.system.processes import ProcessDoc
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
from eidolon_ai_sdk.util.schema_to_model import schema_to_model


class ActionDefinition(BaseModel):
    name: str = "converse"
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

    def make_input_schema(self, agent, handler):
        properties: Dict[str, Any] = {}
        required = []
        user_vars = meta.find_undeclared_variables(Environment().parse(self.user_prompt))
        # pop out any reserved keywords we will inject
        if "datetime_iso" in user_vars:
            user_vars.remove("datetime_iso")
        if len(user_vars) == 1 and "body" in user_vars and not agent.spec.apus and not self.allow_file_upload:
            properties["body"] = dict(type="string", default=Body(..., media_type="text/plain"))
            required.append("body")
        elif user_vars:
            props = {v: self.input_schema.get(v, dict(type="string")) for v in user_vars}
            properties["body"] = dict(type="object", properties=props)
            required.append("body")

        if self.allow_file_upload:
            properties["body"]["properties"]["attached_files"] = dict(type="array", items=FileHandle.model_json_schema())

        if agent.spec.apus:
            cpu_names = [cpu.title for cpu in agent.spec.apus]
            default = agent.cpu.title
            properties["body"]["properties"]["execute_on_cpu"] = dict(type="string", enum=cpu_names, default=default)
            if "required" not in properties["body"]:
                properties["body"]["required"] = []
            properties["body"]["required"].append("execute_on_cpu")

        schema = {"type": "object", "properties": properties, "required": required}
        return schema_to_model(schema, f"{handler.name.capitalize()}{self.name.capitalize()}InputModel")

    def make_output_schema(self, agent, handler):
        if not self.output_schema:
            raise ValueError("output_schema must be specified")
        model_name = f"{handler.name.capitalize()}{self.name.capitalize()}OutputModel"
        return str if self.output_schema == "str" else schema_to_model(self.output_schema, model_name)


class NamedCPU(BaseModel):
    title: Optional[str] = None
    apu: AnnotatedReference[APU]
    default: bool = False


class SimpleAgentSpec(BaseModel):
    description: Optional[str] = None
    system_prompt: str = "You are a helpful assistant"
    agent_refs: List[str] = []
    actions: List[ActionDefinition] = [ActionDefinition()]
    apu: AnnotatedReference[APU] = None
    apus: List[NamedCPU] = []
    title_generation_mode: Literal["none", "on_request"] = "on_request"
    doc_processor: AnnotatedReference[DocumentProcessor]

    @model_validator(mode="before")
    def validate_cpu(cls, value):
        if "cpu" in value:
            logger.warning("cpu is deprecated, use apu instead")
            value["apu"] = value.pop("cpu")
        if "apu" in value and "apus" in value:
            raise ValueError("Cannot specify both apu and apus")
        return value

    # noinspection PyTypeChecker
    @model_validator(mode="after")
    def validate_cpus(self):
        if self.apus:
            self.apu = None
        return self


class SimpleAgent(Specable[SimpleAgentSpec]):
    generate_title_prompt = (
        "You are generating a title for a conversation. Consider the context and content of the discussion or text. "
        "Create a concise, relevant, and accurate representation of the main topic or theme in the content."
        "Create a title that draws insiration from key phrases or ideas in the content. "
        "The title should be no longer than 5 words. Do not wrap the title in quotes. Answer only with the title. The prompt for the conversation is:\n"
    )

    def __init__(self, spec):
        super().__init__(spec=spec)
        if self.spec.apu:
            self.cpu = self.spec.apu.instantiate()
            self.cpu.title = self.cpu.__class__.__name__
            self._register_refs_logic_unit(self.cpu, self.spec.agent_refs)
        else:
            self.cpus = []
            for cpu_spec in self.spec.apus:
                apu = cpu_spec.apu.instantiate()
                # todo - add title from metadata
                apu.title = cpu_spec.title or apu.__class__.__name__
                if cpu_spec.default:
                    apu.default = True
                    self.cpu = apu
                self._register_refs_logic_unit(apu, self.spec.agent_refs)
                self.cpus.append(apu)

        if self.spec.title_generation_mode == "on_request":
            # add a title generation action
            action = ActionDefinition(
                name="generate_title",
                description="Generate a title for the conversation",
                user_prompt=self.generate_title_prompt + "{{ body }}",
                output_schema="str",
                allowed_states=["initialized", "idle"],
                output_state="idle",
            )

            setattr(
                self,
                action.name,
                register_action(
                    *action.allowed_states,
                    name=action.name,
                    input_model=action.make_input_schema,
                    output_model=action.make_output_schema,
                    description=action.description,
                )(self._act_wrapper(action, SimpleAgent._gen_title)),
            )

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
                )(self._act_wrapper(action, SimpleAgent._act)),
            )

    def _register_refs_logic_unit(self, cpu, agent_refs):
        if agent_refs and hasattr(cpu, "logic_units"):
            cpu.logic_units.append(
                AgentsLogicUnit(
                    processing_unit_locator=cpu,
                    spec=AgentsLogicUnitSpec(agents=agent_refs),
                )
            )

    async def create_process(self, process_id):
        t = await self.cpu.main_thread(process_id)
        await t.set_boot_messages(prompts=[SystemAPUMessage(prompt=self.spec.system_prompt)])

    @staticmethod
    def _act_wrapper(action, action_fn):
        async def fn(self, process_id, **kwargs):
            async for e in action_fn(self, action, process_id, **kwargs):
                yield e

        return fn

    async def _act(self, action: ActionDefinition, process_id, **kwargs) -> AsyncIterable[StreamEvent]:
        execute_on_cpu = None
        request_body = to_jsonable_python(kwargs.get("body") or {})
        if "execute_on_cpu" in request_body:
            execute_on_cpu = request_body.pop("execute_on_cpu")

        attached_files: List[FileHandle] = []
        attached_files_messages = []
        if "attached_files" in request_body:
            # add a new file handle message
            attached_files = request_body.pop("attached_files") or []
            for file in attached_files:
                attached_files_messages.append(AttachedFileMessage(file=file, include_directly=True))

        body = dict(datetime_iso=datetime.now().isoformat(), body=str(request_body))
        if isinstance(request_body, dict):
            body.update(request_body)

        env = Environment(undefined=StrictUndefined)
        text_message = UserTextAPUMessage(prompt=env.from_string(action.user_prompt).render(**body))

        if execute_on_cpu:
            cpu = self.cpu
            for named_cpu in self.cpus:
                if named_cpu.title == execute_on_cpu:
                    cpu = named_cpu
                    break
        else:
            cpu = self.cpu

        yield UserInputEvent(input=request_body, files=attached_files)
        thread = await cpu.main_thread(process_id)
        response = thread.stream_request(
            output_format=action.output_schema, prompts=[*attached_files_messages, text_message]
        )

        async for event in response:
            yield event
        yield AgentStateEvent(state=action.output_state)

    async def _gen_title(self, action: ActionDefinition, process_id, **kwargs) -> AsyncIterable[StreamEvent]:
        last_state = RequestContext.get("__last_state__")

        process_obj = await ProcessDoc.find_one(query={"_id": process_id})
        execute_on_cpu = None
        request_body = to_jsonable_python(kwargs.get("body") or {})
        if "execute_on_cpu" in request_body:
            execute_on_cpu = request_body.pop("execute_on_cpu")

        body = dict(datetime_iso=datetime.now().isoformat(), body=str(request_body))
        if isinstance(request_body, dict):
            body.update(request_body)

        env = Environment(undefined=StrictUndefined)
        text_message = UserTextAPUMessage(prompt=env.from_string(action.user_prompt).render(**body))

        if execute_on_cpu:
            cpu = self.cpu
            for named_cpu in self.cpus:
                if named_cpu.title == execute_on_cpu:
                    cpu = named_cpu
                    break
        else:
            cpu = self.cpu

        title_message = UserTextAPUMessage(prompt=self.generate_title_prompt + text_message.prompt)
        response = await (await cpu.new_thread(process_id)).run_request(prompts=[title_message])
        await process_obj.update(title=response)

        yield StringOutputEvent(content=response)
        # return to the previous state
        yield AgentStateEvent(state=last_state)
