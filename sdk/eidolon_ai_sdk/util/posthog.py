import asyncio
import hashlib
import json
import logging
import os
import socket
from functools import wraps, cache
from importlib import metadata
from platform import python_version, uname
from typing import Optional

from posthog import Posthog

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.util.async_wrapper import make_async


class PosthogConfig:
    enabled: Optional[bool] = None
    client: Posthog = Posthog('phc_9lcmDyxVkji98ggIqy2XvyVcItnrgdrMQhZBFp6Du5d', host="https://us.i.posthog.com")


@cache
def posthog_enabled():
    if PosthogConfig.enabled is not None:
        enabled = PosthogConfig.enabled
    else:
        enabled = os.environ.get("DISABLE_ANONYMOUS_METRICS", "false").lower() == "false"
    if enabled:
        logger.info("Collecting anonymous metrics, to disable metrics set DISABLE_ANONYMOUS_METRICS")
    else:
        PosthogConfig.client.disabled = True
    return enabled


@cache
def distinct_id() -> str:
    if not posthog_enabled():
        return "disabled"
    return os.environ.get('POSTHOG_ID') or hashlib.md5(socket.gethostname().encode()).hexdigest()


@cache
def properties():
    system, _, release, version, machine, processor = uname()  # node contains identifying information, ignore
    rtn = {
        "python version": python_version(),
        "platform.system": system,
        "platform.release": release,
        "platform.version": version,
        "platform.machine": machine,
        "platform.processor": processor,
    }
    metrics_loc = os.path.join(os.path.dirname(os.path.dirname((os.path.dirname(__file__)))), 'metrics.json')

    try:
        with open("metrics.json", 'r') as file:
            metrics = json.load(file)
        rtn.update(metrics)
    except FileNotFoundError:
        logger.warning(f"Failed to load metrics from {metrics_loc}", exc_info=logger.isEnabledFor(logging.DEBUG))
        pass
    try:
        rtn['eidolon version'] = metadata.version("eidolon-ai-sdk")
    except metadata.PackageNotFoundError:
        logger.warning("Failed to load eidolon version", exc_info=logger.isEnabledFor(logging.DEBUG))
        pass

    return {k: v for k, v in rtn.items() if v != "" and v is not None}


def metric(fn):
    def with_logging(*args, **kwargs):
        try:
            if posthog_enabled():
                fn(*args, **kwargs)
            else:
                logger.debug(f"Metrics disabled, not reporting {fn.__name__}")
        except Exception:
            logger.warning(f"Error reporting metrics {fn.__name__}", exc_info=logger.isEnabledFor(logging.DEBUG))

    @wraps(fn)
    def second_wrapper(*args, **kwargs):
        return asyncio.create_task(make_async(with_logging)(*args, **kwargs))

    return second_wrapper


# below is a decorator that wraps a function with a try catch and logs with the fn name if exception is thrown
@metric
def report_server_started(time_to_start: float, number_of_agents: int, error: bool):
    kwargs = dict(distinct_id=distinct_id(), event='server_started', properties={
        'time_to_start': time_to_start,
        'number_of_agents': number_of_agents,
        'error': error,
        **properties()
    })
    PosthogConfig.client.capture(**kwargs)
    logger.debug("Server started reported with %s", kwargs)


@metric
def report_new_process():
    PosthogConfig.client.capture(distinct_id(), event='new_process', properties=properties())


@cache
def _builtin_agents():
    from eidolon_ai_sdk.builtins.code_builtins import named_builtins
    return {r.metadata.name for r in named_builtins()}


@metric
def report_agent_action(agent_name: str):
    if agent_name not in _builtin_agents():
        agent_name = "custom"
    PosthogConfig.client.capture(distinct_id(), event='agent_action', properties={
        'agent_type': agent_name,
        **properties()
    })
    logger.info("Agent request reported")
