from __future__ import annotations

import inspect
import typing
import uuid
from collections.abc import AsyncIterator
from inspect import Parameter

from fastapi import FastAPI, Request, HTTPException
from fastapi.params import Body, Param
from pydantic import BaseModel, Field, create_model
from pydantic_core import PydanticUndefined, to_jsonable_python
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from starlette.responses import JSONResponse

from eidos_sdk.agent.agent import AgentState
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.io.events import StartAgentCallEvent, with_context, AgentStateEvent, BaseStreamEvent, \
    ErrorEvent, StringOutputEvent, OutputEvent, SuccessEvent, StreamEvent, EndStreamEvent
from eidos_sdk.system.agent_contract import SyncStateResponse, ListProcessesResponse, StateSummary
from eidos_sdk.system.eidos_handler import EidosHandler, get_handlers
from eidos_sdk.system.processes import ProcessDoc
from eidos_sdk.system.request_context import RequestContext
from eidos_sdk.util.logger import logger


class AgentController:
    name: str
    agent: object
    programs: typing.Dict[str, EidosHandler]
    actions: typing.Dict[str, EidosHandler]

    def __init__(self, name, agent):
        self.name = name
        self.programs = {}
        self.actions = {}
        self.agent = agent
        for handler in get_handlers(self.agent):
            if handler.extra["type"] == "program":
                self.programs[handler.name] = handler
            else:
                self.actions[handler.name] = handler

    async def start(self, app: FastAPI):
        logger.info(f"Starting agent '{self.name}'")
        for handler in [*self.programs.values(), *self.actions.values().__reversed__()]:
            path = f"/agents/{self.name}"
            handler_name = handler.name
            if handler.extra["type"] == "program":
                path += f"/programs/{handler_name}"
            else:
                path += f"/processes/{{process_id}}/actions/{handler_name}"
            endpoint = self.process_action(handler)
            app.add_api_route(
                path,
                endpoint=endpoint,
                methods=["POST"],
                tags=[self.name],
                responses={
                    200: {
                        "model": self.create_response_model(handler),
                        "content": {
                            "text/event-stream": {
                                "schema": {
                                    "$ref": "#/components/schemas/EventTypes"
                                }
                            }
                        }
                    },
                },
                description=handler.description(self.agent, handler),
            )

        app.add_api_route(
            f"/agents/{self.name}/processes",
            endpoint=self.list_processes,
            methods=["GET"],
            response_model=ListProcessesResponse,
            tags=[self.name],
        )

        app.add_api_route(
            f"/agents/{self.name}/processes/{{process_id}}/status",
            endpoint=self.get_process_info,
            methods=["GET"],
            response_model=SyncStateResponse,
            tags=[self.name],
        )

    def stop(self, app: FastAPI):
        pass

    async def run_program(
            self,
            handler: EidosHandler,
            process_id: typing.Optional[str] = None,
            **kwargs,
    ):
        request = typing.cast(Request, kwargs.pop("__request"))
        if not process_id:
            if not handler.extra["type"] == "program":
                raise HTTPException(
                    status_code=400,
                    detail=f'Action "{handler.name}" is not an initializer, but no process_id was provided',
                )
            process = await ProcessDoc.create(agent=self.name, state="processing", data=dict(action=handler.name))
            process_id = process.record_id
        else:
            process = await self.get_latest_process_event(process_id)
            if not process:
                raise HTTPException(status_code=404, detail="Process not found")
            if process.state not in handler.extra["allowed_states"]:
                logger.warn(f"Action {handler.name} cannot process state {process.state}. Allowed states: {handler.extra['allowed_states']}")
                raise HTTPException(
                    status_code=409,
                    detail=f'Action "{handler.name}" cannot process state "{process.state}"',
                )
            process = await process.update(
                agent=self.name, record_id=process_id, state="processing", data=dict(action=handler.name)
            )
        RequestContext.set("process_id", process_id)

        if "process_id" in dict(inspect.signature(handler.fn).parameters):
            kwargs["process_id"] = process_id

        # get the accepted content types
        accept_header = request.headers.get("Accept")
        media_types = accept_header.split(",") if accept_header else []
        try:
            event_stream_idx = media_types.index("text/event-stream")
        except ValueError:
            event_stream_idx = -1

        try:
            app_json_idx = media_types.index("application/json")
        except ValueError:
            app_json_idx = -1

        if event_stream_idx != -1 and (app_json_idx == -1 or event_stream_idx < app_json_idx):
            # stream the results
            async def with_sse(stream: AsyncIterator[BaseStreamEvent]):
                async for event in stream:
                    yield ServerSentEvent(id=str(uuid.uuid4()), data=event.model_dump_json())

            return EventSourceResponse(with_sse(self.agent_event_stream(handler, process, **kwargs)), status_code=200)
        else:
            # run the program synchronously
            return await self.send_response(handler, process, **kwargs)

    def agent_event_stream(self, handler, process, **kwargs) -> AsyncIterator[StreamEvent]:
        if inspect.isasyncgenfunction(handler.fn):
            stream = self.stream_agent_fn(handler, process, **kwargs)
        else:
            stream = self.stream_async_agent_fn(handler, process, **kwargs)
        call_context = f"{self.name}.{handler.name}"
        return with_context(call_context, stream)

    async def send_response(self, handler: EidosHandler, process: ProcessDoc, **kwargs) -> JSONResponse:
        start_event = None
        output_event: typing.Optional[OutputEvent] = None
        state_change_event = None
        final_event = None
        async for event in self.agent_event_stream(handler, process, **kwargs):
            if isinstance(event, StartAgentCallEvent):
                if start_event:
                    raise RuntimeError(f"Received multiple start agent events: {event}")
                start_event = event

            else:
                if not start_event:
                    raise RuntimeError(f"Received event {event} before start agent event")
                if event.stream_context == start_event.stream_context:
                    if isinstance(event, AgentStateEvent):
                        state_change_event = event
                    elif isinstance(event, EndStreamEvent):
                        final_event = event
                    elif isinstance(event, OutputEvent) and not output_event:
                        output_event = event
                    elif isinstance(event, StringOutputEvent):
                        output_event.content += event.content

        if not output_event:
            raise RuntimeError(f"Did not receive output event for {handler.name}")
        if not state_change_event:
            raise RuntimeError(f"Did not receive state change event for {handler.name}")
        if not final_event:
            raise RuntimeError(f"Did not receive final event for {handler.name}")

        process.state = state_change_event.state
        process.data = output_event.content
        return self.doc_to_response(process)

    async def stream_agent_fn(self, handler: EidosHandler, process: ProcessDoc, **kwargs) -> AsyncIterator[StreamEvent]:
        next_state = None
        last_event = None
        yield StartAgentCallEvent(agent_name=self.name, call_name=handler.name, process_id=process.record_id)
        try:
            async for event in handler.fn(self.agent, **kwargs):
                last_event = event
                # todo, we can update record in mongo here
                if isinstance(event, AgentStateEvent):
                    next_state = event.state
                else:
                    yield event

            if last_event and isinstance(last_event, ErrorEvent):
                next_state = "unhandled_error"
            elif not next_state:
                next_state = "terminated"

            yield SuccessEvent()
        except Exception as e:
            next_state = "unhandled_error"
            yield ErrorEvent(reason=e)

        await process.update(
            state=next_state,
            data=dict(data="<stream>"),
        )
        yield AgentStateEvent(state=next_state, available_actions=self.get_available_actions(next_state))

    async def stream_async_agent_fn(self, handler, process, **kwargs) -> AsyncIterator[StreamEvent]:
        state = "unhandled_error"
        data = "<stream>"
        try:
            yield StartAgentCallEvent(agent_name=self.name, call_name=handler.name, process_id=process.record_id)

            response = await handler.fn(self.agent, **kwargs)
            if isinstance(response, AgentState):
                state = response.name
                data = to_jsonable_python(response.data)
            else:
                state = "terminated"
                data = to_jsonable_python(response)

            yield OutputEvent.get(content=data)
            yield SuccessEvent()
        except HTTPException as e:
            logger.warning(f"HTTP error {e.status_code} from {handler.name}", exc_info=True)
            state = "http_error"
            data = dict(detail=e.detail, status_code=e.status_code)
            yield ErrorEvent(reason=data)
        except Exception as e:
            logger.error(f"Unhandled error from {handler.name}", exc_info=True)
            state = "unhandled_error"
            data = str(e)
            yield ErrorEvent(reason=data)
        finally:
            await process.update(state=state, data=data)
            yield AgentStateEvent(state=state, available_actions=self.get_available_actions(state))

    def process_action(self, handler: EidosHandler):
        logger.debug(f"Registering action {handler.name} for program {self.name}")
        sig = inspect.signature(handler.fn)
        params = dict(sig.parameters)
        model: typing.Type[BaseModel] = handler.input_model_fn(self.agent, handler)
        for field in model.model_fields:
            kwargs = dict(annotation=model.model_fields[field].annotation)
            if isinstance(model.model_fields[field], Body) or isinstance(model.model_fields[field], Param):
                kwargs["annotation"] = typing.Annotated[model.model_fields[field].annotation, model.model_fields[field]]
            if model.model_fields[field].default is not PydanticUndefined:
                kwargs["default"] = model.model_fields[field].default

            params[field] = Parameter(field, Parameter.KEYWORD_ONLY, **kwargs)
        if "process_id" in params:
            if handler.extra["type"] == "program":
                del params["process_id"]
            else:
                replace: Parameter = params["process_id"].replace(annotation=str)
                params["process_id"] = replace
        elif handler.extra["type"] == "action":
            params["process_id"] = Parameter("process_id", Parameter.KEYWORD_ONLY, annotation=str)

        del params["self"]

        params["__request"] = Parameter("__request", Parameter.KEYWORD_ONLY, annotation=Request)
        params_values = [v for v in params.values() if v.kind != Parameter.VAR_KEYWORD]

        async def _run_program(**_kwargs):
            return await self.run_program(handler, **_kwargs)

        _run_program.__signature__ = sig.replace(parameters=params_values, return_annotation=typing.Any)
        return _run_program

    async def get_process_info(self, process_id: str):
        latest_record = await self.get_latest_process_event(process_id)
        return self.doc_to_response(latest_record)

    async def list_processes(
            self,
            request: Request,
            limit: int = 20,
            skip: int = 0,
            sort: typing.Literal["ascending", "descending"] = "ascending",
    ):
        query = dict(agent=self.name)
        count = await AgentOS.symbolic_memory.count(ProcessDoc.collection, query)
        cursor = AgentOS.symbolic_memory.find(
            ProcessDoc.collection, query, sort=dict(updated=1 if sort == "ascending" else -1), skip=skip
        )
        acc = []
        async for doc in cursor:
            process = ProcessDoc.model_validate(doc)
            acc.append(
                StateSummary(
                    process_id=process.record_id,
                    state=process.state,
                    available_actions=self.get_available_actions(process.state),
                )
            )
            if len(acc) == limit:
                break
        if len(acc) + skip <= count:
            next_page_url = f"{request.url}agents/{self.name}/processes/?limit={limit}&skip={skip + limit}"
        else:
            next_page_url = None
        return JSONResponse(
            ListProcessesResponse(
                total=count,
                processes=acc,
                next=next_page_url,
            ).model_dump(),
            200,
        )

    def doc_to_response(self, latest_record: ProcessDoc):
        if not latest_record:
            return JSONResponse(dict(detail="Process not found"), 404)
        elif latest_record.state == "unhandled_error":
            return JSONResponse(latest_record.data, 500)
        elif latest_record.state == "http_error":
            return JSONResponse(
                dict(detail=latest_record.data["detail"]),
                latest_record.data["status_code"],
            )
        else:
            return JSONResponse(
                SyncStateResponse(
                    process_id=latest_record.record_id,
                    state=latest_record.state,
                    data=latest_record.data,
                    available_actions=self.get_available_actions(latest_record.state),
                ).model_dump(),
                200,
            )

    def get_available_actions(self, state):
        return [action for action, handler in self.actions.items() if state in handler.extra["allowed_states"]]

    @staticmethod
    async def get_latest_process_event(process_id) -> ProcessDoc:
        return await ProcessDoc.find(query=dict(_id=process_id), sort=dict(updated=-1))

    def create_response_model(self, handler: EidosHandler):
        # if we want, we can calculate the literal state and allowed actions statically for most actions. Not for now though.
        fields = {key: (fieldinfo.annotation, fieldinfo) for key, fieldinfo in SyncStateResponse.model_fields.items()}
        return_type = handler.output_model_fn(self.agent, handler)
        if inspect.isclass(return_type) and issubclass(return_type, AgentState):
            return_type = return_type.model_fields["data"].annotation
        fields["data"] = (
            return_type,
            Field(..., description=fields["data"][1].description),
        )
        return create_model(f"{handler.name.capitalize()}ResponseModel", **fields)
