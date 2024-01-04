from __future__ import annotations

import inspect
import logging
import typing
from inspect import Parameter

from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.params import Body, Param
from pydantic import BaseModel, Field, create_model
from pydantic_core import PydanticUndefined
from starlette.responses import JSONResponse

from eidos_sdk.agent.agent import AgentState
from eidos_sdk.agent_os import AgentOS
from eidos_sdk.system.agent_contract import SyncStateResponse, AsyncStateResponse, ListProcessesResponse, StateSummary
from eidos_sdk.system.eidos_handler import EidosHandler, get_handlers
from eidos_sdk.system.processes import ProcessDoc
from eidos_sdk.util.json_util import model_to_json
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
                    202: {"model": AsyncStateResponse},
                    200: {"model": self.create_response_model(handler)},
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

    # todo, unregister routes
    def stop(self, app: FastAPI):
        pass

    async def restart(self, app: FastAPI):
        self.stop(app)
        await self.start(app)

    def process_action(self, handler: EidosHandler):
        async def run_program(
            request: Request,
            background_tasks: BackgroundTasks,
            process_id: typing.Optional[str] = None,
            **kwargs,
        ):
            callback = request.headers.get("callback-url")
            execution_mode = request.headers.get("execution-mode", "async" if callback else "sync").lower()

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
                    raise HTTPException(
                        status_code=409,
                        detail=f'Action "{handler.name}" cannot process state "{process.state}"',
                    )
                process = await process.update(
                    agent=self.name, record_id=process_id, state="processing", data=dict(action=handler.name)
                )

            async def run_and_store_response():
                try:
                    sig = inspect.signature(handler.fn)
                    if "process_id" in dict(sig.parameters):
                        kwargs["process_id"] = process_id
                    response = await handler.fn(self.agent, **kwargs)
                    if isinstance(response, AgentState):
                        state = response.name
                        data = model_to_json(response.data)
                    else:
                        state = "terminated"
                        data = model_to_json(response)
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
                if callback:
                    raise Exception("Not implemented")
                return doc

            if execution_mode == "sync":
                state = await run_and_store_response()
                return self.doc_to_response(state)
            else:
                background_tasks.add_task(run_and_store_response)
                return JSONResponse(AsyncStateResponse(process_id=process_id).model_dump(), 202)

        logger.debug(f"Registering action {handler.name} for program {self.name}")
        sig = inspect.signature(run_program)
        params = dict(sig.parameters)
        model: typing.Type[BaseModel] = handler.input_model_fn(self.agent, handler)
        for field in model.model_fields:
            kwargs = dict(annotation=model.model_fields[field].annotation)
            if isinstance(model.model_fields[field], Body) or isinstance(model.model_fields[field], Param):
                kwargs["annotation"] = typing.Annotated[model.model_fields[field].annotation, model.model_fields[field]]
            if model.model_fields[field].default is not PydanticUndefined:
                kwargs["default"] = model.model_fields[field].default

            params[field] = Parameter(field, Parameter.KEYWORD_ONLY, **kwargs)
        if handler.extra["type"] == "program":
            del params["process_id"]
        else:
            replace: Parameter = params["process_id"].replace(annotation=str)
            params["process_id"] = replace
        del params["kwargs"]
        run_program.__signature__ = sig.replace(parameters=params.values())
        return run_program

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
