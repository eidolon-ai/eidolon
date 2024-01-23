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
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from starlette.responses import JSONResponse

from eidos_sdk.agent.agent import AgentState
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.io.events import StartAgentCallEvent, EndAgentCallEvent, with_context, AgentStateEvent, BaseStreamEvent, ErrorEvent
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
            # from bson import ObjectId
            # response_name = f"Response_200_{ObjectId()}"
            # response_field = create_response_field(name=response_name, type_=self.create_response_model(handler))
            # _example = response_field.get_default()

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

        if inspect.isasyncgenfunction(handler.fn):
            # todo -- handle the case if the user doesn't want to stream
            return self.stream_response(handler, process, **kwargs)
        else:
            state = await self.run_sync_call(handler, process, **kwargs)
            return self.doc_to_response(state)

    def stream_response(self, handler: EidosHandler, process: ProcessDoc, **kwargs):
        process_id = kwargs.get("process_id")

        async def stream_response_data(**additional_kwargs):
            next_state = None
            last_event = None
            yield StartAgentCallEvent(agent_name=self.name, call_name=handler.name, process_id=process_id, stream_context=[])
            try:
                call_context = f"{self.name}.{handler.name}"
                async for event in with_context(call_context, handler.fn(self.agent, **additional_kwargs)):
                    last_event = event
                    if isinstance(event, AgentStateEvent):
                        next_state = event.state
                    else:
                        yield event

                if last_event and isinstance(last_event, ErrorEvent):
                    next_state = "unhandled_error"
                elif not next_state:
                    next_state = "terminated"

                yield AgentStateEvent(state=next_state, available_actions=self.get_available_actions(next_state), stream_context=[])
                yield EndAgentCallEvent(stream_context=[])
            except Exception as e:
                next_state = "unhandled_error"
                yield ErrorEvent(reason=e, stream_context=[])

            await process.update(
                state=next_state,
                data=dict(data="<stream>"),
            )

        async def with_sse(stream: AsyncIterator[BaseStreamEvent]):
            async for event in stream:
                yield ServerSentEvent(id=str(uuid.uuid4()), data=event.model_dump_json())

        return EventSourceResponse(with_sse(stream_response_data(**kwargs)), status_code=200)

    async def run_sync_call(self, handler: EidosHandler = None, process: ProcessDoc = None, **kwargs):
        try:
            response = await handler.fn(self.agent, **kwargs)
            if isinstance(response, AgentState):
                state = response.name
                data = to_jsonable_python(response.data)
            else:
                state = "terminated"
                data = to_jsonable_python(response)
            doc = await process.update(
                state=state,
                data=data,
            )
        except HTTPException as e:
            doc = await process.update(
                state="http_error",
                data=dict(detail=e.detail, status_code=e.status_code),
            )
            if e.status_code >= 500:
                logging.exception("Unhandled error raised by handler")
            else:
                logging.debug(f"Handler {handler.name} raised a http error", exc_info=True)
        except Exception as e:
            doc = await process.update(
                state="unhandled_error",
                data=dict(error=str(e)),
            )
            logging.exception("Unhandled error raised by handler")
        return doc

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
