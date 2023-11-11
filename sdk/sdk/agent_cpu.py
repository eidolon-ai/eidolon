from __future__ import annotations

from typing import Generic

from agent_os import Agent, T, V

agent_cpu_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "AgentCPUProcessingUnitDescriptors",
    "type": "object",
    "properties": {
        "MemoryUnit": {
            "type": "object",
            "properties": {
                "implementation": {
                    "type": "string",
                    "description": "The FQN name of an implementation."
                }
            },
            "required": ["implementation"]
        },
        "ControlUnit": {
            "type": "object",
            "properties": {
                "implementation": {
                    "type": "string",
                    "description": "The FQN name of an implementation."
                }
            },
            "required": ["implementation"]
        },
        "LLMUnit": {
            "type": "object",
            "properties": {
                "implementation": {
                    "type": "string",
                    "description": "The FQN name of an implementation."
                },
                "model": {
                    "type": "string",
                    "description": "The name of the language model used by the LLM Unit."
                }
            },
            "required": ["implementation", "model"]
        },
        "LogicUnits": {
            "type": "array",
            "description": "The list of Logic Units to use.",
            "items": {
                "type": "object",
                "properties": {
                    "implementation": {
                        "type": "string",
                        "description": "The FQN name of an implementation."
                    }
                },
                "required": ["implementation"]
            }
        }
    },
    "required": ["MemoryUnit", "ControlUnit", "LLMUnit", "LogicUnits"]
}


class LogicUnit:
    @staticmethod
    async def execute(instruction, agent: Agent) -> None:
        # unsure of the object we pass of to manipulate framework. Calling it agent for now
        pass


class MemoryUnit:
    @staticmethod
    async def process(prompt, agent: Agent):  # this probably returns whatever a prompt object is
        pass


class ControlUnit(Generic[T, V]):
    @staticmethod
    async def process(request: T, agent: Agent) -> V:
        pass


class LLMUnit:
    @staticmethod
    async def query(prompt):
        pass


class AgentCPU:
    def __init__(self, cpu_configuration: str):
        self.cpu_configuration = cpu_configuration

    def config(self):
        pass
