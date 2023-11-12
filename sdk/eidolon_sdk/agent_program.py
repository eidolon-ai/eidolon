import importlib

from pydantic import BaseModel, Field, ValidationError, field_validator

from agent import CodeAgent
from .agent_cpu import AgentCPU
from .util.schema_to_model import schema_to_model


class AgentIOState(BaseModel):
    state_name: str = Field(description="The name of the state.")
    input_schema: dict = Field(description="The schema of the input.")
    transitions_to: dict[str, dict] = Field(
        description="The transitions to other states. The key is the name of the state "
                    "to transition to, and the value is the schema of the output.")

    def __init__(self):
        super().__init__()
        self.input_schema_model = schema_to_model(self.input_schema, f'{self.state_name.capitalize()}InputModel')
        self.transitions_to_models = {}
        for key, value in self.transitions_to.items():
            self.transitions_to_models[key] = schema_to_model(value, f'{self.state_name.capitalize()}To{key.capitalize()}OutputModel')


class AgentProgram(BaseModel):
    """
    The `AgentProgram` class represents a program within the agent framework. It serves as a configuration object
    for setting up the program's properties and linking it to a specific Agent CPU. It defines the program's behavior,
    states, and the initial state that the program should be in when it starts.

    Attributes:
        name (str): The name of the program. This is a unique identifier that will also be used as the endpoint name
                    for the program's interface.
        agent_cpu (AgentCPU, optional): An instance of `AgentCPU` that this program will use to execute its instructions.
                                        If not provided, it will default to `None`.
        implementation (str): The Fully Qualified Name (FQN) of the agent class that implements the program logic.
        states (dict[str, AgentIOState]): A mapping of state names to their corresponding `AgentIOState` objects,
                                          defining possible states that the program can be in.
        initial_state (str): The name of the initial state of the program upon startup.

    The `AgentProgram` class requires that you provide the `name`, `implementation`, and `initial_state` upon creation.
    The `agent_cpu` and `states` are optional and can be set after initialization.
    """
    name: str = Field(description="The name of the program. Will be used as the endpoint name.")
    agent_cpu: AgentCPU = Field(default=None, description="The Agent CPU to use.")
    implementation: str = Field(description="The FQN of agent class.")
    states: dict[str, AgentIOState] = Field(description="The states of the program.")
    initial_state: str = Field(description="The initial state of the program.")

    @classmethod
    @field_validator('agent_cpu', mode="before")
    def validate_agent_cpu(cls, v, values):
        # Dynamically import the class from the implementation field
        implementation_fqn = values.get('implementation')
        if implementation_fqn:
            module_name, class_name = implementation_fqn.rsplit(".", 1)
            try:
                module = importlib.import_module(module_name)
                impl_class = getattr(module, class_name)
            except (ImportError, AttributeError):
                raise ValidationError(f"Unable to import {implementation_fqn}")

            # Check if the class is a subclass of CodeAgent
            if issubclass(impl_class, CodeAgent):
                return v  # agent_cpu is optional for CodeAgent

            # If not a CodeAgent, and agent_cpu is not provided, raise an error
            if not v:
                raise ValueError('agent_cpu is required for non-CodeAgent implementations')
        else:
            raise ValidationError("implementation is required")

        return v
