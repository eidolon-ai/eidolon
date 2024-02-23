from __future__ import annotations

import asyncio
import inspect
import logging
import typing
import uuid
from collections.abc import AsyncIterator
from inspect import Parameter

from fastapi import FastAPI, Request, HTTPException
from fastapi.params import Body, Param
from pydantic import BaseModel, Field, create_model
from pydantic_core import PydanticUndefined, to_jsonable_python
from sse_starlette import EventSourceResponse, ServerSentEvent
from starlette.responses import JSONResponse

from eidolon_ai_client.events import (
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
    UserInputEvent,
    CanceledEvent,
)
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.agent.agent import AgentState
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.cpu.agent_call_history import AgentCallHistory
from eidolon_ai_sdk.system.agent_contract import (
    SyncStateResponse,
    ListProcessesResponse,
    StateSummary,
    DeleteProcessResponse,
    CreateProcessArgs,
)
from eidolon_ai_sdk.system.fn_handler import FnHandler, get_handlers
from eidolon_ai_sdk.system.processes import ProcessDoc, store_events, load_events
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.util.class_utils import for_name


# todo, agent controller has become a mega impl, we should break up responsibilities
class AgentController:
    name: str
    agent: object
    actions: typing.Dict[str, FnHandler]

    def __init__(self, name, agent):
        self.name = name
        self.actions = {}
        self.agent = agent
        for handler in get_handlers(self.agent):
            if handler.name in self.actions:
                self.actions[handler.name].extra["allowed_states"] = (
                    *self.actions[handler.name].extra["allowed_states"],
                    *handler.extra["allowed_states"],
                )
            else:
                self.actions[handler.name] = handler

    async def start(self, app: FastAPI):
        logger.info(f"Starting agent '{self.name}'")
        app.add_api_route(
            f"/agents/{self.name}/processes",
            endpoint=self.list_processes,
            methods=["GET"],
            response_model=ListProcessesResponse,
            tags=[self.name],
        )

        app.add_api_route(
            f"/agents/{self.name}/processes",
            endpoint=self.create_process,
            methods=["POST"],
            response_model=StateSummary,
            tags=[self.name],
        )

        app.add_api_route(
            f"/agents/{self.name}/processes/{{process_id}}",
            endpoint=self.delete_process,
            methods=["DELETE"],
            response_model=DeleteProcessResponse,
            tags=[self.name],
        )

        app.add_api_route(
            f"/agents/{self.name}/programs",
            endpoint=self.get_programs,
            methods=["GET"],
            response_model=typing.List[str],
            tags=[self.name],
        )

        added_actions = {}
        for handler in [*self.actions.values().__reversed__()]:
            handler_name = handler.name
            path = f"/agents/{self.name}/processes/{{process_id}}/actions/{handler_name}"
            if handler_name not in added_actions:
                await self.add_route(app, handler, path, False)
                added_actions[handler_name] = path
            else:
                logger.warning(
                    f"Action {handler_name} is already registered for path {added_actions[handler_name]}. "
                    f"Skipping registration for path {path}"
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

    async def add_route(self, app, handler, path, isEndpointAProgram: bool):
        endpoint = self.process_action(handler, isEndpointAProgram)
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

    async def stop(self, app: FastAPI):
        pass

    async def run_program(
            self,
            handler: FnHandler,
            process_id: typing.Optional[str] = None,
            **kwargs,
    ):
        request = typing.cast(Request, kwargs.pop("__request"))
        if not process_id:
            if "initialized" not in handler.extra["allowed_states"]:
                raise HTTPException(
                    status_code=400,
                    detail=f'Action "{handler.name}" is not an initializer, but no process_id was provided',
                )
            last_state = "initialized"
            process = await self._create_process(state="processing")
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
            last_state = process.state
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

            return EventSourceResponse(
                with_sse(self.agent_event_stream(handler, process, last_state, **kwargs)), status_code=200
            )
        else:
            # run the program synchronously
            return await self.send_response(handler, process, last_state, **kwargs)

    async def _create_process(self, **kwargs):
        process = await ProcessDoc.create(agent=self.name, **kwargs)
        if hasattr(self.agent, "create_process"):
            await self.agent.create_process(process.record_id)
        return process

    async def send_response(self, handler: FnHandler, process: ProcessDoc, last_state: str, **kwargs) -> JSONResponse:
        state_change_event = None
        final_event = None
        result_object = None
        string_result = ""
        async for event in self.agent_event_stream(handler, process, last_state, **kwargs):
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

    async def agent_event_stream(self, handler, process, last_state, **kwargs) -> AsyncIterator[StreamEvent]:
        is_async_gen = inspect.isasyncgenfunction(handler.fn)
        stream = handler.fn(self.agent, **kwargs) if is_async_gen else self.stream_agent_fn(handler, **kwargs)
        events_to_store = []
        ended = False
        transitioned = False
        try:
            async for event in self.stream_agent_iterator(stream, process, handler.name, kwargs):
                if not ended:
                    ended = event.is_root_end_event()
                    transitioned = event.is_root_and_type(AgentStateEvent)
                    if (
                            isinstance(event, StringOutputEvent)
                            and events_to_store
                            and isinstance(events_to_store[-1], StringOutputEvent)
                            and event.stream_context == events_to_store[-1].stream_context
                    ):
                        events_to_store[-1].content += event.content
                    else:
                        events_to_store.append(event)
                    yield event
                else:
                    logger.warning(f"Received event after end event ({event.event_type}), ignoring")
        except asyncio.CancelledError:
            logger.info(f"Process {process.record_id} was cancelled")
            if not ended:
                if not transitioned:
                    await process.update(state=last_state)
                    actions = self.get_available_actions(last_state)
                    events_to_store.append(AgentStateEvent(state=last_state, available_actions=actions))
                events_to_store.append(CanceledEvent())

            raise
        finally:
            await store_events(self.name, process.record_id, events_to_store)

    async def stream_agent_iterator(
            self,
            stream: AsyncIterator[StreamEvent],
            process: ProcessDoc,
            call_name,
            user_input: typing.Dict[str, typing.Any],
    ) -> AsyncIterator[StreamEvent]:
        state_change = None
        seen_end = False
        try:
            yield UserInputEvent(input=to_jsonable_python(user_input, fallback=str))
            yield StartAgentCallEvent(
                machine=AgentOS.current_machine_url(),
                agent_name=self.name,
                call_name=call_name,
                process_id=process.record_id,
            )
            async for event in stream:
                if event.is_root_and_type(ErrorEvent):
                    logger.warning("Error event received")
                if not seen_end:
                    seen_end = event.is_root_end_event()
                    if event.is_root_and_type(AgentStateEvent):
                        state_change = True
                        event.available_actions = self.get_available_actions(event.state)
                        await process.update(state=event.state)
                    yield event
                else:
                    logger.warning(f"Received event after end event ({event.event_type}), ignoring")
            if not state_change:
                await process.update(state="terminated")
                yield AgentStateEvent(state="terminated", available_actions=self.get_available_actions("terminated"))
            if not seen_end:
                yield SuccessEvent()
        except HTTPException as e:
            logger.warning(f"HTTP Error {e}", exc_info=logger.isEnabledFor(logging.DEBUG))
            if not seen_end:
                await process.update(state="http_error", error_info=dict(detail=e.detail, status_code=e.status_code))
                yield AgentStateEvent(state="http_error", available_actions=self.get_available_actions("http_error"))
                yield ErrorEvent(reason=dict(detail=e.detail, status_code=e.status_code))
        except Exception as e:
            logger.exception(f"Unhandled Error {e}")
            if not seen_end:
                await process.update(state="unhandled_error", error_info=dict(detail=str(e), status_code=500))
                yield AgentStateEvent(
                    state="unhandled_error", available_actions=self.get_available_actions("unhandled_error")
                )
                yield ErrorEvent(reason=dict(detail=str(e), status_code=500))

    async def stream_agent_fn(self, handler, **kwargs) -> AsyncIterator[StreamEvent]:
        response = await handler.fn(self.agent, **kwargs)
        if isinstance(response, AgentState):
            yield OutputEvent.get(content=to_jsonable_python(response.data))
            yield AgentStateEvent(state=response.name, available_actions=self.get_available_actions(response.name))
        else:
            yield OutputEvent.get(content=to_jsonable_python(to_jsonable_python(response)))

    def process_action(self, handler: FnHandler, isEndpointAProgram: bool):
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
            if isEndpointAProgram:
                del params["process_id"]
            else:
                replace: Parameter = params["process_id"].replace(annotation=str)
                params["process_id"] = replace
        elif not isEndpointAProgram:
            params["process_id"] = Parameter("process_id", Parameter.KEYWORD_ONLY, annotation=str)

        del params["self"]

        params["__request"] = Parameter("__request", Parameter.KEYWORD_ONLY, annotation=Request)
        params_values = [v for v in params.values() if v.kind != Parameter.VAR_KEYWORD]

        async def _run_program(**_kwargs):
            return await self.run_program(handler, **_kwargs)

        _run_program.__signature__ = sig.replace(parameters=params_values, return_annotation=typing.Any)
        return _run_program

    async def get_programs(self):
        """
        Get the operations that are available for this agent that can be run from the initial state
        """
        programs = []
        for handler in [*self.actions.values().__reversed__()]:
            handler_name = handler.name
            if "initialized" in handler.extra["allowed_states"]:
                programs.append(handler_name)

        return JSONResponse(programs, 200)

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

    async def create_process(self, args: CreateProcessArgs = CreateProcessArgs()):
        """
        Create a new process. Use this method first to get a process id before calling any other action
        :param args: An optional title for the process
        :return:
        """
        process = await self._create_process(state="initialized", title=args.title)
        return JSONResponse(
            StateSummary(
                process_id=process.record_id,
                state=process.state,
                available_actions=self.get_available_actions(process.state),
            ).model_dump(),
            200,
        )

    async def delete_process(self, process_id: str):
        """
        Delete a process and all of its children
        """
        process_obj = await ProcessDoc.find_one(query={"_id": process_id})
        num_delete = await self._delete_process(process_id) if process_obj else 0
        return JSONResponse(
            DeleteProcessResponse(process_id=process_id, deleted=num_delete).model_dump(), 200 if num_delete > 0 else 204
        )

    async def _delete_process(self, process_id: str):
        num_deleted = 0
        async for child in AgentCallHistory.get_children(process_id):
            num_deleted += await self._delete_process(child)
        await AgentCallHistory.delete(query={"parent_process_id": process_id})
        logger.info(f"Successfully deleted child processes for process {process_id}")

        references = AgentOS.get_resources(ReferenceResource).values()
        agents = AgentOS.get_resources(AgentResource).values()
        for r in (*agents, *references):
            implementation = to_jsonable_python(r.spec)["implementation"]
            is_root = not AgentOS.get_resource(ReferenceResource, implementation, default=None)
            if is_root:
                resource_class = for_name(implementation)
                if hasattr(resource_class, "delete_process"):
                    await resource_class.delete_process(process_id)
                    logger.info(f"Successfully {resource_class.__name__} records associated with process {process_id}")
                else:
                    logger.debug(f"No deletion hook for {resource_class}")
            else:
                logger.debug(f"Skipping non root reference {r.metadata.name}")

        await ProcessDoc.delete(_id=process_id)
        return num_deleted + 1

    async def list_processes(
            self,
            request: Request,
            limit: int = 20,
            skip: int = 0,
            sort: typing.Literal["ascending", "descending"] = "ascending",
    ):
        """
        List all processes for this agent. Supports paging and sorting
        """
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

    async def get_latest_process_event(self, process_id) -> ProcessDoc:
        return await ProcessDoc.find_one(query=dict(_id=process_id, agent=self.name), sort=dict(updated=-1))

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
