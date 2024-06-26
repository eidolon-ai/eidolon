import argparse
import asyncio
import logging.config
import pathlib
from collections import deque
from contextlib import asynccontextmanager
from importlib.metadata import version, PackageNotFoundError

import dotenv
import time
import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import TypeAdapter
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import ContextMiddleware
from eidolon_ai_sdk.builtins.components.opentelemetry import OpenTelemetryManager
from eidolon_ai_sdk.security.permissions import PermissionException, permission_exception_handler
from eidolon_ai_sdk.security.security_middleware import SecurityMiddleware
from eidolon_ai_sdk.system import resource_load_error_handler
from eidolon_ai_sdk.system.agent_machine import AgentMachine
from eidolon_ai_sdk.system.dynamic_middleware import DynamicMiddleware
from eidolon_ai_sdk.system.kernel import AgentOSKernel
from eidolon_ai_sdk.system.resources.machine_resource import MachineResource
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import load_resources, Resource
from eidolon_ai_sdk.util.posthog import report_server_started, PosthogConfig
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
        nargs='+',
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
    parser.add_argument(
        "--disable-metrics",
        help="Disable anonymous metrics collection",
        default=False,
    )
    parser.add_argument(
        "--fail-on-bad-agent",
        help="Fail the server if an agent fails to start",
        default=False,
    )
    parser.add_argument(
        "--dotenv",
        action="append",
        help="specify a .env file to load environment variables from.",
    )
    return parser.parse_args()


@asynccontextmanager
async def start_os(app: FastAPI, resource_generator, machine_name, log_level=logging.INFO, replay_override=..., fail_on_agent_start_error=False):
    t0 = time.perf_counter()

    resource_load_error_handler.fail_on_agent_start_error = fail_on_agent_start_error

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
            try:
                AgentOSKernel.register_resource(resource=resource, source=source)
            except Exception as e:
                raise ValueError(f"Failed to load resource {resource.metadata.name} from {source}") from e

        logger.info(f"Building machine '{machine_name}'")
        machine_spec = AgentOSKernel.get_resource(MachineResource, machine_name).spec
        logger.debug(yaml.safe_dump(machine_spec.model_dump()))
        machine: AgentMachine = machine_spec.instantiate()
        AgentOSKernel.load_machine(machine)
        await machine.start(app)

        if replay_override is not ...:
            spec = AgentOSKernel.get_resource_raw(ReferenceResource, "ReplayConfig").spec
            spec["save_loc"] = replay_override
        if AgentOSKernel.get_instance(ReplayConfig).save_loc:
            logger.warning("Replay points are enabled, this feature is intended for test environments only.")

        open_tele = AgentOSKernel.get_instance(OpenTelemetryManager)
        await open_tele.start()
        try:
            time_to_start = time.perf_counter() - t0
            report_server_started(time_to_start, len(machine.agent_controllers), False)
            logger.info(f"Server Started in {time_to_start:.2f}s")
            yield
        finally:
            await open_tele.stop()

        await machine.stop()
    except BaseException:
        time_to_start = time.perf_counter() - t0
        await report_server_started(time_to_start, -1, True)
        logger.exception("Failed to start AgentOS")
        raise
    finally:
        AgentOSKernel.reset()


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
    disable_metrics = args.disable_metrics
    if disable_metrics:
        PosthogConfig.enabled = False
    log_level_str = "debug" if args.debug else "info"
    log_level = logging.DEBUG if args.debug else logging.INFO
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    for dotenv_file in args.dotenv or []:
        dotenv.load_dotenv(dotenv_file)

    _app = start_app(
        lambda app: start_os(
            app,
            load_resources(args.yaml_path),
            args.machine,
            log_level,
            replay_override="recordings" if args.record else ...,
            fail_on_agent_start_error=args.fail_on_bad_agent,
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


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{await request.body()}: {exc_str}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


# noinspection PyTypeChecker
def start_app(lifespan):
    try:
        _app = FastAPI(lifespan=lifespan)
        _app.add_exception_handler(RequestValidationError, validation_exception_handler)
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
