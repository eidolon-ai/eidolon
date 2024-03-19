import logging

import argparse

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from usage_server import endpoints
from usage_server.logger_ import logger

app = FastAPI(title="Usage Service")
app.include_router(endpoints.usage, tags=["Usage"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_args():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Start a FastAPI server.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8527,
        help="Port to run the FastAPI server on. Defaults to 8527.",
    )
    parser.add_argument("--debug", action="store_true", help="Turn on debug logging")
    parser.add_argument(
        "-r",
        "--reload",
        help="Reload the server when the code changes. Defaults to False.",
        action="store_true",
    )

    # Parse command line arguments
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_level_str = "debug" if args.debug else "info"
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=args.port,
        log_level=log_level_str,
        reload=args.reload,
    )
