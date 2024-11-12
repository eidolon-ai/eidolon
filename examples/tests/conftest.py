import os
import pathlib

import dotenv
import pytest
from pytest_asyncio import fixture

from eidolon_ai_sdk.test_utils.machine import TestMachine

dotenv.load_dotenv()
os.environ["DISABLE_ANONYMOUS_METRICS"] = "true"  # machine is ran from subprocess, so disable metrics via envar


@fixture(scope="session")
def eidolon_examples():
    return pathlib.Path(__file__).parent.parent / "eidolon_examples"


@pytest.fixture(scope="session")
def machine(tmp_path_factory):
    return TestMachine(tmp_path_factory.mktemp("test_utils_storage"))


@pytest.fixture(autouse=True)
def state_manager(request, machine):
    machine.reset_state()
    yield
    machine.reset_state()


@fixture
def server_loc():
    return "http://localhost:5346"
