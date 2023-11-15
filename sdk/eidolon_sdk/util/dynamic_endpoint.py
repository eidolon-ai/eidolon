from typing import Type, Callable

from fastapi import Body, Request, BackgroundTasks
from pydantic import BaseModel

"""
This file exists to create dynamic endpoints for the FastAPI server. We need this to properly hook up the body / 
parameter descriptions. The two methods correspond to the initialization and action endpoints since init does not take
a process id, but actions do. If we can do this explicitly without wrappers, that would be ideal since we will need to 
hand this off to the agent definers to support anything other than JSON bodies. 
"""

# todo, look into forge library to solve this problem: https://stackoverflow.com/questions/1409295/set-function-signature-in-python/50533832#50533832


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
