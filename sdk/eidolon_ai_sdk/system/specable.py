from __future__ import annotations

import textwrap
from typing import Generic, TypeVar

from pydantic import GetJsonSchemaHandler, BaseModel
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema as cs


T = TypeVar("T", bound=BaseModel)


class Specable(Generic[T]):
    """
    A generic type which can be used to describe a specable type. Specable types are expected to accept "spec" in kwarg.
    If Specable is not used, There will be no spec validation and the spec will be passed through as-is.
    """

    spec: T

    def __init__(self, spec: T, **kwargs: object):
        self.spec = spec

    @classmethod
    @property
    def __pydantic_core_schema__(cls):
        schema__ = cls.specable_cls().__pydantic_core_schema__
        schema__["ref"] = cls.__name__
        return schema__

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        ref = handler(core_schema)
        json_schema = handler.resolve_ref_schema(ref)
        json_schema["title"] = cls.__name__
        if "extra" not in cls.specable_cls().model_config:  # default to no extra props
            json_schema["additionalProperties"] = False
        if "description" not in json_schema and cls.specable_cls().__doc__:
            json_schema["description"] = textwrap.dedent(cls.specable_cls().__doc__).strip()
        return json_schema

    @classmethod
    def specable_cls(cls):
        bases = getattr(cls, "__orig_bases__", [])
        specable = next(
            (base for base in bases if getattr(base, "__origin__", None) is Specable),
            None,
        )
        if specable:
            return specable.__args__[0]
        else:
            raise ValueError(f"Specable base {cls} not found")
