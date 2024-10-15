import copy
import hashlib
import json
import logging
import os
import re
import socket
import time
from functools import cache
from importlib import metadata
from platform import python_version, uname
from typing import Optional, Any

from posthog import Posthog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import RequestContext
from eidolon_ai_sdk.util.routing import get_route_name


class PosthogConfig:
    enabled: Optional[bool] = None
    client: Posthog = Posthog("phc_9lcmDyxVkji98ggIqy2XvyVcItnrgdrMQhZBFp6Du5d", host="https://us.i.posthog.com")


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
def machine_id() -> str:
    if not posthog_enabled():
        return "disabled"
    return os.environ.get("POSTHOG_ID") or hashlib.md5(socket.gethostname().encode()).hexdigest()


def properties():
    return copy.deepcopy(_properties())


@cache
def _properties():
    system, _, release, version, machine, processor = uname()  # node contains identifying information, ignore
    rtn = {
        "python version": python_version(),
        "platform.system": system,
        "platform.release": release,
        "platform.version": version,
        "platform.machine": machine,
        "platform.processor": processor,
        "machine_id": machine_id(),
    }
    metrics_loc = os.path.join(os.path.dirname(os.path.dirname((os.path.dirname(__file__)))), "metrics.json")

    try:
        with open("metrics.json", "r") as file:
            metrics = json.load(file)
        rtn.update(metrics)
    except FileNotFoundError:
        logger.warning(f"Failed to load metrics from {metrics_loc}", exc_info=logger.isEnabledFor(logging.DEBUG))
        pass
    try:
        rtn["eidolon version"] = metadata.version("eidolon-ai-sdk")
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

    return with_logging


# below is a decorator that wraps a function with a try catch and logs with the fn name if exception is thrown
@metric
def report_server_started(time_to_start: float, number_of_agents: int, error: bool):
    kwargs = dict(
        distinct_id=machine_id(),
        event="server_started",
        properties={
            "time_to_start": time_to_start,
            "number_of_agents": number_of_agents,
            "error": error,
            **properties(),
        },
    )
    PosthogConfig.client.capture(**kwargs)
    logger.debug("Server started reported with %s", kwargs)


@cache
def _builtin_agents():
    from eidolon_ai_sdk.builtins.code_builtins import named_builtins
    return {r.metadata.name for r in named_builtins()}


@metric
def report_agent_state_change(process_id, state, error: Optional[Any] = None):
    l_distinct_id = RequestContext.get("X-Posthog-Distinct-Id", machine_id())
    props = properties()
    props["process_id"] = process_id
    props['agent_type'] = _get_agent_type()
    props["state"] = state
    if error:
        props["error"] = error
    PosthogConfig.client.capture(l_distinct_id, event="process_state_transition", properties=props)
    logger.info("Agent request reported")


def _get_agent_type():
    agent_type = RequestContext.get('agent_type', default="unknown")
    if agent_type not in _builtin_agents():
        agent_type = "custom"
    return agent_type


AGENT_PATTERN = re.compile(r'(/agents?/)([^/]+)')
ACTIONS_PATTERN = re.compile(r'(/actions/)([^/]+)')


class PostHogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        t0 = time.perf_counter()
        l_distinct_id = RequestContext.get("X-Posthog-Distinct-Id", machine_id())
        props = properties()
        props['response_type'] = request.headers.get("accept", "unknown")
        pre_sub = get_route_name(request)
        if pre_sub:
            post_sub = AGENT_PATTERN.sub(r"\1{agent_name}", pre_sub)  # replaces
            post_sub = ACTIONS_PATTERN.sub(r"\1{action_name}", post_sub)
            props['route'] = post_sub
        props['method'] = request.method
        try:
            response = await call_next(request)
            props['response_code'] = response.status_code
        except Exception as e:
            props['response_code'] = 500
            props['error'] = str(e)
            raise e
        finally:
            props['duration'] = time.perf_counter() - t0
            metric(PosthogConfig.client.capture)(
                l_distinct_id, event="http_request", properties=props
            )

        return response
