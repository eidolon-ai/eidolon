from __future__ import annotations

import importlib
import inspect
import typing
from datetime import datetime
from typing import Optional

from bson import ObjectId
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo
from starlette.responses import JSONResponse

from agent_memory import SymbolicMemory
from eidolon_sdk.util.dynamic_endpoint import add_dynamic_route
from .agent import Agent, AgentState
from .agent_os import AgentOS
from .agent_program import AgentProgram


class ProcessResponse(BaseModel):
    process_id: str = Field(..., description="The ID of the conversation.")


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

        self.agent = impl_class(self, agent_memory=self.agent_os.machine.agent_memory)

        add_dynamic_route(
            app=app,
            path=f"/programs/{self.agent_program.name}",
            input_model=self.create_input_model('INIT'),
            response_model=ProcessResponse,
            fn=self.processRoute('INIT'),
            status_code=202,
        )

        for action, handler in filter(lambda tu: tu[0] != "INIT", self.agent.action_handlers.items()):
            # the endpoint to hit to process/continue the current state
            add_dynamic_route(
                app=app,
                path=f"/programs/{self.agent_program.name}/processes/{{process_id}}/actions/{action}",
                input_model=self.create_input_model(action),
                response_model=ProcessResponse,
                fn=self.processRoute(action),
                status_code=202,
            )

        app.add_api_route(
            f"/programs/{self.agent_program.name}/processes/{{process_id}}/status",
            endpoint=self.getProcessInfo,
            methods=["GET"],
            # response_model=dict,
        )

    def create_input_model(self, action):
        sig = inspect.signature(self.agent.action_handlers[action].fn).parameters
        hints = typing.get_type_hints(self.agent.action_handlers[action].fn, include_extras=True)
        fields = {}
        for param, hint in filter(lambda tu: tu[0] != 'return', hints.items()):
            if hasattr(hint, '__metadata__') and isinstance(hint.__metadata__[0], FieldInfo):
                field: FieldInfo = hint.__metadata__[0]
                field.default = sig[param].default
                fields[param] = (hint.__origin__, field)
            else:
                # _empty default isn't being handled by create_model properly (still optional when it should be required)
                default = ... if getattr(sig[param].default, "__name__", None) == '_empty' else sig[param].default
                fields[param] = (hint, default)

        input_model = create_model(f'{action.capitalize()}InputModel', **fields)
        return input_model

    def stop(self, app: FastAPI):
        pass

    def restart(self, app: FastAPI):
        self.stop(app)
        self.start(app)

    def processRoute(self, action: str):
        async def processStateRoute(request: Request, body: BaseModel, process_id: typing.Optional[str], background_tasks: BackgroundTasks):
            print(action)
            print(body)
            memory: SymbolicMemory = self.agent_os.machine.agent_memory.symbolic_memory
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

            state = dict(process_id=process_id, state="processing", data=dict(action=action, body=body.model_dump()), date=str(datetime.now().isoformat()))
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
                    await memory.insert_one(
                        'processes',
                        dict(
                            process_id=process_id,
                            state=state,
                            data=data,
                            date=str(datetime.now().isoformat()))
                    )
                except HTTPException as e:
                    await memory.insert_one(
                        'processes',
                        dict(
                            process_id=process_id,
                            state="http_error",
                            data=dict(detail=e.detail, status_code=e.status_code),
                            date=str(datetime.now().isoformat()))
                    )
                    print(e)  # todo, log this
                except Exception as e:
                    await memory.insert_one(
                        'processes',
                        dict(
                            process_id=process_id,
                            state="unhandled_error",
                            data=dict(error=str(e)),
                            date=str(datetime.now().isoformat()))
                    )
                    print(e)  # todo, log this

            pid = process_id or self.agent_os.startProcess(request.headers.get('callback_url'))
            background_tasks.add_task(run_and_store_response)
            return {"process_id": pid}

        return processStateRoute

    async def getProcessInfo(self, process_id: str):
        latest_record = await self.get_latest_process_event(process_id)
        if not latest_record:
            raise HTTPException(status_code=404, detail="Process not found")
        elif latest_record['state'] == 'unhandled_error':
            return JSONResponse(latest_record['data'], 500)
        elif latest_record['state'] == 'http_error':
            return JSONResponse(dict(detail=latest_record['data']['detail']), latest_record['data']['status_code'])
        else:
            try:
                del latest_record['_id']
            except KeyError:
                pass
            return JSONResponse(dict(
                process_id=latest_record['process_id'],
                state=latest_record['state'],
                data=latest_record['data'],
            ), 200)

    async def get_latest_process_event(self, process_id):
        # todo, memory needs to include sorting
        latest_record = None
        memory: SymbolicMemory = self.agent_os.machine.agent_memory.symbolic_memory
        records = memory.find('processes', dict(process_id=process_id))
        async for record in records:
            if not latest_record or record['date'] > latest_record['date']:
                latest_record = record
        return latest_record

    def create_response_model(self, state: str):
        fields = {
            "conversation_id": (str, Field(..., description="The ID of the conversation.")),
        }
        for t_name, t_model in self.agent_program.states[state].transitions_to_models.items():
            fields[t_name] = (Optional[t_model], Field(default=None, description="The answer for {t_name} transition state."))

        return create_model(f'{state.capitalize()}ResponseModel', **fields)
