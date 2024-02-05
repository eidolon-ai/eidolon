from __future__ import annotations

from functools import wraps
from typing import Optional

import dill
import yaml
from pydantic import BaseModel

from eidos_sdk.agent_os import AgentOS


class ResumePointConfig(BaseModel):
    save_loc: Optional[str] = None  # If None, resume points are disabled
    digit_length: int = 3


def default_serializer(*args, **kwargs):
    return yaml.safe_dump(dict(args=args, kwargs=kwargs)), "yaml"


def default_deserializer(str_):
    obj = yaml.safe_load(str_)
    return obj["args"], obj["kwargs"]


def resume_point(fn, serializer=default_serializer, deserializer=default_deserializer):
    config = AgentOS.get_instance(ResumePointConfig)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if config.save_loc:
            existing_files = [int(d.split("_")[0]) for d in AgentOS.file_memory.glob(config.save_loc + "/*")]
            top = max(0, *existing_files) if existing_files else -1
            next_ = str(top + 1)
            next_ = "0" * (config.digit_length - len(next_)) + next_
            loc = f"{config.save_loc}/{next_}_{fn.__name__}"
            AgentOS.file_memory.mkdir(loc)
            data, file_type = serializer(*args, **kwargs)
            AgentOS.file_memory.write_file(loc + "/fn.dill", dill.dumps(fn))
            AgentOS.file_memory.write_file(loc + f"/data.{file_type}", data.encode())
            AgentOS.file_memory.write_file(loc + "/deserializer.dill", dill.dumps(deserializer))
        return fn(*args, **kwargs)

    return wrapper


def resume(loc):
    data_loc = AgentOS.file_memory.glob(loc + "/data.*")[0]
    deserializer = dill.loads(AgentOS.file_memory.read_file(loc + "/deserializer.dill"))
    args, kwargs = deserializer(AgentOS.file_memory.read_file(data_loc))
    fn = dill.loads(AgentOS.file_memory.read_file(loc + "/fn.dill"))
    return fn(*args, **kwargs)
