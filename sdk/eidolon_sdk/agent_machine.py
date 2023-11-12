from typing import List

import yaml
from pydantic import Field, BaseModel, field_validator

from agent_memory import AgentMemory
from agent_program import AgentProgram
from agent_io import AgentIO

base_class_dict = {
    "agent_memory": AgentMemory,
    "agent_io": AgentIO,
}


class AgentMachine(BaseModel):
    """
    Represents the execution environment for agent programs within the EidolonOS framework.

    The AgentMachine class encapsulates the necessary components to run and manage
    agent programs. It holds references to the agent's memory, I/O, and a list of
    programs that the machine can execute.

    Attributes:
        agent_memory (AgentMemory): The memory component where the agent stores
            its episodes, semantic thoughts, and procedural knowledge. It is a
            critical part of the agent's ability to maintain state across interactions.
        agent_io (AgentIO): The input/output system configured for the agent that
            allows it to interact with the external world or other systems.
        agent_programs (List[AgentProgram]): A list of AgentProgram instances that
            contains the executable code and associated descriptors for the agent's
            actions.

    Class Methods:
        validate_units: Validates that the provided units for memory and I/O have the
            correct implementation based on the provided descriptors. It ensures that
            the implementations are subclasses of the expected base classes.

    Static Methods:
        parse(machine_description: str): Parses a string representation of the machine
            description, typically in YAML format, into an instance of AgentMachine.

    Raises:
        ValueError: If the implementation class for memory or I/O is not found, or
            if it is not a subclass of the expected base class, a ValueError is raised.
    """

    agent_memory: AgentMemory = Field(..., description="The Agent Memory to use.")
    agent_io: AgentIO = Field(..., description="The Agent IO configured on this machine.")
    agent_programs: List[AgentProgram] = Field(..., description="The list of Agent Programs to run on this machine.")

    @classmethod
    @field_validator('agent_memory', 'agent_io')
    def validate_units(cls, value, field):
        """
        Validates that the memory and I/O units provided have implementations that
        are subclasses of the specified base classes for each respective field.

        Args:
            value (dict): The value containing the 'implementation' key with the name
                of the class to be validated.
            field (str): The name of the field being validated, either 'agent_memory'
                or 'agent_io'.

        Returns:
            The instantiated implementation class if validation is successful.

        Raises:
            ValueError: If 'implementation' key is not in the value, if the implementation
                class is not found, or if the found class is not a subclass of the
                base class corresponding to the field.
        """

        if 'implementation' in value:
            base_class = base_class_dict.get(field.name)
            implementation_class = globals().get(value['implementation'])
            if implementation_class and issubclass(implementation_class, base_class):
                return implementation_class()
            else:
                raise ValueError(f"Implementation class '{value['implementation']}' not found or is not a subclass of {field.name}.")
        raise ValueError("Implementation not provided.")

    @staticmethod
    def parse(machine_description: str):
        """
        Parses a YAML string describing an AgentMachine into an AgentMachine instance.

        Args:
            machine_description (str): A string in YAML format that describes the
                configuration and components of the AgentMachine.

        Returns:
            AgentMachine: An instantiated AgentMachine object based on the parsed
                description.
        """

        machine_descriptor = yaml.safe_load(machine_description)
        return AgentMachine(**machine_descriptor)
