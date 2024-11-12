import argparse
import asyncio
import logging
import os.path

import dotenv
import uvicorn
from dotenv import find_dotenv, load_dotenv

from eidolon_ai_sdk.bin.server import start_os, start_app
from eidolon_ai_sdk.system.resources.resources_base import load_resources
from eidolon_ai_sdk.util.posthog import PosthogConfig


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
        nargs="+",
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
    parser.add_argument(
        "--dotenv-override",
        action='store_true',
        help="Override existing environment variables with those in the .env file.",
    )
    return parser.parse_args()


args = parse_args()
disable_metrics = args.disable_metrics
if disable_metrics:
    PosthogConfig.enabled = False
log_level_str = "debug" if args.debug else "info"
log_level = logging.DEBUG if args.debug else logging.INFO
loop = asyncio.get_event_loop()
loop.set_debug(True)
load_dotenv(find_dotenv(usecwd=True), override=args.dotenv_override)
for dotenv_file in args.dotenv or []:
    dotenv.load_dotenv(dotenv_file, override=args.dotenv_override)

app = start_app(
    lambda app: start_os(
        app,
        load_resources(args.yaml_path),
        args.machine,
        log_level,
        replay_override="recordings" if args.record else ...,
        fail_on_agent_start_error=args.fail_on_bad_agent,
    )
)


def main():
    # Run the server
    kwargs = {}
    if args.reload:
        kwargs["reload"] = True
        kwargs["reload_dirs"] = [os.getcwd()]
        kwargs["reload_includes"] = ["*.yml", "*.yaml", "*.py", ".env"]

        potential_watch_locs = args.yaml_path
        potential_watch_locs.extend(args.dotenv or [])
        local_env = find_dotenv(usecwd=True)
        if local_env:
            potential_watch_locs.append(local_env)

        for f in potential_watch_locs:
            if os.path.relpath(f).startswith(".."):
                kwargs["reload_dirs"].append(os.path.abspath(f) if os.path.isdir(f) else os.path.abspath(os.path.dirname(f)))

    uvicorn.run(
        "eidolon_ai_sdk.bin.agent_http_server:app", host="0.0.0.0", port=args.port, log_level=log_level_str, **kwargs
    )


if __name__ == "__main__":
    main()
