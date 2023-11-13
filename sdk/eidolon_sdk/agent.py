from __future__ import annotations

from typing import Dict, Any

from .agent_program import AgentProgram


class Agent:
    def __init__(self, agent_program: AgentProgram):
        self.agent_program = agent_program

    async def execute(self, state_name: str, input: Dict[str, Any]):
        pass


class CodeAgent(Agent):
    pass
