import pathlib
import subprocess
from contextlib import contextmanager

import pytest


@pytest.fixture(scope="session")
def eidolon_server(eidolon_examples):
    @contextmanager
    def fn(resources_loc, *args):
        http_server_loc = eidolon_examples.parent.parent / "sdk" / "eidos_sdk" / "bin" / "agent_http_server.py"

        # Command to start the HTTP server
        cmd = ["python", str(http_server_loc), str(resources_loc), *args]

        # Start the server as a separate process
        server = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Wait until "Server Started" is printed
        for line in server.stdout:
            print(line.decode().strip())  # print the server's output
            if "Server Started" in line.decode():
                break

        yield server
        # After tests are done, terminate the server process
        server.terminate()

    return fn


@pytest.fixture(scope="session")
def eidolon_examples():
    return pathlib.Path(__file__).parent.parent / "eidolon_examples"


@pytest.fixture
def server_loc():
    return "http://localhost:8080"
