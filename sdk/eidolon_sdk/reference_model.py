from __future__ import annotations

import typing

from pydantic import BaseModel, model_validator

from eidolon_sdk.util.class_utils import for_name

T = typing.TypeVar('T', bound=BaseModel)


class Plugable(typing.Generic[T]):
    schema: T

    def __init__(self, *args, **kwargs):
        self.schema = kwargs['schema']


class Reference(BaseModel):
    _sub_class: typing.Type = Plugable
    implementation: str
    schema: dict = {}

    @model_validator(mode='after')
    def _validate(self):
        if not issubclass(self._sub_class, Plugable):
            raise ValueError(f"Implementation class '{self.implementation}' is not a Configurable.")
        self._build_schema(for_name(self.implementation, self._sub_class))
        return self

    def instantiate(self):
        impl_class = for_name(self.implementation, self._sub_class)
        return impl_class(schema=self._build_schema(impl_class))

    def _build_schema(self, impl_class):
        # todo, this needs to be more robust
        bases = getattr(impl_class, '__orig_bases__', None)
        if not bases:
            raise ValueError(f"Unable to find config object")
        schema_type, = bases[0].__args__
        return schema_type.model_validate(self.schema)
