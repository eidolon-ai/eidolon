from __future__ import annotations

from typing import Literal, Dict, Any

from eidos_sdk.system.resources.resources_base import Resource


class ReferenceResource(Resource):
    kind: Literal["Reference"] = "Reference"
    spec: Dict[str, Any] | str
