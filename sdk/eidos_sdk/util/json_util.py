from pydantic import BaseModel
from typing import Any


def model_to_json(model: Any) -> Any:
    if isinstance(model, BaseModel):
        return model.model_dump()
    elif isinstance(model, dict):
        return model
    elif isinstance(model, list):
        return [model_to_json(m) for m in model]
    else:
        return model
