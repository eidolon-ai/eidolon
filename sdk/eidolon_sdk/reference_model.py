from __future__ import annotations

import typing

from pydantic import BaseModel, model_validator

from eidolon_sdk.util.class_utils import for_name

T = typing.TypeVar('T', bound=BaseModel)


class Plugable(typing.Generic[T]):
    spec: T

    def __init__(self, *args, **kwargs):
        self.spec = kwargs['spec']


class ReferenceMeta(type):
    def __getitem__(cls, key):
        class GenericReference(BaseModel):
            _sub_class: typing.Type = key
            implementation: str
            spec: dict = {}

            @model_validator(mode='after')
            def _validate(self):
                if not issubclass(self._sub_class, Plugable):
                    raise ValueError(f"Implementation class '{self.implementation}' is not a Plugable.")
                self._build_spec(for_name(self.implementation, self._sub_class))
                return self

            def instantiate(self):
                impl_class = for_name(self.implementation, self._sub_class)
                return impl_class(spec=self._build_spec(impl_class))

            def _build_spec(self, impl_class):
                # todo, this needs to be more robust
                bases = getattr(impl_class, '__orig_bases__', None)
                if not bases:
                    raise ValueError(f"Unable to find config object")
                spec_type, = bases[0].__args__
                return spec_type.model_validate(self.spec)

        return GenericReference


class Reference(metaclass=ReferenceMeta):
    pass

    def instantiate(self):
        pass
