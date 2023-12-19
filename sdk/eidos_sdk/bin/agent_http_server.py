import argparse
import logging.config
import os
import pathlib
from contextlib import asynccontextmanager
from itertools import chain

import dotenv
import uvicorn
import yaml
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from eidos_sdk.agent_os import AgentOS
from eidos_sdk.system.agent_machine import AgentMachine, error_logger
from eidos_sdk.system.resources import builtin_resources
from eidos_sdk.system.resources_base import Resource
from eidos_sdk.util.logger import logger

dotenv.load_dotenv()


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

    # Parse command line arguments
    return parser.parse_args()


def load_resources(path):
    for file in os.listdir(path):
        file_loc = os.path.join(path, file)
        with error_logger(file_loc), open(file_loc) as resource_yaml:
            resource = Resource.model_validate(yaml.safe_load(resource_yaml))
        yield resource, file_loc


@asynccontextmanager
async def start_os(app, resource_generator, log_level=logging.INFO, machine_name="DEFAULT"):
    conf_ = pathlib.Path(__file__).parent.parent.parent / "logging.conf"
    logging.config.fileConfig(conf_)
    logger.setLevel(log_level)
    try:
        machine = AgentMachine.from_resources(chain(builtin_resources, resource_generator), machine_name)
        AgentOS.load_machine(machine)
        await machine.start(app)
        logger.info("Server Started")
        yield
    except Exception:
        logger.exception("Failed to start AgentOS")
        raise
    machine.stop()
    AgentOS.reset()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger("eidolon")
        logger.info(f"Request: {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception("Unhandled exception")
            raise e
        logger.info(f"Response: {response.status_code}")
        return response


def main():
    args = parse_args()
    log_level_str = "debug" if args.debug else "info"
    log_level = logging.DEBUG if args.debug else logging.INFO

    _app = FastAPI(
        lifespan=lambda app: start_os(app, load_resources(args.yaml_path), log_level, args.machine),
    )
    _app.add_middleware(LoggingMiddleware)

    # Run the server
    uvicorn.run(
        _app,
        host="0.0.0.0",
        port=args.port,
        log_level=log_level_str,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
