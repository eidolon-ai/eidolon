from __future__ import annotations

import importlib
import inspect
import typing
from datetime import datetime

from bson import ObjectId
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field, create_model
from starlette.responses import JSONResponse

from .agent import Agent, AgentState, ProcessContext
from .agent_memory import SymbolicMemory
from .agent_os import AgentOS
from .agent_program import AgentProgram
from .util.dynamic_endpoint import create_endpoint_with_process_id, create_endpoint_without_process_id


class AsyncStateResponse(BaseModel):
    process_id: str = Field(..., description="The ID of the conversation.")


class SyncStateResponse(AsyncStateResponse):
    state: str = Field(..., description="The state of the conversation.")
    data: typing.Any = Field(..., description="The data returned by the last state change.")
    available_actions: typing.List[str] = Field(..., description="The actions available from the current state.")


class AgentProcess:
    agent: Agent
    agent_program: AgentProgram
    agent_os: AgentOS

    def __init__(self, agent_program: AgentProgram, agent_os: AgentOS):
        self.agent_program = agent_program
        self.agent_os = agent_os

    def start(self, app: FastAPI):
        # First create the Agent implementation
        module_name, class_name = self.agent_program.implementation.rsplit(".", 1)
        module = importlib.import_module(module_name)
        impl_class = getattr(module, class_name)

        self.agent = impl_class(self, agent_machine=self.agent_os.machine)

        for action, handler in self.agent.action_handlers.items():
            path = f"/programs/{self.agent_program.name}"
            if action == 'INIT':
                endpoint = create_endpoint_without_process_id(self.agent.get_input_model(action), self.process_action(action))
            else:
                path += f"/processes/{{process_id}}/actions/{action}"
                endpoint = create_endpoint_with_process_id(self.agent.get_input_model(action), self.process_action(action))
            app.add_api_route(path, endpoint=endpoint, methods=["POST"], tags=[self.agent_program.name], responses={
                202: {"model": AsyncStateResponse},
                200: {'model': self.create_response_model(action)},
            })

        app.add_api_route(
            f"/programs/{self.agent_program.name}/processes/{{process_id}}/status",
            endpoint=self.get_process_info,
            methods=["GET"],
            response_model=SyncStateResponse,
            tags=[self.agent_program.name],
        )

    def stop(self, app: FastAPI):
        pass

    def restart(self, app: FastAPI):
        self.stop(app)
        self.start(app)

    # todo, defining this on agents and then handling the dynamic function call will give flexibility to define request body
    def process_action(self, action: str):
        async def processStateRoute(
                request: Request,
                body: BaseModel,
                process_id: typing.Optional[str],
                background_tasks: BackgroundTasks,
        ):
            print(action)
            print(body)
            memory: SymbolicMemory = self.agent_os.machine.agent_memory.symbolic_memory
            callback = request.headers.get('callback-url')
            execution_mode = request.headers.get('execution-mode', 'async' if callback else 'sync').lower()

            if not process_id:
                process_id = str(ObjectId())
                state = 'UNINITIALIZED'
            else:
                found = await self.get_latest_process_event(process_id)
                if not found:
                    raise HTTPException(status_code=404, detail="Process not found")
                state = found['state']

            handler = self.agent.action_handlers[action]
            if state not in handler.allowed_states:
                raise HTTPException(status_code=409, detail=f"Action \"{action}\" cannot process state \"{state}\"")

            state = dict(process_id=process_id, state="processing", data=dict(action=action, body=body.model_dump()),
                         date=str(datetime.now().isoformat()))
            await memory.insert_one('processes', state)

            async def run_and_store_response():
                try:
                    response = await handler.fn(self.agent, **body.model_dump())
                    if isinstance(response, AgentState):
                        state = response.name
                        data = response.data.model_dump() if isinstance(response.data, BaseModel) else response.data
                    else:
                        state = 'terminated'
                        data = response.model_dump() if isinstance(response, BaseModel) else response
                    doc = dict(process_id=process_id, state=state, data=data, date=str(datetime.now().isoformat()))
                except HTTPException as e:
                    doc = dict(
                        process_id=process_id,
                        state="http_error",
                        data=dict(detail=e.detail, status_code=e.status_code),
                        date=str(datetime.now().isoformat())
                    )
                    print(e)
                except Exception as e:
                    doc = dict(
                        process_id=process_id,
                        state="unhandled_error",
                        data=dict(error=str(e)),
                        date=str(datetime.now().isoformat())
                    )
                    print(e)
                await memory.insert_one('processes', doc)
                if callback:
                    raise Exception("Not implemented")
                return doc

            self.agent.process_context.set(ProcessContext(process_id=process_id, callback_url=callback))
            if execution_mode == 'sync':
                state = await run_and_store_response()
                return self.doc_to_response(state)
            else:
                background_tasks.add_task(run_and_store_response)
                return JSONResponse(AsyncStateResponse(process_id=process_id).model_dump(), 202)

        return processStateRoute

    async def get_process_info(self, process_id: str):
        latest_record = await self.get_latest_process_event(process_id)
        return self.doc_to_response(latest_record)

    def doc_to_response(self, latest_record: dict):
        if not latest_record:
            return JSONResponse(dict(detail="Process not found"), 404)
        elif latest_record['state'] == 'unhandled_error':
            return JSONResponse(latest_record['data'], 500)
        elif latest_record['state'] == 'http_error':
            return JSONResponse(dict(detail=latest_record['data']['detail']), latest_record['data']['status_code'])
        else:
            try:
                del latest_record['_id']
            except KeyError:
                pass
            return JSONResponse(SyncStateResponse(
                process_id=latest_record['process_id'],
                state=latest_record['state'],
                data=latest_record['data'],
                available_actions=[
                    action for action, handler in self.agent.action_handlers.items() if latest_record['state'] in handler.allowed_states
                ],
            ).model_dump(), 200)

    async def get_latest_process_event(self, process_id):
        # todo, memory needs to include sorting
        latest_record = None
        memory: SymbolicMemory = self.agent_os.machine.agent_memory.symbolic_memory
        records = memory.find('processes', dict(process_id=process_id))
        async for record in records:
            if not latest_record or record['date'] > latest_record['date']:
                latest_record = record
        return latest_record

    def create_response_model(self, action: str):
        # if we want, we can calculate the literal state and allowed actions statically for most actions. Not for now though.
        fields = {key: (fieldinfo.annotation, fieldinfo) for key, fieldinfo in SyncStateResponse.model_fields.items()}
        return_type = self.agent.get_response_model(action)
        if inspect.isclass(return_type) and issubclass(return_type, AgentState):
            return_type = return_type.model_fields['data'].annotation
        fields['data'] = (return_type, Field(..., description=fields['data'][1].description))

        return create_model(f'{action.capitalize()}ResponseModel', **fields)
