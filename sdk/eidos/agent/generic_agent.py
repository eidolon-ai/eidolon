from typing import Annotated, Dict, Any, Literal

from fastapi import Body
from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel, field_validator, Field

from eidos.agent.agent import Agent, register_action, AgentState, AgentSpec, register_program, spec_input_model, \
    get_input_model, nest_with_fn
from eidos.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage, ImageCPUMessage
from eidos.system.reference_model import Specable


# todo, this probably defines states and output schema, but leaving that out for now
class GenericAgentSpec(AgentSpec):
    system_prompt: str
    question_prompt: str
    prompt_properties: Dict[str, Any] = Field({}, description="A dictionary of properties to be used in the prompt")
    files: Literal['disable', 'single', 'multiple'] = "disable"

    @field_validator('prompt_properties')
    def validate_prompt_properties(cls, input_dict):
        if not isinstance(input_dict, dict):
            raise ValueError("prompt_properties must be a dict")
        # todo -- make sure the dictionary doesn't contain any format = "binary" fields, nested
        for k, v in input_dict.items():
            if isinstance(v, dict):
                if v.get('format') == 'binary':
                    raise ValueError("prompt_properties cannot contain format = 'binary' fields. Use the files option instead")
        return input_dict


class LlmResponse(BaseModel):
    response: str


def fixup_properties(spec: GenericAgentSpec):
    properties: Dict[str, Any] = {}
    if spec.prompt_properties:
        properties['body'] = dict(
            type="object",
            properties=spec.prompt_properties,
        )
    if spec.files == 'single':
        properties['files'] = dict(type="string", format="binary")
    elif spec.files == 'multiple':
        properties['files'] = dict(type="array", items=dict(type="string", format="binary"))
    elif 'files' in properties:
        del properties['files']
    return properties


class GenericAgent(Agent, Specable[GenericAgentSpec]):
    @register_program(input_model=spec_input_model(
        fixup_properties,
        transformer=nest_with_fn(get_input_model)
    ))
    async def question(self, process_id, **kwargs) -> AgentState[LlmResponse]:
        body = kwargs.get('body')
        body = dict(body) if body else {}
        files = kwargs.get('files', [])
        if not isinstance(files, list):
            files = [files]
        schema = LlmResponse.model_json_schema()
        schema['type'] = 'object'

        env = Environment(undefined=StrictUndefined)
        t = await self.cpu.main_thread(process_id)
        await t.set_boot_messages(
            schema,
            SystemCPUMessage(prompt=(env.from_string(self.spec.system_prompt).render(**body)))
        )

        # pull out any kwargs that are UploadFile and put them in a list of UserImageCPUMessage
        image_messages = []
        for image in files:
            image_messages.append(ImageCPUMessage(image=image.file, prompt=image.filename))

        response = await t.schedule_request(
            prompts=[UserTextCPUMessage(prompt=(env.from_string(self.spec.question_prompt).render(**body))), *image_messages],
            output_format=schema
        )
        response = LlmResponse(**response)
        return AgentState(name='idle', data=response)

    @register_action('idle')
    async def respond(self, process_id, statement: Annotated[str, Body(embed=True)]) -> AgentState[LlmResponse]:
        t = await self.cpu.main_thread(process_id)
        response = await t.schedule_request([UserTextCPUMessage(prompt=statement)], LlmResponse.model_json_schema())
        return AgentState(name='idle', data=response)
