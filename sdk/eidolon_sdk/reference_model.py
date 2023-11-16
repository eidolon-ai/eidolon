from __future__ import annotations

import logging
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

            # todo, fix bug here where checking wrong class. is subclass should be on reference_class
            def build_reference_spec(self):
                reference_class = self._get_reference_class()
                if issubclass(reference_class, Specable):
                    bases = getattr(reference_class, '__orig_bases__', [])
                    specable = next((base for base in bases if getattr(base, '__origin__', None) is Specable), None)
                    if specable:
                        spec_type, = specable.__args__
                        return spec_type.model_validate(self.spec)
                    else:
                        logging.warning(f'Unable to find Specable definition on "{reference_class}", skipping validation')
                        return self.spec
                else:
                    return self.spec

            def instantiate(self, *args, **kwargs):
                spec = self.build_reference_spec()
                if spec is not None:
                    kwargs['spec'] = spec
                return self._get_reference_class()(*args, **kwargs)

            def _get_reference_class(self):
                return for_name(self.implementation, self._sub_class)

        return GenericReference


class Reference(metaclass=ReferenceMeta):
    pass

    def build_reference_spec(self):
        pass

    def instantiate(self, *args, **kwargs):
        pass
