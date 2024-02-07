from __future__ import annotations

import os
from functools import wraps
from glob import glob
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
                existing_dirs = [os.path.split(d)[-1] for d in AgentOS.file_memory.glob(config.save_loc + "/*")]
                dir_number = [int(d.split("_")[0]) for d in existing_dirs]
                top = max(0, *dir_number) if dir_number else -1
                next_ = str(top + 1)
                next_ = "0" * (config.digit_length - len(next_)) + next_
                loc = f"{config.save_loc}/{next_}_{name_override or fn.__name__}"
                AgentOS.file_memory.mkdir(loc)

                printable_save_loc = loc
                if hasattr(AgentOS.file_memory, "resolve"):
                    printable_save_loc = AgentOS.file_memory.resolve(printable_save_loc)
                logger.info(f"Saving replay point to {printable_save_loc}")

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
    loc = str(loc)
    data_file = glob(loc + "/data.*")
    if not data_file:
        raise FileNotFoundError(f"No data file found in {loc}")

    with open(loc + "/deserializer.dill", "rb") as file:
        deserializer = dill.load(file)
    with open(loc + "/fn.dill", "rb") as file:
        fn = dill.load(file)
    with open(loc + "/parser.dill", "rb") as file:
        parser = dill.load(file)

    with open(data_file[0]) as file:
        args, kwargs = deserializer(file.read())
    return parser(fn(*args, **kwargs))
