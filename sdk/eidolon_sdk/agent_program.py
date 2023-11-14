import importlib

from pydantic import BaseModel, Field, ValidationError, field_validator

from .agent_cpu import AgentCPU


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
        initial_state (str): The name of the initial state of the program upon startup.

    The `AgentProgram` class requires that you provide the `name`, `implementation`, and `initial_state` upon creation.
    The `agent_cpu` and `states` are optional and can be set after initialization.
    """
    name: str = Field(description="The name of the program. Will be used as the endpoint name.")
    agent_cpu: AgentCPU = Field(default=None, description="The Agent CPU to use.")
    implementation: str = Field(description="The FQN of agent class.")

    @classmethod
    @field_validator('implementation', mode="before")
    def validate_agent_cpu(cls, v, values):
        """
        Validates the 'agent_cpu' field of the AgentProgram class. This method ensures that the specified 'agent_cpu'
        is appropriate for the given 'implementation' of the agent. If the 'implementation' is a subclass of `CodeAgent`,
        the 'agent_cpu' field is optional. Otherwise, it is required.

        This is a class method decorated with `field_validator` which checks the 'agent_cpu' field before other validations.

        Parameters:
            v: The value of 'agent_cpu' to be validated.
            values (dict): A dictionary containing all the fields of the AgentProgram instance.

        Raises:
            ValidationError: If 'implementation' cannot be imported or is not provided, or if 'agent_cpu' is required
                             but not provided for non-CodeAgent implementations.

        Returns:
            The validated 'agent_cpu' if the validation is successful.

        This method uses dynamic importing based on the 'implementation' field to fetch the agent class and then determines
        the necessity of 'agent_cpu' based on whether the agent class is a subclass of `CodeAgent`.

        Note:
            This method should be considered as part of the internal API of the AgentProgram class and should not be
            invoked directly in normal usage.
        """

        # Dynamically import the class from the implementation field
        implementation_fqn = v.get('implementation')
        if implementation_fqn:
            module_name, class_name = implementation_fqn.rsplit(".", 1)
            try:
                module = importlib.import_module(module_name)
                impl_class = getattr(module, class_name)
            except (ImportError, AttributeError):
                raise ValidationError(f"Unable to import {implementation_fqn}")

            from .agent import CodeAgent
            # Check if the class is a subclass of CodeAgent
            if issubclass(impl_class, CodeAgent):
                return v  # agent_cpu is optional for CodeAgent

            # If not a CodeAgent, and agent_cpu is not provided, raise an error
            if not v:
                raise ValueError('agent_cpu is required for non-CodeAgent implementations')
        else:
            raise ValidationError("implementation is required")

        return v
