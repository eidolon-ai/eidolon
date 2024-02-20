from __future__ import annotations

from typing import Literal


from eidolon_ai_sdk.system.reference_model import Reference
from eidolon_ai_sdk.system.resources.resources_base import Resource


class AgentResource(Resource):
    kind: Literal["Agent"] = "Agent"
    spec: Reference[object, "Agent"]  # noqa: F821
