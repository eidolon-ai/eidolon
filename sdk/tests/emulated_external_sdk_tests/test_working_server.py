from pathlib import Path

import pytest
from pytest_asyncio import fixture

from eidolon_ai_client.client import Agent, Machine
from eidolon_ai_sdk.system.resources.resources_base import load_resources
from eidolon_ai_sdk.test_utils.machine import TestMachine
from eidolon_ai_sdk.test_utils.server import serve_thread
from eidolon_ai_sdk.test_utils.vcr import vcr_patch


@fixture(scope="module")
def machine(tmp_path_factory):
    return TestMachine(tmp_path_factory.mktemp("test_utils_storage"))


@fixture(scope="module", autouse=True)
def server(machine):
    resources = load_resources([Path(__file__).parent / "resources"])
    with serve_thread([machine, *resources]):
        yield


@fixture(autouse=True)
def state_manager(test_name, machine):
    machine.reset_state()
    with vcr_patch(test_name):
        yield
    machine.reset_state()


@pytest.mark.vcr
def test_can_start_server():
    pass


@pytest.mark.vcr
async def test_can_create_process():
    process = await Agent.get("hello_world").create_process()
    response = await process.action("converse", "hi! what is the capital of france?")
    assert "paris" in response.data.lower()


@pytest.mark.vcr
async def test_state_does_not_leach_between_tests():
    found = await Machine().processes()
    assert not found.processes

