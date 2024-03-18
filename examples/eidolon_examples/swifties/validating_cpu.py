import json
from typing import Any, List, Literal, Union, Dict, Optional, AsyncIterator, Callable, Tuple

from fastapi import HTTPException
from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from eidolon_ai_client.client import Agent
from eidolon_ai_client.events import StartStreamContextEvent, OutputEvent
from eidolon_ai_client.util.stream_collector import merge_streams
from eidolon_ai_sdk.cpu.agent_cpu import AgentCPU, Thread
from eidolon_ai_sdk.cpu.agent_io import CPUMessageTypes, SystemCPUMessage
from eidolon_ai_sdk.cpu.call_context import CallContext
from eidolon_ai_sdk.cpu.logic_unit import LogicUnit
from eidolon_ai_sdk.system.reference_model import AnnotatedReference, Specable, Reference
from eidolon_ai_sdk.util.stream_collector import StreamCollector, stream_manager


class InputValidatorBody(BaseModel):
    prompts: str


class OutputValidatorBody(BaseModel):
    prompts: str
    output_schema: str | dict
    response: Any


# todo, validation rejections should probably be non 2xx
class InputValidatorResponse(BaseModel):
    status: Literal["allow", "block"]
    reason: Optional[str] = None


class OutputValidationResponse(BaseModel):
    status: Literal["allow", "regenerate"]
    reason: Optional[str] = None


class ValidatingCPUSpec(BaseModel):
    cpu: AnnotatedReference[AgentCPU]
    logic_units: List[Reference[LogicUnit]] = []
    input_validators: List[str] = []
    output_validators: List[str] = []
    regeneration_prompt: str = """
    Your response violates our response standards and the user has requested a new response. They will pretend that they
    never saw your previous response. 
    
    When regenerating your response, respond as if you are answering the question.
    Since the user will pretend they never saw your previous message, your new response should stand on its own without 
    your previous response.
    
    Do not apologize for your mistake or reference the fact that you are regenerating your response. The user would 
    prefer to forget that you made a mistake.
    
    Please re-answer the last user message while incorporating the changes below.
    #### CHANGES ####
    {changes}
    """
    remove_intermediate_outputs: bool = False
    max_response_regenerations: int = 10


class ValidatingCPU(AgentCPU, Specable[ValidatingCPUSpec]):
    def __init__(self, **kwargs):
        AgentCPU.__init__(self, **kwargs)
        Specable.__init__(self, **kwargs)
        if not hasattr(self.spec.cpu, "logic_units"):
            self.spec.cpu.logic_units = []
        self.spec.cpu.logic_units.extend(self.spec.logic_units)

        self.cpu = self.spec.cpu.instantiate()
        if self.spec.remove_intermediate_outputs:
            raise RuntimeError("Unsupported Feature")
        self.env = Environment(undefined=StrictUndefined)

    async def set_boot_messages(self, *args, **kwargs):
        await self.cpu.set_boot_messages(*args, **kwargs)

    async def schedule_request(
        self,
        call_context: CallContext,
        prompts: List[CPUMessageTypes],
        output_format: Union[Literal["str"], Dict[str, Any]],
    ) -> Any:
        prompts_str = json.dumps(to_jsonable_python(prompts))
        async for e in self._validate_input(prompts_str):
            yield e
        depth = 1
        resp_stream, resp_fn, changes_fn = self._generate_resp(call_context, depth, output_format, prompts, prompts_str)
        async for e in resp_stream:
            yield e
        while changes_fn() and depth <= self.spec.max_response_regenerations:
            prompt = self.env.from_string(self.spec.regeneration_prompt).render(changes=changes_fn())
            change_prompt = [SystemCPUMessage(prompt=prompt)]
            resp_stream, resp_fn, changes_fn = self._generate_resp(
                call_context, depth, output_format, change_prompt, prompts_str
            )
            async for e in resp_stream:
                yield e
            depth += 1
        yield OutputEvent.get(resp_fn())

    async def _validate_input(self, prompts_str):
        collectors = [self._check_input(v, prompts=prompts_str) for v in self.spec.input_validators]
        async for e in merge_streams(collectors):
            yield e
        responses = [InputValidatorResponse.model_validate(c.get_content()) for c in collectors]
        invalid_responses = [r for r in responses if r.status != "allow"]
        if invalid_responses:
            reasons = "; ".join([r.reason for r in invalid_responses if r.reason])
            raise HTTPException(
                status_code=409,
                detail=reasons or "Reqeust flagged by input validator",
            )

    def parse_action(self, agent_action: str):
        return agent_action.split(".")

    def _check_input(self, v: str, prompts) -> StreamCollector:
        [agent, action] = self.parse_action(v)
        program_stream = Agent.get(agent).stream_program(action, InputValidatorBody(prompts=prompts))
        context = StartStreamContextEvent(context_id=f"validator_{v.replace('.', '_')}")
        return stream_manager(program_stream, context)

    def _check_output(self, v, prompts, resp, output_format) -> StreamCollector:
        [agent, action] = self.parse_action(v)
        program_stream = Agent.get(agent).stream_program(
            action, OutputValidatorBody(prompts=prompts, output_schema=output_format, response=resp)
        )
        context = StartStreamContextEvent(context_id=f"validator_{v.replace('.', '_')}")
        return stream_manager(program_stream, context)

    def _generate_resp(
        self, call_context, depth, output_format, prompts, prompts_str
    ) -> Tuple[AsyncIterator, Callable, Callable]:
        acc = {}

        async def _stream():
            response = stream_manager(
                self.cpu.schedule_request(call_context, prompts, output_format),
                StartStreamContextEvent(context_id=f"proposal_{depth}"),
            )
            async for e in response:
                yield e

            validators = [
                self._check_output(v, prompts_str, response.get_content(), output_format)
                for v in self.spec.output_validators
            ]
            async for e in merge_streams(validators):
                yield e

            change_responses = [OutputValidationResponse.model_validate(c.get_content()) for c in validators]
            acc["changes"] = [c.reason for c in change_responses if c.status != "allow"]
            acc["contents"] = response.get_content()

        def _resp():
            return acc["contents"]

        def _changes():
            return acc["changes"]

        return _stream(), _resp, _changes

    async def clone_thread(self, call_context: CallContext) -> Thread:
        return await self.cpu.__class__.clone_thread(self, call_context)
