from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional, Union, Dict, Any, AsyncIterable

from fastapi import Body
from jinja2 import Environment, meta, StrictUndefined
from openai import BaseModel
from pydantic import field_validator, model_validator
from pydantic_core import to_jsonable_python

from eidolon_ai_client.events import AgentStateEvent, StreamEvent, StringOutputEvent
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.agent.agent import register_action
from eidolon_ai_sdk.cpu.agent_cpu import AgentCPU
from eidolon_ai_sdk.cpu.agent_io import SystemCPUMessage, ImageCPUMessage, UserTextCPUMessage
from eidolon_ai_sdk.cpu.agents_logic_unit import AgentsLogicUnitSpec, AgentsLogicUnit
from eidolon_ai_sdk.system.processes import ProcessDoc
from eidolon_ai_sdk.system.reference_model import Specable, AnnotatedReference
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
        # pop out any reserved keywords we will inject
        if "datetime_iso" in user_vars:
            user_vars.remove("datetime_iso")
        if self.input_schema is not None:
            properties["body"] = dict(type="object", properties=self.input_schema)
            required.append("body")
        elif len(user_vars) == 1 and "body" in user_vars and not agent.spec.cpus:
            properties["body"] = dict(type="string", default=Body(..., media_type="text/plain"))
            required.append("body")
        elif user_vars:
            props = {v: dict(type="string") for v in user_vars}
            properties["body"] = dict(type="object", properties=props)
            required.append("body")

        if self.files == "single-optional":
            properties["file"] = dict(type="string", format="binary")
        elif self.files == "single":
            properties["file"] = dict(type="string", format="binary")
            required.append("file")
        elif self.files == "multiple":
            properties["file"] = dict(type="array", items=dict(type="string", format="binary"))
        if agent.spec.cpus:
            cpu_names = [cpu.title for cpu in agent.spec.cpus]
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
    cpu: AnnotatedReference[AgentCPU]
    default: bool = False


class SimpleAgentSpec(BaseModel):
    description: Optional[str] = None
    system_prompt: str = "You are a helpful assistant"
    agent_refs: List[str] = []
    actions: List[ActionDefinition] = [ActionDefinition()]
    cpu: AnnotatedReference[AgentCPU] = None
    cpus: Optional[List[NamedCPU]] = []
    title_generation_mode: Literal["none", "on_request"] = "on_request"

    @model_validator(mode="before")
    def validate_cpu(cls, value):
        if "cpu" in value and "cpus" in value:
            raise ValueError("Cannot specify both cpu and cpus")
        return value

    # noinspection PyTypeChecker
    @model_validator(mode="after")
    def validate_cpus(self):
        if self.cpus:
            self.cpu = None
        return self


class SimpleAgent(Specable[SimpleAgentSpec]):
    generate_title_prompt = ("You are generating a title for a conversation. Consider the context and content of the discussion or text. "
                             "Create a concise, relevant, and accurate representation of the main topic or theme in the content."
                             "Create a title that draws insiration from key phrases or ideas in the content. "
                             "The title should be no longer than 5 words. Do not wrap the title in quotes. Answer only with the title. The prompt for the conversation is:\n")

    def __init__(self, spec):
        super().__init__(spec=spec)
        if self.spec.cpu:
            self.cpu = self.spec.cpu.instantiate()
            self.cpu.title = self.cpu.__class__.__name__
            self._register_refs_logic_unit(self.cpu, self.spec.agent_refs)
        else:
            self.cpus = []
            for cpu_spec in self.spec.cpus:
                cpu = cpu_spec.cpu.instantiate()
                # todo - add title from metadata
                cpu.title = cpu_spec.title or cpu.__class__.__name__
                if cpu_spec.default:
                    cpu.default = True
                    self.cpu = cpu
                self._register_refs_logic_unit(cpu, self.spec.agent_refs)
                self.cpus.append(cpu)

        if self.spec.title_generation_mode == "on_request":
            # add a title generation action
            action = ActionDefinition(
                name="generate_title",
                description="Generate a title for the conversation",
                user_prompt=self.generate_title_prompt + "{{ body }}",
                output_schema="str",
                files="disable",
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
        await t.set_boot_messages(prompts=[SystemCPUMessage(prompt=self.spec.system_prompt)])

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

        body = dict(datetime_iso=datetime.now().isoformat(), body=str(request_body))
        if isinstance(request_body, dict):
            body.update(request_body)

        files = kwargs.get("file", []) or []
        if not isinstance(files, list):
            files = [files]

        image_messages = [ImageCPUMessage(image=file.file, prompt=file.filename) for file in files if file]

        env = Environment(undefined=StrictUndefined)
        text_message = UserTextCPUMessage(prompt=env.from_string(action.user_prompt).render(**body))

        if execute_on_cpu:
            cpu = self.cpu
            for named_cpu in self.cpus:
                if named_cpu.title == execute_on_cpu:
                    cpu = named_cpu
                    break
        else:
            cpu = self.cpu

        thread = await cpu.main_thread(process_id)
        response = thread.stream_request(output_format=action.output_schema, prompts=[*image_messages, text_message])

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
        text_message = UserTextCPUMessage(prompt=env.from_string(action.user_prompt).render(**body))

        if execute_on_cpu:
            cpu = self.cpu
            for named_cpu in self.cpus:
                if named_cpu.title == execute_on_cpu:
                    cpu = named_cpu
                    break
        else:
            cpu = self.cpu

        title_message = UserTextCPUMessage(prompt=self.generate_title_prompt + text_message.prompt)
        response = await (await cpu.new_thread(process_id)).run_request(prompts=[title_message])
        await process_obj.update(title=response)

        yield StringOutputEvent(content=response)
        # return to the previous state
        print(process_obj.state)
        yield AgentStateEvent(state=last_state)
