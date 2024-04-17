from __future__ import annotations

import inspect
import io
import os
from functools import wraps
from glob import glob
from typing import Optional

import dill
from pydantic import BaseModel
from srsly.ruamel_yaml import YAML
from srsly.ruamel_yaml.scalarstring import walk_tree

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.util.str_utils import log_stack_trace


class ReplayConfig(BaseModel):
    save_loc: Optional[str] = None  # If None, resume points are disabled
    digit_length: int = 3


def default_serializer(*args, **kwargs):
    # this is not serializing multi-line strings well, we should consider swapping yaml parsers or customizing this
    f = io.BytesIO()
    with YAML(output=f) as yaml:
        to_dump = dict(args=list(args), kwargs=kwargs)
        walk_tree(to_dump)  # replaces multi line strings with LiteralScalarString
        yaml.dump(to_dump, stream=f)
    f.flush()
    return f.getvalue().decode(), "yaml"


def default_deserializer(str_):
    with YAML() as yaml:
        obj = yaml.load(str_)
    return obj["args"], obj["kwargs"]


async def default_parser(resp):
    yield await resp


def replayable(
    fn, serializer=default_serializer, deserializer=default_deserializer, parser=default_parser, name_override=None
):
    config = AgentOS.get_instance(ReplayConfig)

    async def maybe_save_args(*args, **kwargs):
        if config.save_loc:
            try:
                existing_dirs = [os.path.split(d)[-1] for d in await AgentOS.file_memory.glob(config.save_loc + "/*")]
                dir_number = [int(d.split("_")[0]) for d in existing_dirs]
                top = max(0, *dir_number) if dir_number else -1
                next_ = str(top + 1)
                next_ = "0" * (config.digit_length - len(next_)) + next_
                loc = f"{config.save_loc}/{next_}_{name_override or fn.__name__}"
                await AgentOS.file_memory.mkdir(loc)

                printable_save_loc = loc
                if hasattr(AgentOS.file_memory, "resolve"):
                    printable_save_loc = AgentOS.file_memory.resolve(printable_save_loc)
                logger.info(f"Saving replay point to {printable_save_loc}")

                data, file_type = serializer(*args, **kwargs)
                await AgentOS.file_memory.write_file(loc + "/fn.dill", dill.dumps(fn))
                await AgentOS.file_memory.write_file(loc + f"/data.{file_type}", data.encode())
                await AgentOS.file_memory.write_file(loc + "/deserializer.dill", dill.dumps(deserializer))
                await AgentOS.file_memory.write_file(loc + "/parser.dill", dill.dumps(parser))
            except Exception as e:
                log_stack_trace()
                logger.exception(e)

    @wraps(fn)
    async def wrapper_async_gen(*args, **kwargs):
        await maybe_save_args(*args, **kwargs)
        async for e in fn(*args, **kwargs):
            yield e

    @wraps(fn)
    async def wrapper_async(*args, **kwargs):
        await maybe_save_args(*args, **kwargs)
        return await fn(*args, **kwargs)

    if inspect.isasyncgenfunction(fn):
        return wrapper_async_gen
    else:
        return wrapper_async


async def replay(loc):
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
    async for e in parser(fn(*args, **kwargs)):
        yield e
