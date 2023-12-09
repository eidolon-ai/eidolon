from __future__ import annotations

import logging
import typing

from pydantic import BaseModel, model_validator, Field

from eidos.agent_os import AgentOS
from eidos.util.class_utils import for_name, fqn
from eidos.util.logger import logger

T = typing.TypeVar('T', bound=BaseModel)


class Specable(typing.Generic[T]):
    """
    A generic type which can be used to describe a specable type. Specable types are expected to accept "spec" in kwarg.
    If Specable is not used, There will be no spec validation and the spec will be passed through as-is.
    """
    spec: T

    def __init__(self, spec: T, **kwargs: object):
        self.spec = spec


class ReferenceMeta(type):
    def __getitem__(self, item) -> typing.Type[_GenericReference]:
        return self(item)

    def __call__(cls, bound: typing.Type = None, default: str | typing.Type = None, kind: str = None, **kwargs) -> typing.Type[_GenericReference]:
        default = default if default is None or isinstance(default, str) else fqn(default)

        class _SpecificReference(_GenericReference):
            _bound = bound

            @model_validator(mode='before')
            def _transform(self):
                if isinstance(self, str):
                    if "." in self:
                        bucket, name = self.split(".")
                    else:
                        bucket, name = kind, self
                    found = AgentOS.get_resource(bucket, name).model_dump(exclude={'apiVersion', 'kind', 'metadata'})
                    return found
                elif isinstance(self, dict):
                    os_default = AgentOS.get_resource(kind, default=None)

                    if self.get('implementation'):  # First priority is explicit impl
                        return self
                    elif os_default:
                        self.pop('implementation', None)  # then default resource set at OS level
                        dump = os_default.model_dump(exclude={'apiVersion', 'kind', 'metadata'})
                        dump.update(self)  # likely just spec is overwritten, but we should let everything flow through
                        return dump
                    elif default:  # then system default
                        self['implementation'] = default
                        return self
                    elif bound:  # finally fallback to bound class
                        logger.warning(f"Unable to find resource for {self}, falling back to bounding class")
                        self['implementation'] = fqn(bound)
                        return self
                    else:
                        raise ValueError(f"Unable to find class to reference")

                else:
                    raise ValueError(f"Unable to transform {self} to a reference")

        return typing.Annotated[_SpecificReference, Field(default_factory=_SpecificReference, validate_default=True, **kwargs)]


class Reference(metaclass=ReferenceMeta):
    """
    A wrapper to provide a generic reference to a class. Returns an annotated BaseModel which contains two fields
    (implementation and optional spec) and an instantiate method.

    References can be used as fields in a BaseModel to automatically wire up another portion of the system and
    describe it within a spec. For example:

    class AgentSpec(BaseModel):
        foo: Reference(MyFoo, default=SubFoo, kind='Foo')
        bar: Reference(MyBar, default=SubBar, kind='Bar')
        baz: Reference(MyBaz, default=SubBaz)
        qux: Reference(MyQux, default=SubQux)
        corge: Reference(MyCorge)

    apiVersion: eidolon/v1
    kind: Agent
    metadata:
        name: MySpecableClass
    spec:
        foo:                                # overrides all defaults
            implementation: fqn.SubSubFoo
            spec: {...}
        bar: named_bar_resource             # finds named resource on AgentOS
        baz: Baz.named_bar_resource         # finds named resource on AgentOS, but requires kind prefix
                                            # qux reverts to default SubQux
                                            # corge reverts to default MyCorge

    Note:   That the default is a class (or the fqn of a class) and not an instance of the class.
    Note:   "spec" can be provided independently to override spec for whatever default is being used. Similarly, if
            "spec" is not provided, the default spec will be used for the chosen implementation.
    Note:   "kind" is not required, but allows for the default to be set at the OS level (used before code default if
            defined) and a default bucket when referencing other resources.
    Note:   This class and the implementation below are just syntactic sugar.
            See _SpecificReference in the metaclass for the actual implementation.
    Note:   Caution should be used when extending Reference. If the extended object is used as a field in a BaseModel,
            it will not automatically receive the annotated default_factory.
    """
    implementation: str = None
    spec: dict = None

    def instantiate(self, *args, **kwargs):
        ...


class _GenericReference(BaseModel):
    _bound: typing.Type
    implementation: str
    spec: dict = None

    @model_validator(mode='after')
    def _validate(self):
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
        return for_name(self.implementation, self._bound or object)


V = typing.TypeVar('V')


class WithDefault(typing.Generic[V]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return v
