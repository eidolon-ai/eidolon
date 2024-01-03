from __future__ import annotations

from typing import Literal

from eidos_sdk.system.reference_model import Reference
from eidos_sdk.system.resources.resources_base import Resource


class AgentResource(Resource):
    kind: Literal["Agent"] = "Agent"
    spec: Reference
