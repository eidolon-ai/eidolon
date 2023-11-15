from typing import Type, Callable

from fastapi import Body, FastAPI, Request, BackgroundTasks
from pydantic import BaseModel


def create_endpoint_with_process_id(model: Type[BaseModel], fn: Callable):
    async def dynamic_endpoint(
            background_tasks: BackgroundTasks,
            request: Request,
            item: model = Body(...),
            process_id: str = None,
    ):
        # Process the input item
        return await fn(
            request=request,
            body=item,
            process_id=process_id,
            background_tasks=background_tasks,
        )
    return dynamic_endpoint


def create_endpoint_without_process_id(model: Type[BaseModel], fn: Callable):
    async def dynamic_endpoint(
            background_tasks: BackgroundTasks,
            request: Request,
            item: model = Body(...),
    ):
        # Process the input item
        return await fn(
            request=request,
            body=item,
            process_id=None,
            background_tasks=background_tasks,
        )
    return dynamic_endpoint


def add_dynamic_route(add_proccess_param, app: FastAPI, path: str, input_model: Type[BaseModel], fn: Callable, **kwargs):
    endpoint = create_endpoint_with_process_id(input_model, fn)
    app.add_api_route(path, endpoint=endpoint, methods=["POST"], **kwargs)
