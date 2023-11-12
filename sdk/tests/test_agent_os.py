import yaml

from eidolon_sdk.agent_machine import AgentMachine
from eidolon_sdk.agent_os import AgentOS
from fastapi.testclient import TestClient


def get_client(machine):
    os = AgentOS(yaml.dump(machine.model_dump()))
    os.start()
    return TestClient(os.app)


def test_empty_start():
    client = get_client(AgentMachine(agent_memory={}, agent_io={}, agent_programs=[]))
    docs = client.get("/docs")
    assert docs.status_code == 200
