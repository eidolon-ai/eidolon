import logging.config
import pathlib
import typing
from collections import deque
from contextlib import asynccontextmanager
from importlib.metadata import version, PackageNotFoundError
from typing import Literal

import dotenv
import time
from dotenv import find_dotenv
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import TypeAdapter, BaseModel, Field
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from eidolon_ai_client.events import StreamEvent
from eidolon_ai_client.util.logger import logger
from eidolon_ai_client.util.request_context import ContextMiddleware
from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.builtins.components.opentelemetry import OpenTelemetryManager
from eidolon_ai_sdk.security.permissions import PermissionException, permission_exception_handler
from eidolon_ai_sdk.security.security_middleware import SecurityMiddleware
from eidolon_ai_sdk.system import resource_load_error_handler
from eidolon_ai_sdk.system.agent_machine import AgentMachine
from eidolon_ai_sdk.system.dynamic_middleware import DynamicMiddleware
from eidolon_ai_sdk.system.kernel import AgentOSKernel
from eidolon_ai_sdk.system.resources.agent_resource import AgentResource
from eidolon_ai_sdk.system.resources.machine_resource import MachineResource
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.resources.resources_base import Resource
from eidolon_ai_sdk.util.posthog import report_server_started, PostHogMiddleware
from eidolon_ai_sdk.util.replay import ReplayConfig

dotenv.load_dotenv(find_dotenv(usecwd=True))

try:
    from opentelemetry.instrumentation.logging import LoggingInstrumentor

    LoggingInstrumentor().instrument()
except ImportError:
    pass

try:
    EIDOLON_SDK_VERSION = version("eidolon-ai-sdk")
except PackageNotFoundError:
    EIDOLON_SDK_VERSION = "unknown"


class ResourceStatus(BaseModel):
    resource_name: str = Field(description="The name of the resource.")
    resource_status: Literal["initialized", "starting", "running", "stopped", "error"] = Field(
        description="The status of the resource."
    )
    errors: typing.List[str] = Field(default=[], description="Any errors that occurred while starting the resource.")


class MachineStatus(BaseModel):
    machine_status: str = Field(description="The status of the machine.")
    machine_name: str = Field(description="The name of the machine.")
    machine_version: str = Field(description="The version of the machine.")
    resources: typing.Dict[str, ResourceStatus] = Field(description="Resources available on this machine.")
    agents: typing.Dict[str, ResourceStatus] = Field(description="Agents running on this machine.")


@asynccontextmanager
async def start_os(
    app: FastAPI,
    resource_generator,
    machine_name,
    log_level=logging.INFO,
    replay_override=...,
    fail_on_agent_start_error=False,
):
    t0 = time.perf_counter()

    resource_load_error_handler.fail_on_agent_start_error = fail_on_agent_start_error

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Agent Machine",
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

    _status = "starting"

    # add system level endpoints
    @app.get(path="/system/health", tags=["system"], description="Health check")
    async def health():
        resource_status = {}
        agent_status = {}
        for res in AgentOSKernel.get_resources(ReferenceResource):
            errors = resource_load_error_handler.load_errors.get(res, []) + resource_load_error_handler.start_errors.get(
                res, []
            )
            resource_status[res] = ResourceStatus(
                resource_name=res, resource_status="error" if errors else "running", errors=errors
            )
        for res in AgentOSKernel.get_resources(AgentResource):
            errors = resource_load_error_handler.load_errors.get(res, []) + resource_load_error_handler.start_errors.get(
                res, []
            )
            agent_status[res] = ResourceStatus(
                resource_name=res, resource_status="error" if errors else "running", errors=errors
            )
        return MachineStatus(
            machine_status=_status,
            machine_name=machine_name,
            machine_version=EIDOLON_SDK_VERSION,
            resources=resource_status,
            agents=agent_status,
        )

    # noinspection PyShadowingNames
    @app.get("/system/version", tags=["system"], description="Get the version of the EIDOS SDK")
    async def version():
        return {"version": EIDOLON_SDK_VERSION}

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse("/docs")

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
        AgentOS.machine_name = machine_name
        machine_spec = AgentOSKernel.get_resource(MachineResource, machine_name).spec
        logger.debug(machine_spec.model_dump())
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
            report_server_started(time.perf_counter() - t0, len(machine.agent_controllers), False)
            logger.info(f"Server Started in {time.perf_counter() - t0 :.2f}s")
            _status = "running"
            yield
        finally:
            await open_tele.stop()

        await machine.stop()
    except BaseException:
        logger.exception("Failed to start AgentOS")
        report_server_started(time.perf_counter() - t0, -1, True)
        raise
    finally:
        _status = "stopped"
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
        _app = FastAPI(lifespan=lifespan, title="Agent Machine")
        _app.add_exception_handler(RequestValidationError, validation_exception_handler)
        _app.add_middleware(DynamicMiddleware)
        _app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        _app.add_middleware(SecurityMiddleware)
        _app.add_middleware(PostHogMiddleware)
        _app.add_middleware(ContextMiddleware)
        _app.add_middleware(LoggingMiddleware)
        _app.add_exception_handler(PermissionException, permission_exception_handler)
        FastAPIInstrumentor.instrument_app(_app)
        return _app
    except Exception as e:
        logger.exception("Failed to start FastAPI", exc_info=e)
        raise
