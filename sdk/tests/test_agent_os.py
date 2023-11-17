from __future__ import annotations

import contextlib
from typing import Annotated, Type, List, Literal

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pydantic import BaseModel, Field

from eidolon_sdk.agent import CodeAgent, Agent, initializer, register_action, AgentState
from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.agent_memory import AgentMemory, SymbolicMemory
from eidolon_sdk.agent_os import AgentOS
from eidolon_sdk.agent_program import AgentProgram
from eidolon_sdk.cpu.agent_cpu import AgentCPU
from eidolon_sdk.cpu.agent_io import UserTextCPUMessage
from eidolon_sdk.impl.local_symbolic_memory import LocalSymbolicMemory


@pytest.fixture
def app():
    return FastAPI()


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def os_manager(app):
    @contextlib.contextmanager
    def fn(*agents: Type[Agent], memory_override: SymbolicMemory = None):
        machine = AgentMachine(AgentMemory(symbolic_memory=memory_override or LocalSymbolicMemory()), [])
        machine.agent_programs = [AgentProgram(
            name=agent.__name__.lower(),
            agent=agent(machine, AgentCPU(machine))
        ) for agent in agents]
        os = AgentOS(machine=machine)
        os.start(app)
        try:
            yield
        finally:
            os.stop()

    return fn


class HelloWorldResponse(BaseModel):
    question: str
    answer: str


class HelloWorld(CodeAgent):
    counter = 0  # todo, this is a hack to make sure function is called. Should wrap with mock instead

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        HelloWorld.counter = 0

    @initializer
    async def idle(self, question: Annotated[
        str, Field(description="The question to ask. Can be anything, but it better be hello")]):
        HelloWorld.counter += 1
        if question == "hello":
            return HelloWorldResponse(question=question, answer="world")
        elif question == "exception":
            raise Exception("some unexpected error")
        else:
            raise HTTPException(status_code=501, detail="huge system error handling unprecedented edge case")


@pytest.fixture(autouse=True)
def memory():
    return LocalSymbolicMemory()


def test_empty_start(client, os_manager):
    with os_manager():
        docs = client.get("/docs")
        assert docs.status_code == 200


def test_program(client, os_manager):
    with os_manager(HelloWorld):
        response = client.post("/programs/helloworld", json=dict(question="hello"))
        assert response.status_code == 200


def test_program_actually_calls_code(client, os_manager):
    with os_manager(HelloWorld):
        client.post("/programs/helloworld", json=dict(question="hello"))
        assert HelloWorld.counter == 1


def test_program_automatically_terminates_if_no_new_state_provided(client, os_manager):
    with os_manager(HelloWorld):
        pid = client.post("/programs/helloworld", json=dict(question="hello")).json()['process_id']
        response = client.get(f"/programs/helloworld/processes/{pid}/status")
        assert response.status_code == 200
        assert response.json()['state'] == 'terminated'


class ParamTester(CodeAgent):
    last_call = None

    @initializer
    async def foo(self, x: int, y: int = 5, z: Annotated[int, Field(description="z is a param")] = 10):
        ParamTester.last_call = (x, y, z)
        return dict(x=x, y=y, z=z)


def test_non_annotated_params(client, os_manager):
    with os_manager(ParamTester):
        response = client.post("/programs/paramtester", json=dict(x=1, y=2, z=3))
        assert response.status_code == 200
        assert ParamTester.last_call == (1, 2, 3)


def test_defaults(client, os_manager):
    with os_manager(ParamTester):
        response = client.post("/programs/paramtester", json=dict(x=1))
        assert response.status_code == 200
        assert ParamTester.last_call == (1, 5, 10)


def test_required_param_missing(client, os_manager):
    with os_manager(ParamTester):
        response = client.post("/programs/paramtester", json=dict())
        assert response.status_code == 422


def test_required_param_missing_with_no_body(client, os_manager):
    with os_manager(ParamTester):
        response = client.post("/programs/paramtester")
        assert response.status_code == 422


@pytest.mark.parametrize("db", ["mongo", "local"])
@pytest.mark.asyncio
async def test_async_retrieve_result(async_client, os_manager, symbolic_memory, db):
    with os_manager(HelloWorld, memory_override=symbolic_memory if db == "mongo" else None):
        post = await async_client.post("/programs/helloworld", json=dict(question="hello"),
                                       headers={'execution-mode': 'async'})
        assert post.status_code == 202
        response = await async_client.get(f"/programs/helloworld/processes/{post.json()['process_id']}/status")
        assert response.status_code == 200
        assert response.json()['data'] == dict(question="hello", answer="world")


@pytest.mark.parametrize("db", ["mongo", "local"])
@pytest.mark.asyncio
async def test_program_http_error(async_client, os_manager, symbolic_memory, db):
    with os_manager(HelloWorld, memory_override=symbolic_memory if db == "mongo" else None):
        response = await async_client.post("/programs/helloworld", json=dict(question="hola"))
        assert response.json()['detail'] == "huge system error handling unprecedented edge case"


def test_program_error(client, os_manager):
    with os_manager(HelloWorld):
        response = client.post("/programs/helloworld", json=dict(question="exception"))
        assert response.status_code == 500
        assert response.json()['error'] == "some unexpected error"


class MemTester(CodeAgent):
    @initializer
    async def add(self, x: int):
        await self.agent_memory.symbolic_memory.insert_one("test", dict(x=x))


# todo, lets parameterize this one with mongo as well
@pytest.mark.parametrize("db", ["mongo", "local"])
@pytest.mark.asyncio
async def test_programs_can_call_memory(async_client, os_manager, memory, symbolic_memory, db):
    if db == "mongo":
        memory = symbolic_memory
    with os_manager(MemTester, memory_override=memory):
        await async_client.post("/programs/memtester", json=dict(x=1))
        found = await memory.find_one("test", dict(x=1))
        assert found
        assert found['x'] == 1


class StateTester(CodeAgent):
    @initializer
    async def foo(self):
        return AgentState(name="a", data=dict())

    @register_action("a", "b")
    async def bar(self, next_state: str):
        return AgentState(name=next_state, data=dict())


def test_can_transition_state(client, os_manager):
    with os_manager(StateTester):
        post = client.post("/programs/statetester", json={})
        pid = post.json()['process_id']
        assert client.get(f"/programs/statetester/processes/{pid}/status").json()['state'] == "a"
        assert client.post(f"/programs/statetester/processes/{pid}/actions/bar",
                           json=dict(next_state="b")).status_code == 200
        assert client.get(f"/programs/statetester/processes/{pid}/status").json()['state'] == "b"


def test_enforced_state_limits(client, os_manager):
    with os_manager(StateTester):
        post = client.post("/programs/statetester", json={})
        pid = post.json()['process_id']
        assert client.get(f"/programs/statetester/processes/{pid}/status").json()['state'] == "a"
        assert client.post(f"/programs/statetester/processes/{pid}/actions/bar",
                           json=dict(next_state="c")).status_code == 200
        assert client.get(f"/programs/statetester/processes/{pid}/status").json()['state'] == "c"
        assert client.post(f"/programs/statetester/processes/{pid}/actions/bar",
                           json=dict(next_state="c")).status_code == 409


@pytest.mark.skip("todo, this needs some special handling")
def test_empty_body_functions_if_no_args_required(client, os_manager):
    with os_manager(StateTester):
        assert client.post("/programs/statetester").status_code == 200


class PidTester(CodeAgent):
    @initializer
    async def foo(self):
        return dict(agent_found_pid=self.get_context().process_id)


def test_agents_can_read_process_id(client, os_manager):
    with os_manager(PidTester):
        post = client.post("/programs/pidtester", json={})
        assert post.json()['process_id'] == post.json()['data']['agent_found_pid']


class CpuResponse(BaseModel):
    response: str


class CpuTester(Agent):
    @initializer
    async def foo(self):
        return await self.cpu_request([UserTextCPUMessage(prompt="foo")], {}, CpuResponse.model_json_schema())


@pytest.mark.skip("this is not working yet. Not sure where bug is.")
def test_agent_can_use_cpu(client, os_manager):
    with os_manager(CpuTester):
        post = client.post("/programs/cputester", json={})
        assert post.status_code == 200
        assert post.json()['data'] == dict(foo="bar")


class DocumentedBase(BaseModel):
    some_int: int


class ExtendedStateChange(AgentState[DocumentedBase]):
    name: Literal['scoped_name']


class Documented(CodeAgent):
    @initializer
    async def init(self, x: int) -> dict[str, int]:
        pass

    @register_action("a")
    async def no_types(self):
        pass

    @register_action("a")
    async def dict_response(self) -> dict:
        pass

    @register_action("a")
    async def base_model_response(self) -> DocumentedBase:
        pass

    @register_action("a")
    async def param_keys(self, x: str, y: List[int], z: DocumentedBase):
        pass

    @register_action("a")
    async def state_response(self) -> AgentState[DocumentedBase]:
        pass

    @register_action("a")
    async def inherited_state_response(self) -> AgentState[DocumentedBase]:
        pass


class TestOpenApiDocs:
    @pytest.fixture()
    def openapi_schema(self, client, os_manager):
        with os_manager(Documented):
            # Get the OpenAPI schema
            yield client.get("/openapi.json").json()

    def test_registers_expected_paths(self, openapi_schema):
        assert '/programs/documented' in openapi_schema['paths']
        assert '/programs/documented/processes/{process_id}/status' in openapi_schema['paths']
        assert '/programs/documented/processes/{process_id}/actions/no_types' in openapi_schema['paths']

    def test_init_is_not_registered(self, openapi_schema):
        assert '/programs/documented/processes/{process_id}/actions/init' not in openapi_schema['paths']
        assert '/programs/documented/processes/{process_id}/actions/INIT' not in openapi_schema['paths']

    def test_params_are_well_handled(self, openapi_schema):
        assert action_request_schema(openapi_schema, 'param_keys') == {
            'properties': {'x': {'type': 'string', 'title': 'X'},
                           'y': {'items': {'type': 'integer'}, 'type': 'array', 'title': 'Y'},
                           'z': {'$ref': '#/components/schemas/DocumentedBase'}}, 'type': 'object',
            'required': ['x', 'y', 'z'], 'title': 'Param_keysInputModel'}

    def test_no_params(self, openapi_schema):
        assert action_request_schema(openapi_schema, 'no_types') == {'type': 'object', 'title': 'No_typesInputModel',
                                                                     'properties': {}}

    def test_response_types(self, openapi_schema):
        assert action_response_schema(openapi_schema, 'no_types') == {}
        assert action_response_schema(openapi_schema, 'dict_response') == {'type': 'object'}

    def test_model_response(self, openapi_schema):
        assert action_response_referenced_schema(openapi_schema, 'base_model_response')['required'] == ['some_int']

    def test_model_with_state_change(self, openapi_schema):
        assert action_response_referenced_schema(openapi_schema, 'state_response')['required'] == ['some_int']

    def test_model_with_inherited_state_change(self, openapi_schema):
        assert action_response_referenced_schema(openapi_schema, 'inherited_state_response')['required'] == ['some_int']

    def test_root_does_not_have_process_id_param_arg(self, openapi_schema):
        assert 'parameters' not in openapi_schema['paths']['/programs/documented']['post']

    def test_actions_do_have_process_id_param_arg(self, openapi_schema):
        assert openapi_schema['paths']['/programs/documented/processes/{process_id}/actions/no_types']['post'][
                   'parameters'] == [
                   {'name': 'process_id', 'in': 'path', 'required': True,
                    'schema': {'type': 'string', 'title': 'Process Id'}}
               ]

    def test_get_status_endpoint_does_have_process_id_param_arg(self, openapi_schema):
        assert openapi_schema['paths']['/programs/documented/processes/{process_id}/status']['get']['parameters'] == [
            {'name': 'process_id', 'in': 'path', 'required': True, 'schema': {'type': 'string', 'title': 'Process Id'}}
        ]


def action_request_schema(openapi_schema, action):
    body_ref = openapi_schema['paths'][('/programs/documented/processes/{process_id}/actions/%s' % action)]['post'][
        'requestBody']['content']['application/json']['schema']['$ref']
    return openapi_schema['components']['schemas'][body_ref.split("/")[-1]]


def action_response_schema(openapi_schema, action):
    body_ref = openapi_schema['paths'][('/programs/documented/processes/{process_id}/actions/%s' % action)]['post'][
        'responses']['200']['content']['application/json']['schema']['$ref']
    data_ = openapi_schema['components']['schemas'][body_ref.split("/")[-1]]['properties']['data']

    # these two fields should be present, but we don't care what their value is since it is likely to change with time
    del data_['title']
    del data_['description']
    return data_


def action_response_referenced_schema(openapi_schema, action):
    body_ref = openapi_schema['paths'][('/programs/documented/processes/{process_id}/actions/%s' % action)]['post'][
        'responses']['200']['content']['application/json']['schema']['$ref']
    sub_ref = openapi_schema['components']['schemas'][body_ref.split("/")[-1]]['properties']['data']['allOf'][0]['$ref']
    return openapi_schema['components']['schemas'][sub_ref.split("/")[-1]]
