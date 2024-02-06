from __future__ import annotations

from typing import Literal

from eidolon_ai_sdk.system.agent_machine import AgentMachine
from eidolon_ai_sdk.system.reference_model import AnnotatedReference
from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata


class MachineResource(Resource):
    kind: Literal["Machine"] = "Machine"
    metadata: Metadata
    spec: AnnotatedReference[AgentMachine]
