import argparse
import logging.config
import pathlib
from collections import deque
from contextlib import asynccontextmanager
from importlib.metadata import version, PackageNotFoundError

import dotenv
import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import TypeAdapter
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import ContextMiddleware
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.builtins.components.opentelemetry import OpenTelemetryManager
from eidolon_ai_sdk.security.permissions import PermissionException, permission_exception_handler
from eidolon_ai_sdk.security.security_middleware import SecurityMiddleware
from eidolon_ai_sdk.system.agent_machine import AgentMachine
from eidolon_ai_sdk.system.dynamic_middleware import DynamicMiddleware
from eidolon_ai_sdk.system.resources.machine_resource import MachineResource
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import load_resources, Resource
from eidolon_ai_sdk.util.replay import ReplayConfig

dotenv.load_dotenv()

try:
    from opentelemetry.instrumentation.logging import LoggingInstrumentor

    LoggingInstrumentor().instrument()
except ImportError:
    pass

try:
    EIDOLON_SDK_VERSION = version("eidolon-ai-sdk")
except PackageNotFoundError:
    EIDOLON_SDK_VERSION = "unknown"


def parse_args():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Start a FastAPI server.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="Port to run the FastAPI server on. Defaults to 8080.",
    )
    parser.add_argument(
        "-r",
        "--reload",
        help="Reload the server when the code changes. Defaults to False.",
        action="store_true",
    )
    parser.add_argument("--debug", action="store_true", help="Turn on debug logging")
    parser.add_argument(
        "yaml_path",
        type=str,
        help="Path to a directory containing YAML files describing the agent machine to start.",
    )
    parser.add_argument(
        "-m",
        "--machine",
        type=str,
        help="The name of the machine to start.",
        default="DEFAULT",
    )
    parser.add_argument(
        "--record",
        help="Enable replay points and save them to the provide directory",
        action="store_true",
        default=False,
    )

    # Parse command line arguments
    return parser.parse_args()


@asynccontextmanager
async def start_os(app: FastAPI, resource_generator, machine_name, log_level=logging.INFO, replay_override=...):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Custom API",
            version=EIDOLON_SDK_VERSION,
            routes=app.routes,
        )

        # EventTypes
        queue = deque(
            [("EventTypes", TypeAdapter(StreamEvent).json_schema(ref_template="#/components/schemas/{model}"))]
        )
        depth = 0
        while queue:
            if depth > 100:
                raise ValueError("Too many $defs")
            name, schema = queue.popleft()
            if "$defs" in schema:
                for d_name, d in schema["$defs"].items():
                    queue.append((d_name, d))
                del schema["$defs"]
            openapi_schema["components"]["schemas"][name] = schema
            depth += 1

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    conf_ = pathlib.Path(__file__).parent.parent.parent / "logging.conf"
    logging.config.fileConfig(conf_)
    logger.setLevel(log_level)

    # add system level endpoints
    @app.get(path="/system/health", tags=["system"], description="Health check")
    async def health():
        return {"status": "ok"}

    # noinspection PyShadowingNames
    @app.get("/system/version", tags=["system"], description="Get the version of the EIDOS SDK")
    async def version():
        return {"version": EIDOLON_SDK_VERSION}

    try:
        for resource_or_tuple in resource_generator:
            if isinstance(resource_or_tuple, Resource):
                resource, source = resource_or_tuple, None
            else:
                resource, source = resource_or_tuple
            AgentOS.register_resource(resource=resource, source=source)

        logger.info(f"Building machine '{machine_name}'")
        machine_spec = AgentOS.get_resource(MachineResource, machine_name).spec
        logger.debug(yaml.safe_dump(machine_spec.model_dump()))
        machine: AgentMachine = machine_spec.instantiate()
        AgentOS.load_machine(machine)
        await machine.start(app)

        if replay_override is not ...:
            spec = AgentOS.get_resource_raw(ReferenceResource, "ReplayConfig").spec
            spec["save_loc"] = replay_override
        if AgentOS.get_instance(ReplayConfig).save_loc:
            logger.warning("Replay points are enabled, this feature is intended for test environments only.")

        open_tele = AgentOS.get_instance(OpenTelemetryManager)
        await open_tele.start()
        try:
            logger.info("Server Started")
            yield
        finally:
            await open_tele.stop()

        await machine.stop()
    except BaseException:
        logger.exception("Failed to start AgentOS")
        raise
    finally:
        AgentOS.reset()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception("Unhandled exception")
            raise e
        if response.status_code >= 500:
            logger.error(f"Response: {response.status_code}")
        else:
            logger.info(f"Response: {response.status_code}")
        return response


def main():
    args = parse_args()
    log_level_str = "debug" if args.debug else "info"
    log_level = logging.DEBUG if args.debug else logging.INFO

    _app = start_app(
        lambda app: start_os(
            app,
            load_resources(args.yaml_path),
            args.machine,
            log_level,
            replay_override="recordings" if args.record else ...,
        )
    )

    # Run the server
    uvicorn.run(
        _app,
        host="0.0.0.0",
        port=args.port,
        log_level=log_level_str,
        reload=args.reload,
    )


# noinspection PyTypeChecker
def start_app(lifespan):
    try:
        _app = FastAPI(lifespan=lifespan)
        _app.add_middleware(DynamicMiddleware)
        _app.add_middleware(ContextMiddleware)
        _app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        _app.add_middleware(SecurityMiddleware)
        _app.add_middleware(LoggingMiddleware)
        _app.add_exception_handler(PermissionException, permission_exception_handler)
        FastAPIInstrumentor.instrument_app(_app)
        return _app
    except Exception as e:
        logger.exception("Failed to start FastAPI", e)
        raise


if __name__ == "__main__":
    main()
