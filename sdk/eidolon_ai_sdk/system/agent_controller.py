from __future__ import annotations

import inspect
import logging
import typing
import uuid
from collections.abc import AsyncIterator
from fastapi import FastAPI, Request, HTTPException
from fastapi.params import Body, Param
from inspect import Parameter
from pydantic import BaseModel, Field, create_model
from pydantic_core import PydanticUndefined, to_jsonable_python
from sse_starlette import EventSourceResponse, ServerSentEvent
from starlette.responses import JSONResponse

from eidolon_ai_sdk.agent.agent import AgentState
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.io.events import (
    StartAgentCallEvent,
    AgentStateEvent,
    BaseStreamEvent,
    ErrorEvent,
    StringOutputEvent,
    OutputEvent,
    SuccessEvent,
    StreamEvent,
    EndStreamEvent,
    ObjectOutputEvent,
)
from eidolon_ai_sdk.system.agent_contract import SyncStateResponse, ListProcessesResponse, StateSummary
from eidolon_ai_sdk.system.fn_handler import FnHandler, get_handlers
from eidolon_ai_sdk.system.processes import ProcessDoc, store_events, load_events
from eidolon_ai_sdk.system.request_context import RequestContext
from eidolon_ai_sdk.util.logger import logger


class AgentController:
    name: str
    agent: object
    programs: typing.Dict[str, FnHandler]
    actions: typing.Dict[str, FnHandler]

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
                        "content": {"text/event-stream": {"schema": {"$ref": "#/components/schemas/EventTypes"}}},
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

        app.add_api_route(
            f"/agents/{self.name}/processes/{{process_id}}/events",
            endpoint=self.get_process_events,
            methods=["GET"],
            response_model=typing.List[typing.Dict[str, typing.Any]],
            tags=[self.name],
        )

    def stop(self, app: FastAPI):
        pass

    async def run_program(
        self,
        handler: FnHandler,
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
            process = await ProcessDoc.create(agent=self.name, state="processing")
            process_id = process.record_id
        else:
            process = await self.get_latest_process_event(process_id)
            if not process:
                raise HTTPException(status_code=404, detail="Process not found")
            if process.state not in handler.extra["allowed_states"]:
                logger.warning(
                    f"Action {handler.name} cannot process state {process.state}. Allowed states: {handler.extra['allowed_states']}"
                )
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
                try:
                    async for event in stream:
                        yield ServerSentEvent(id=str(uuid.uuid4()), data=event.model_dump_json())
                except Exception as e:
                    logger.exception(f"Server Error {e}")
                    raise e

            return EventSourceResponse(with_sse(self.agent_event_stream(handler, process, **kwargs)), status_code=200)
        else:
            # run the program synchronously
            return await self.send_response(handler, process, **kwargs)

    async def send_response(self, handler: FnHandler, process: ProcessDoc, **kwargs) -> JSONResponse:
        state_change_event = None
        final_event = None
        result_object = None
        string_result = ""
        async for event in self.agent_event_stream(handler, process, **kwargs):
            if event.is_root_and_type(StringOutputEvent):
                string_result += event.content
            elif event.is_root_and_type(ObjectOutputEvent):
                result_object = event.content
            elif event.is_root_and_type(AgentStateEvent):
                state_change_event = event
            elif event.is_root_and_type(EndStreamEvent):
                final_event = event
            else:
                logger.debug(f"ignored event {event}")

        if not state_change_event:
            raise RuntimeError(f"Did not receive state change event for {handler.name}")
        if not final_event:
            raise RuntimeError(f"Did not receive final event for {handler.name}")

        process.state = state_change_event.state
        if final_event.is_root_and_type(ErrorEvent):
            process.error_info = final_event.reason
            return self.doc_to_response(process, None)
        else:
            if result_object:
                data = result_object
            else:
                data = string_result
            return self.doc_to_response(process, data)

    async def agent_event_stream(self, handler, process, **kwargs) -> AsyncIterator[StreamEvent]:
        is_async_gen = inspect.isasyncgenfunction(handler.fn)
        stream = handler.fn(self.agent, **kwargs) if is_async_gen else self.stream_agent_fn(handler, **kwargs)
        events_to_store = []
        async for event in self.stream_agent_iterator(stream, process, handler.name):
            events_to_store.append(event)
            yield event

        await store_events(self.name, process.record_id, events_to_store)

    async def stream_agent_iterator(
        self, stream: AsyncIterator[StreamEvent], process: ProcessDoc, call_name
    ) -> AsyncIterator[StreamEvent]:
        state_change = None
        last_event = None
        try:
            yield StartAgentCallEvent(
                machine=AgentOS.current_machine_url(),
                agent_name=self.name,
                call_name=call_name,
                process_id=process.record_id,
            )
            async for event in stream:
                last_event = event
                if event.is_root_and_type(AgentStateEvent):
                    event.available_actions = self.get_available_actions(event.state)
                    state_change = event
                    await process.update(state=event.state)
                elif event.is_root_and_type(ErrorEvent):
                    logger.warning("Error event received")
                yield event

            if last_event.is_root_and_type(ErrorEvent):
                await process.update(state="unhandled_error", error_info=dict(detail=last_event.reason, status_code=500))
                yield AgentStateEvent(
                    state="unhandled_error", available_actions=self.get_available_actions("unhandled_error")
                )
            elif not state_change:
                await process.update(state="terminated")
                yield AgentStateEvent(state="terminated", available_actions=self.get_available_actions("terminated"))

            if not last_event.is_root_and_type(ErrorEvent):
                yield SuccessEvent()
        except HTTPException as e:
            logger.warning(f"HTTP Error {e}", exc_info=logger.isEnabledFor(logging.DEBUG))
            yield ErrorEvent(reason=dict(detail=e.detail, status_code=e.status_code))
            if not isinstance(last_event, AgentStateEvent):
                await process.update(state="http_error", error_info=dict(detail=e.detail, status_code=e.status_code))
                yield AgentStateEvent(state="http_error", available_actions=self.get_available_actions("http_error"))
        except Exception as e:
            logger.exception(f"Unhandled Error {e}")
            yield ErrorEvent(reason=dict(detail=str(e), status_code=500))
            if not isinstance(last_event, AgentStateEvent):
                await process.update(state="unhandled_error", error_info=dict(detail=str(e), status_code=500))
                yield AgentStateEvent(
                    state="unhandled_error", available_actions=self.get_available_actions("unhandled_error")
                )

    async def stream_agent_fn(self, handler, **kwargs) -> AsyncIterator[StreamEvent]:
        response = await handler.fn(self.agent, **kwargs)
        if isinstance(response, AgentState):
            state = response.name
            data = to_jsonable_python(response.data)
        else:
            state = "terminated"
            data = to_jsonable_python(response)

        yield OutputEvent.get(content=data)
        yield AgentStateEvent(state=state, available_actions=self.get_available_actions(state))

    def process_action(self, handler: FnHandler):
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
        if not latest_record:
            return JSONResponse(dict(detail="Process not found"), 404)
        elif (
            latest_record.state == "unhandled_error"
            or latest_record.state == "http_error"
            or latest_record.state == "error"
        ):
            detail = latest_record.error_info
            status_code = 500
            if isinstance(latest_record.error_info, dict):
                detail = latest_record.error_info.get("detail", latest_record.error_info)
                status_code = latest_record.error_info.get("status_code", 500)
            logger.info(f"Successfully retrieved stored error response, status_code={status_code}")
            return JSONResponse(detail, status_code)
        else:
            return JSONResponse(
                StateSummary(
                    process_id=latest_record.record_id,
                    state=latest_record.state,
                    available_actions=self.get_available_actions(latest_record.state),
                ).model_dump(),
                200,
            )

    async def get_process_events(self, process_id: str):
        return await load_events(self.name, process_id)

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

    def doc_to_response(self, latest_record: ProcessDoc, data: typing.Any):
        if not latest_record:
            return JSONResponse(dict(detail="Process not found"), 404)
        elif (
            latest_record.state == "unhandled_error"
            or latest_record.state == "http_error"
            or latest_record.state == "error"
        ):
            detail = latest_record.error_info
            status_code = 500
            if isinstance(latest_record.error_info, dict):
                detail = latest_record.error_info.get("detail", latest_record.error_info)
                status_code = latest_record.error_info.get("status_code", 500)
            logger.info(f"Successfully retrieved stored error response, status_code={status_code}")
            return JSONResponse(detail, status_code)
        else:
            return JSONResponse(
                SyncStateResponse(
                    process_id=latest_record.record_id,
                    state=latest_record.state,
                    data=data,
                    available_actions=self.get_available_actions(latest_record.state),
                ).model_dump(),
                200,
            )

    def get_available_actions(self, state):
        return [action for action, handler in self.actions.items() if state in handler.extra["allowed_states"]]

    @staticmethod
    async def get_latest_process_event(process_id) -> ProcessDoc:
        return await ProcessDoc.find(query=dict(_id=process_id), sort=dict(updated=-1))

    def create_response_model(self, handler: FnHandler):
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
