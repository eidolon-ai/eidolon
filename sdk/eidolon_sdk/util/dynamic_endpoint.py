from typing import Type, Callable

from fastapi import Body, FastAPI
from pydantic import BaseModel


def create_endpoint(model: Type[BaseModel], fn: Callable):
    async def dynamic_endpoint(item: model = Body(...)):
        # Process the input item
        return await fn(item)
    return dynamic_endpoint


def add_dynamic_route(app: FastAPI, path: str, input_model: Type[BaseModel], response_model: Type[BaseModel], fn: Callable, **kwargs):
    app.add_api_route(path, endpoint=create_endpoint(input_model, fn), methods=["POST"], response_model=response_model, **kwargs)
