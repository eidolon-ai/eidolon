from __future__ import annotations

from typing import Literal, Dict, Any, Annotated

from pydantic import BeforeValidator, AfterValidator

from eidolon_ai_sdk.system.resources.resources_base import Resource, Metadata


def _nest_implementation(value):
    return dict(implementation=value) if isinstance(value, str) else value


def _not_default(value: Metadata):
    if value.name == "DEFAULT":
        raise ValueError("Must name references")
    return value


class ReferenceResource(Resource):
    kind: Literal["Reference"] = "Reference"
    metadata: Annotated[Metadata, AfterValidator(_not_default)]
    spec: Annotated[Dict[str, Any], BeforeValidator(_nest_implementation)]
