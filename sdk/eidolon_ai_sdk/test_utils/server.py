import os
import threading
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from sse_starlette.sse import AppStatus

from eidolon_ai_client.util.logger import logger
from eidolon_ai_sdk.bin.server import start_os, start_app
from eidolon_ai_sdk.system.resources.resources_base import load_resources


@contextmanager
def serve_thread(resources, machine_name="test_machine", port=5346):
    def resource_generator():
        for resource in resources:
            if isinstance(resource, (str, Path)):
                yield from load_resources([resource])
            else:
                yield resource

    @asynccontextmanager
    async def manage_lifecycle(_app: FastAPI):
        async with start_os(
                app=_app,
                resource_generator=resource_generator(),
                machine_name=machine_name,
                fail_on_agent_start_error=True,
        ):
            yield

    app = start_app(lifespan=manage_lifecycle)
    server_wrapper = []

    def run_server():
        AppStatus.should_exit = False
        AppStatus.should_exit_event = None

        try:
            config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info", loop="asyncio")
            server = uvicorn.Server(config)
            server_wrapper.append(server)
            server.run()
            server_wrapper.append("stopped")
        except BaseException as e:
            server_wrapper.append("aborted")
            logger.exception("Server failed to start")
            raise e

    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    try:
        # Wait for the server to start
        while len(server_wrapper) == 0 or not (
                server_wrapper[-1] in {"aborted", "stopped"} or server_wrapper[0].started
        ):
            pass
        if server_wrapper[-1] in {"aborted", "stopped"}:
            raise Exception("Server failed to start")

        print(f"Server started on port {port}")
        os.environ["EIDOLON_LOCAL_MACHINE"] = f"http://localhost:{port}"
        yield f"http://localhost:{port}"
    finally:
        maybe_server = server_wrapper[-1]
        if isinstance(maybe_server, uvicorn.Server):
            maybe_server.should_exit = True
        server_thread.join()
