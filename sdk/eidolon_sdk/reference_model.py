from __future__ import annotations

import typing

from pydantic import BaseModel, model_validator

from eidolon_sdk.util.class_utils import for_name

T = typing.TypeVar('T', bound=BaseModel)


# Type wrapper to describe the config type which is expected. If not specable, spec is passed in un-validated
class Specable(typing.Generic[T]):
    spec: T


class ReferenceMeta(type):
    def __getitem__(cls, key):
        class GenericReference(BaseModel):
            _sub_class: typing.Type = key
            implementation: str
            spec: dict = None

            @model_validator(mode='after')
            def _validate(self):
                self.build_reference_spec()
                return self

            def build_reference_spec(self):
                if issubclass(self._sub_class, Specable):
                    reference_class = self.get_reference_class()
                    bases = getattr(reference_class, '__orig_bases__', None)
                    if not bases:
                        raise ValueError(f"Unable to find {reference_class} config object")
                    # todo, add the right check here. Should grab the base which is a Specable, and then get the type
                    spec_type, = bases[0].__args__
                    return spec_type.model_validate(self.spec)
                else:
                    return self.spec

            def get_reference_class(self):
                return for_name(self.implementation, self._sub_class)

        return GenericReference


class Reference(metaclass=ReferenceMeta):
    pass

    def build_reference_spec(self):
        pass

    def get_reference_class(self) -> typing.Type:
        pass
