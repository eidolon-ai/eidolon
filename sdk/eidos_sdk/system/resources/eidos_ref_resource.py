from __future__ import annotations

from typing import Literal, Dict, Any

from eidos_sdk.system.resources.resources_base import Resource


class Reference(Resource):
    kind: Literal["Reference"] = "Reference"
    spec: Dict[str, Any] | str
