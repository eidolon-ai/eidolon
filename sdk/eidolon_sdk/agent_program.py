from pydantic import BaseModel, Field

from .agent_cpu import AgentCPU
from .util.schema_to_model import schema_to_model


class AgentIOState(BaseModel):
    state_name: str = Field(..., description="The name of the state.")
    input_schema: dict = Field(..., description="The schema of the input.")
    transitions_to: dict[str, dict] = Field(..., description="The transitions to other states. The key is the name of the state "
                                                             "to transition to, and the value is the schema of the output.")

    def __init__(self):
        super().__init__()
        self.input_schema_model = schema_to_model(self.input_schema, f'{self.state_name.capitalize()}InputModel')
        self.transitions_to_models = {}
        for key, value in self.transitions_to.items():
            self.transitions_to_models[key] = schema_to_model(value, f'{self.state_name.capitalize()}To{key.capitalize()}OutputModel')


class AgentProgram(BaseModel):
    agent_cpu: AgentCPU = Field(..., description="The Agent CPU to use.")
    implementation: str = Field(..., description="The FQN of agent class.")
    states: dict[str, AgentIOState] = Field(..., description="The states of the program.")
    initial_state: str = Field(..., description="The initial state of the program.")
