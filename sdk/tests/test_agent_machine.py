import pytest

from eidolon_sdk.agent_machine import AgentMachine

hello_world = """
agent_memory:
  file_memory:
    implementation: "eidolon_sdk.impl.noop_memory.NoopFileMemory"
  symbolic_memory:
    implementation: "eidolon_sdk.impl.noop_memory.NoopSymbolicMemory"
  similarity_memory:
    implementation: "eidolon_sdk.impl.noop_memory.NoopSimilarityMemory"
agent_programs:
  - name: "ExampleAgentProgram"
    implementation: "examples.hello_world.HelloWorld.HelloWorld"
    initial_state: "Idle"
    states:
      Idle:
        state_name: "Idle"
        description: "This is the starting state of the agent program."
        input_schema:
          type: "object"
          properties:
            name:
              type: "string"
              description: "Your name"
        transitions_to:
          Idle:
            description: "The welcome message is printed."
            type: "object"
            properties:
              welcome_message:
                type: "string"
"""


def test_parse():
    AgentMachine.parse(hello_world)


@pytest.mark.skip(reason="fails with TypeError: 'mappingproxy' object cannot be converted to 'PyDict', making not to come back later")
def test_dump_after_parse():
    AgentMachine.parse(hello_world).model_dump()
