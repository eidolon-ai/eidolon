from __future__ import annotations

from typing import List

from pydantic import BaseModel

from eidolon_ai_sdk.apu.agents_logic_unit import AgentsLogicUnit, AgentsLogicUnitSpec
from eidolon_ai_sdk.apu.apu import APU
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from eidolon_ai_sdk.system.specable import Specable


class AgentSpec(BaseModel):
    apu: AnnotatedReference[APU]
    agent_refs: List[str] = []


class Agent(Specable[AgentSpec]):
    apu: APU

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apu = self.spec.apu.instantiate()
        if self.spec.agent_refs and hasattr(self.apu, "logic_units"):
            self.apu.logic_units.append(
                AgentsLogicUnit(
                    processing_unit_locator=self.apu,
                    spec=AgentsLogicUnitSpec(agents=self.spec.agent_refs),
                )
            )
