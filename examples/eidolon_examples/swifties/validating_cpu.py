import asyncio
import json
from typing import Any, List, Literal, Union, Dict, Optional, Iterable

from fastapi import HTTPException
from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from eidos_sdk.agent.client import Program
from eidos_sdk.cpu.agent_cpu import AgentCPU, Thread
from eidos_sdk.cpu.agent_io import CPUMessageTypes, SystemCPUMessage
from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.cpu.logic_unit import LogicUnit
from eidos_sdk.system.reference_model import AnnotatedReference, Specable, Reference
from eidos_sdk.util.logger import logger


class InputValidatorBody(BaseModel):
    prompts: str


class OutputValidatorBody(BaseModel):
    prompts: str
    output_schema: str | dict
    response: Any


# todo, validation rejections should probably be non 2xx
class InputValidatorResponse(BaseModel):
    status: Literal['allow', "block"]
    reason: Optional[str] = None


class OutputValidationResponse(BaseModel):
    status: Literal['allow', "regenerate"]
    reason: Optional[str] = None


class ValidatingCPUSpec(BaseModel):
    cpu: AnnotatedReference[AgentCPU]
    logic_units: List[Reference[LogicUnit]] = []
    input_validators: List[str] = []
    output_validators: List[str] = []
    regeneration_prompt: str = """
    Your response violates our response standards. 
    Please re-answer the last user message while incorporating the changes below
    When regenerating your response, respond as if you are just answering the last user question again.
    The user will not see your previous response, so do not apologize for your mistake or reference the fact that you 
    are regenerating your response.
    
    #### CHANGES ####
    {changes}
    """
    remove_intermediate_outputs: bool = False
    max_response_regenerations: int = 10


class ValidatingCPU(AgentCPU, Specable[ValidatingCPUSpec]):
    def __init__(self, **kwargs):
        AgentCPU.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)
        if not hasattr(self.spec.cpu, 'logic_units'):
            self.spec.cpu.logic_units = []
        self.spec.cpu.logic_units.extend(self.spec.logic_units)

        self.cpu = self.spec.cpu.instantiate()
        if self.spec.remove_intermediate_outputs:
            raise RuntimeError("Unsupported Feature")
        self.env = Environment(undefined=StrictUndefined)

    async def set_boot_messages(self, *args, **kwargs):
        await self.cpu.set_boot_messages(*args, **kwargs)

    async def schedule_request(self,
                               call_context: CallContext,
                               prompts: List[CPUMessageTypes],
                               output_format: Union[Literal["str"], Dict[str, Any]],
                               ) -> Any:
        prompts_str = json.dumps(to_jsonable_python(prompts))

        validators = [self._check_input(v, prompts=prompts_str) for v in self.spec.input_validators]
        await asyncio.gather(*validators)

        resp = await self.cpu.schedule_request(call_context, prompts, output_format)
        depth = 1
        while changes := await self._get_required_changes(output_format, prompts_str, resp):
            if depth > self.spec.max_response_regenerations:
                # todo, think this through
                raise HTTPException(500)

            logger.info("Output require changes, regenerating")
            prompt = self.env.from_string(self.spec.regeneration_prompt).render(changes=changes)
            resp = await self.cpu.schedule_request(call_context, [SystemCPUMessage(prompt=prompt)], output_format)
            depth += 1
        return resp

    async def _check_input(self, v: str, prompts):
        status = await Program.get(v).execute(InputValidatorBody(prompts=prompts))
        resp = status.parse(InputValidatorResponse)
        if resp.status != "allow":
            raise HTTPException(
                status_code=409,
                detail=resp.reason or "Reqeust flagged by input validator",
            )

    async def _check_output(self, v, prompts, resp, output_format) -> OutputValidationResponse:
        status = await Program.get(v).execute(OutputValidatorBody(prompts=prompts, output_schema=output_format, response=resp))
        return status.parse(OutputValidationResponse)

    async def _get_required_changes(self, output_format, prompts, resp) -> List[str]:
        output_validators = [self._check_output(v, prompts, resp, output_format) for v in self.spec.output_validators]
        output_responses: Iterable[OutputValidationResponse] = await asyncio.gather(*output_validators)
        return [o.reason for o in output_responses if o.status != "allow"]

    async def clone_thread(self, call_context: CallContext) -> Thread:
        return await self.cpu.__class__.clone_thread(self, call_context)
