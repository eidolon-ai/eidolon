from typing import List, Annotated

from fastapi import UploadFile, Body
from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel

from eidos.agent.agent import Agent, register_action, AgentState, AgentSpec, register_program, spec_input_model
from eidos.cpu.agent_io import UserTextCPUMessage, SystemCPUMessage, ImageCPUMessage
from eidos.system.reference_model import Specable


# todo, this probably defines states and output schema, but leaving that out for now
class GenericAgentSpec(AgentSpec):
    system_prompt: str
    question_prompt: str
    prompt_properties: dict = {}


class LlmResponse(BaseModel):
    response: str


class GenericAgent(Agent, Specable[GenericAgentSpec]):
    @register_program(input_model=spec_input_model(lambda spec: dict(type="object", properties=spec.prompt_properties)))
    async def question(self, process_id, body, images: List[UploadFile] = None) -> AgentState[LlmResponse]:
        images = images or []
        schema = LlmResponse.model_json_schema()
        schema['type'] = 'object'

        env = Environment(undefined=StrictUndefined)
        await self.cpu.main_thread(process_id).set_boot_messages(
            SystemCPUMessage(prompt=(env.from_string(self.spec.system_prompt).render(**dict(body))))
        )
        # pull out any kwargs that are UploadFile and put them in a list of UserImageCPUMessage
        image_messages = []
        for image in images:
            image_messages.append(ImageCPUMessage(image=image.file, prompt=image.filename))

        response = await self.cpu.main_thread(process_id).schedule_request(
            prompts=[UserTextCPUMessage(prompt=(env.from_string(self.spec.question_prompt).render(**dict(body)))), *image_messages],
            output_format=schema
        )
        response = LlmResponse(**response)
        return AgentState(name='idle', data=response)

    @register_action('idle')
    async def respond(self, process_id, statement: Annotated[str, Body(embed=True)]) -> AgentState[LlmResponse]:
        response = await self.cpu.main_thread(process_id).schedule_request([UserTextCPUMessage(prompt=statement)], LlmResponse.model_json_schema())
        return AgentState(name='idle', data=response)
