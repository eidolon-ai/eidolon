from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

from pydantic import BaseModel, Field, field_validator, ValidationError

from eidolon_sdk.agent import Agent

T = TypeVar('T')
V = TypeVar('V')


class LogicUnit(BaseModel, ABC):
    @abstractmethod
    async def execute(self, instruction, framework) -> None:
        # unsure of the object we pass of to manipulate framework.
        pass


class MemoryUnit(BaseModel, ABC):
    @abstractmethod
    async def process(self, prompt, agent):  # this probably returns whatever a prompt object is
        pass


class ControlUnit(BaseModel, Generic[T, V], ABC):
    @abstractmethod
    async def process(self, request: T, agent: Agent) -> V:
        pass


class LLMUnit(BaseModel, ABC):
    model: str = Field(..., description="The name of the language model used by the LLM Unit.")

    @abstractmethod
    async def query(self, prompt):
        pass


base_class_dict = {
    "memory_unit": MemoryUnit,
    "control_unit": ControlUnit,
    "llm_unit": LLMUnit,
    "logic_units": LogicUnit
}


class AgentCPU(BaseModel):
    """
    Defines the central processing unit (CPU) of an agent, which is responsible for managing the execution
    of logic units and interfacing with the memory and control units.

    Attributes:
        memory_unit (MemoryUnit): An instance of `MemoryUnit` that provides the memory storage capabilities for the CPU.
        control_unit (ControlUnit): An instance of `ControlUnit` that directs the operation of the CPU by coordinating
                                    the instruction cycle, including fetching, decoding, and executing instructions.
        llm_unit (LLMUnit): An instance of `LLMUnit` that facilitates the interaction with a Large Language Model (LLM).
        logic_units (List[LogicUnit]): A list of `LogicUnit` instances that perform various logical operations as part
                                       of the CPU's processing tasks.

    The class also includes a class-level validator that ensures the instantiated units are derived from the correct base classes.
    """

    memory_unit: MemoryUnit = Field(description="The Memory Unit to use.")
    control_unit: ControlUnit = Field(description="The Control Unit to use.")
    llm_unit: LLMUnit = Field(description="The LLM Unit to use.")
    logic_units: List[LogicUnit] = Field(description="The list of Logic Units to use.")

    # A validator to instantiate the correct class based on the implementation name
    @classmethod
    @field_validator('memory_unit', 'control_unit', 'llm_unit', "logic_units")
    def validate_units(cls, value, values, config, field):
        """
        Validates and instantiates units for the AgentCPU based on the provided implementation details.

        This method dynamically imports and instantiates classes for the specified units based on the 'implementation'
        attribute within the provided value. It supports validating and instantiating single units as well as lists of units.

        Parameters:
            value: The value containing the implementation details for the unit or list of units.
            values (dict): A dictionary containing all the fields of the AgentCPU instance.
            config: The configuration passed to the Pydantic model.
            field: The model's field that is being validated.

        Raises:
            ValidationError: If the specified implementation cannot be imported or is not provided.
            ValueError: If the implementation class is not found or is not a subclass of the expected base class.

        Returns:
            An instantiated unit object or a list of instantiated unit objects that have been validated.
        """

        if 'implementation' in value:
            base_class = base_class_dict.get(field.name)
            implementation_fqn = values.get('implementation')
            if implementation_fqn:
                module_name, class_name = implementation_fqn.rsplit(".", 1)
                try:
                    module = importlib.import_module(module_name)
                    implementation_class = getattr(module, class_name)
                except (ImportError, AttributeError):
                    raise ValidationError(f"Unable to import {implementation_fqn}")
            else:
                raise ValidationError("Implementation not provided.")

            if implementation_class and issubclass(implementation_class, base_class):
                return implementation_class(**value)
            else:
                raise ValueError(
                    f"Implementation class '{value['implementation']}' not found or is not a subclass of {field.name}.")
        elif isinstance(value, list):
            return [cls.validate_units(item, values, config, field) for item in value]

        raise ValueError("Implementation not provided.")

    def config(self, cpu_configuration: str):
        pass
