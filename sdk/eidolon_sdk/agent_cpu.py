from __future__ import annotations

import importlib
from typing import Generic, TypeVar, List

from pydantic import BaseModel, Field, field_validator, ValidationError

from agent import Agent

T = TypeVar('T')
V = TypeVar('V')


class LogicUnit(BaseModel):
    @staticmethod
    async def execute(instruction, framework) -> None:
        # unsure of the object we pass of to manipulate framework.
        pass


class MemoryUnit(BaseModel):
    @staticmethod
    async def process(prompt, agent):  # this probably returns whatever a prompt object is
        pass


class ControlUnit(BaseModel, Generic[T, V]):
    @staticmethod
    async def process(request: T, agent: Agent) -> V:
        pass


class LLMUnit(BaseModel):
    model: str = Field(..., description="The name of the language model used by the LLM Unit.")

    @staticmethod
    async def query(prompt):
        pass


base_class_dict = {
    "memory_unit": MemoryUnit,
    "control_unit": ControlUnit,
    "llm_unit": LLMUnit,
    "logic_units": LogicUnit
}


class AgentCPU(BaseModel):
    memory_unit: MemoryUnit = Field(description="The Memory Unit to use.")
    control_unit: ControlUnit = Field(description="The Control Unit to use.")
    llm_unit: LLMUnit = Field(description="The LLM Unit to use.")
    logic_units: List[LogicUnit] = Field(description="The list of Logic Units to use.")

    # A validator to instantiate the correct class based on the implementation name
    @classmethod
    @field_validator('memory_unit', 'control_unit', 'llm_unit', "logic_units")
    def validate_units(cls, value, values, config, field):
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
