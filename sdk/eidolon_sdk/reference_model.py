from __future__ import annotations

import logging
import typing

from pydantic import BaseModel, model_validator, Field

from eidolon_sdk.util.class_utils import for_name, fqn

T = typing.TypeVar('T', bound=BaseModel)


class Specable(typing.Generic[T]):
    """
    A generic type which can be used to describe a specable type. Specable types are expected to accept "spec" in kwarg.
    If Specable is not used, There will be no spec validation and the spec will be passed through as-is.
    """
    spec: T

    def __init__(self, spec: T, **kwargs):
        self.spec = spec


class ReferenceMeta(type):
    def __call__(cls, **kwargs):
        return cls[object](**kwargs)

    def __getitem__(cls, key):
        class GenericReference(BaseModel):
            _sub_class: typing.Type = key
            implementation: str = Field(default=None, description="The implementation of the reference")
            spec: dict = None

            @model_validator(mode='after')
            def _validate(self):
                if self.implementation is None:
                    self.implementation = fqn(self._sub_class)
                self.build_reference_spec()
                return self

            def build_reference_spec(self):
                reference_class = self._get_reference_class()
                if issubclass(reference_class, Specable):
                    bases = getattr(reference_class, '__orig_bases__', [])
                    specable = next((base for base in bases if getattr(base, '__origin__', None) is Specable), None)
                    if specable:
                        spec_type, = specable.__args__
                        return spec_type.model_validate(self.spec or {})
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
    """
    A wrapper to provide a generic reference to a class. Can be used like a Generic type to validate sub-class constraints

    Reference[Foo](implementation="module.CLASS") will validate that the implementation is a subclass of Foo.
    Reference(implementation="module.CLASS") is equivalent to Reference[object](implementation="module.CLASS").

    Can be used in conjunction with Specable to validate the spec provided to the reference.

    References are expected to accept a spec kwarg in __init__

    Note:   This class and the implementation below are just syntactic sugar.
            See GenericReference in the metaclass for the actual implementation.
    """
    implementation: str
    spec: dict = None

    def build_reference_spec(self):
        pass

    def instantiate(self, *args, **kwargs):
        pass
