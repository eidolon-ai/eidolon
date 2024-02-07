from __future__ import annotations

from functools import wraps
from typing import Optional

import dill
import yaml
from pydantic import BaseModel

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.util.logger import logger


class ReplayConfig(BaseModel):
    save_loc: Optional[str] = None  # If None, resume points are disabled
    digit_length: int = 3


def default_serializer(*args, **kwargs):
    args = list(args)
    return yaml.safe_dump(dict(args=args, kwargs=kwargs), sort_keys=False), "yaml"


def default_deserializer(str_):
    obj = yaml.safe_load(str_)
    return obj["args"], obj["kwargs"]


async def default_parser(resp):
    yield resp


def replayable(
    fn, serializer=default_serializer, deserializer=default_deserializer, parser=default_parser, name_override=None
):
    config = AgentOS.get_instance(ReplayConfig)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if config.save_loc:
            try:
                existing_files = [int(d.split("_")[0]) for d in AgentOS.file_memory.glob(config.save_loc + "/*")]
                top = max(0, *existing_files) if existing_files else -1
                next_ = str(top + 1)
                next_ = "0" * (config.digit_length - len(next_)) + next_
                loc = f"{config.save_loc}/{next_}_{name_override or fn.__name__}"
                AgentOS.file_memory.mkdir(loc)
                data, file_type = serializer(*args, **kwargs)
                AgentOS.file_memory.write_file(loc + "/fn.dill", dill.dumps(fn))
                AgentOS.file_memory.write_file(loc + f"/data.{file_type}", data.encode())
                AgentOS.file_memory.write_file(loc + "/deserializer.dill", dill.dumps(deserializer))
                AgentOS.file_memory.write_file(loc + "/parser.dill", dill.dumps(parser))
            except Exception as e:
                logger.exception(f"Error saving resume point: {e}")
        return fn(*args, **kwargs)

    return wrapper


def replay(loc):
    data_file = AgentOS.file_memory.glob(loc + "/data.*")
    if not data_file:
        if hasattr(AgentOS.file_memory, "resolve"):
            loc = AgentOS.file_memory.resolve(loc)
        raise FileNotFoundError(f"No data file found in {loc}")
    data_loc = data_file[0]
    deserializer = dill.loads(AgentOS.file_memory.read_file(loc + "/deserializer.dill"))
    args, kwargs = deserializer(AgentOS.file_memory.read_file(data_loc))
    fn = dill.loads(AgentOS.file_memory.read_file(loc + "/fn.dill"))
    parser = dill.loads(AgentOS.file_memory.read_file(loc + "/parser.dill"))
    return parser(fn(*args, **kwargs))
