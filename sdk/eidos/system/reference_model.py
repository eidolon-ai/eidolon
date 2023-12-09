from __future__ import annotations

import logging
from typing import TypeVar, Generic, Type, get_args, Annotated

from pydantic import BaseModel, model_validator, Field

from eidos.agent_os import AgentOS
from eidos.util.class_utils import for_name, fqn

T = TypeVar('T', bound=BaseModel)


class Specable(Generic[T]):
    """
    A generic type which can be used to describe a specable type. Specable types are expected to accept "spec" in kwarg.
    If Specable is not used, There will be no spec validation and the spec will be passed through as-is.
    """
    spec: T

    def __init__(self, spec: T, **kwargs: object):
        self.spec = spec


B = TypeVar('B')
D = TypeVar('D')


class Reference(BaseModel, Generic[B, D]):
    bound: Type[B] = None
    default: Type[D] = None
    implementation: str = None
    spec: dict = None

    def __class_getitem__(cls, params):
        if not isinstance(params, tuple):
            params = (params, D)
        return super().__class_getitem__(params)

    @model_validator(mode='before')
    def _transform(self):
        if isinstance(self, str):
            split = list(self.split("."))
            bucket = split.pop(0)
            name = ".".join(split) if split else "DEFAULT"
            found = AgentOS.get_resource(bucket, name)
            return found.model_dump(exclude={'apiVersion', 'kind', 'metadata'})
        else:
            return self

    @model_validator(mode='after')
    def _validate(self):
        if not self.bound:
            generic_bound = get_args(self.__class__.model_fields['bound'].annotation)[0]
            self.bound = object if isinstance(generic_bound, TypeVar) else generic_bound
        if not self.default:
            generic_default = get_args(self.__class__.model_fields['default'].annotation)[0]
            self.default = None if isinstance(generic_default, TypeVar) else generic_default

        if not self.implementation and self.default:
            self.implementation = fqn(self.default)
        if not self.implementation and self.bound != object:
            self.implementation = fqn(self.bound)
        if not self.implementation:
            raise ValueError(f'Unable to determine implementation for "{self}"')

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
        return for_name(self.implementation, self.bound or object)


class AnnotatedReference(Reference):
    def __class_getitem__(cls, params) -> Type[Reference]:
        return Annotated[Reference[params], Field(default=Reference[params]())]
