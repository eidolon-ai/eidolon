from __future__ import annotations

from typing import Literal, Dict, Any, Annotated

from pydantic import BeforeValidator

from eidos_sdk.system.resources.resources_base import Resource


def _nest_implementation(value):
    return dict(implementation=value) if isinstance(value, str) else value


class ReferenceResource(Resource):
    kind: Literal["Reference"] = "Reference"
    spec: Annotated[Dict[str, Any], BeforeValidator(_nest_implementation)]
