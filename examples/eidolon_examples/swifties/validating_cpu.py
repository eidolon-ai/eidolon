import asyncio
import json
from typing import Any, List, Literal, Union, Dict, Optional, AsyncIterator, Callable, Tuple

from aiostream import stream
from fastapi import HTTPException
from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from eidos_sdk.agent.client import Program
from eidos_sdk.cpu.agent_cpu import AgentCPU, Thread
from eidos_sdk.cpu.agent_io import CPUMessageTypes, SystemCPUMessage
from eidos_sdk.cpu.call_context import CallContext
from eidos_sdk.cpu.logic_unit import LogicUnit
from eidos_sdk.io.events import StartStreamContextEvent, OutputEvent
from eidos_sdk.system.reference_model import AnnotatedReference, Specable, Reference
from eidos_sdk.util.stream_collector import StreamCollector


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

        depth = 1
        resp_stream, resp_fn, changes_fn = self._generate_resp(call_context, depth, output_format, prompts, prompts_str)
        async for e in resp_stream:
            yield e
        while changes_fn() and depth <= self.spec.max_response_regenerations:
            prompt = self.env.from_string(self.spec.regeneration_prompt).render(changes=changes_fn())
            change_prompt = [SystemCPUMessage(prompt=prompt)]
            resp_stream, resp_fn, changes_fn = self._generate_resp(call_context, depth, output_format, change_prompt, prompts_str)
            async for e in resp_stream:
                yield e
            depth += 1
        yield OutputEvent.get(resp_fn())

    async def _check_input(self, v: str, prompts):
        status = await Program.get(v).execute(InputValidatorBody(prompts=prompts))
        resp = status.parse(InputValidatorResponse)
        if resp.status != "allow":
            raise HTTPException(
                status_code=409,
                detail=resp.reason or "Reqeust flagged by input validator",
            )

    def _check_output(self, v, prompts, resp, output_format) -> StreamCollector:
        program_stream = Program.get(v).stream_execute(OutputValidatorBody(prompts=prompts, output_schema=output_format, response=resp))
        context = StartStreamContextEvent(context_id=f"validator_{v.replace('.', '_')}")
        return StreamCollector(stream=program_stream, wrap_with_context=context)

    def _generate_resp(self, call_context, depth, output_format, prompts, prompts_str) -> Tuple[AsyncIterator, Callable, Callable]:
        acc = {}
        async def _stream():
            collector = StreamCollector(
                stream=self.cpu.schedule_request(call_context, prompts, output_format),
                wrap_with_context=StartStreamContextEvent(context_id=f"proposal_{depth}")
            )
            async for e in collector:
                yield e
            if self.spec.output_validators:
                change_collectors = [
                    self._check_output(v, prompts_str, collector.contents, output_format)
                    for v in self.spec.output_validators
                ]
                async for e in stream.merge(change_collectors[0], *change_collectors[1:]):
                    yield e
            else:
                change_collectors = []

            change_responses = [OutputValidationResponse.model_validate(c.contents) for c in change_collectors]
            acc['changes'] = [c.contents for c in change_responses if c.status != "allow"]
            acc['contents'] = collector.contents

        def _resp():
            return acc['contents']
        def _changes():
            return acc['changes']
        return _stream(), _resp, _changes

    async def clone_thread(self, call_context: CallContext) -> Thread:
        return await self.cpu.__class__.clone_thread(self, call_context)
