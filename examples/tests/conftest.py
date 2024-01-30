import os
import pathlib
import subprocess
import time
from contextlib import contextmanager

import pytest


def tail(file_path, sleep_sec=0.1):
    with open(file_path, "r") as file:
        # Move to the end of the file
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(sleep_sec)  # Wait briefly if no new line is found.
                continue
            yield line


@pytest.fixture(scope="session")
def log_dir():
    log_dir = os.getenv("EIDOLON_TEST_LOG_DIR", "/tmp/eidolon_test_logs")
    os.makedirs(log_dir, exist_ok=True)
    os.system(f"rm -rf {log_dir}/*")
    return log_dir


@pytest.fixture(scope="session")
def eidolon_server(eidolon_examples, log_dir):
    @contextmanager
    def fn(resources_loc, *args, log_file=None):
        # Command to start the HTTP server
        cmd = ["eidos-server", str(resources_loc), *args]
        cwd = eidolon_examples.parent
        log_file = os.path.join(log_dir, log_file or "logs.txt")

        # Using "a" to append to the log file since multiple tests may use the same file.
        with open(log_file, "a") as file:
            print(f"Logging to {log_file}")
            file.writelines(["-" * 20 + "\n", f"Running subprocess with command: {' '.join(cmd)}\n", "-" * 20 + "\n"])
            file.flush()  # Otherwise the lines will end up after the server logs
            server = subprocess.Popen(args=cmd, cwd=cwd, stdout=file, stderr=subprocess.STDOUT)

            # Wait until "Server Started" is printed
            t0 = time.time()
            for line in tail(log_file):
                print(line)
                if "Server Started" in line:
                    break
                elif "Failed to start AgentOS" in line:
                    raise RuntimeError("Failed to start AgentOS")
                if time.time() - t0 > 30:
                    raise RuntimeError("Server took too long to start, aborting.")

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
