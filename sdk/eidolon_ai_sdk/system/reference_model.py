from __future__ import annotations

import copy
import logging
from typing import TypeVar, Generic, Type, Annotated, Optional, ClassVar

from pydantic import BaseModel, model_validator, Field, ConfigDict

from eidolon_ai_sdk.agent_os import AgentOS
from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.util.class_utils import for_name, fqn

T = TypeVar("T", bound=BaseModel)


class Specable(Generic[T]):
    """
    A generic type which can be used to describe a specable type. Specable types are expected to accept "spec" in kwarg.
    If Specable is not used, There will be no spec validation and the spec will be passed through as-is.
    """

    spec: T

    def __init__(self, spec: T, **kwargs: object):
        self.spec = spec


B = TypeVar("B")
D = TypeVar("D")


class Reference(BaseModel):
    """
    Used to create references to other classes. t is designed to be used with two type variables, `B` and `D` which are
    the type bound and default type respectively. Neither are required, and if only one type is provided it is assumed
    to be the bound. Bound is used as the default if no default is provided. default can also be a string which will be
    looked up from the OS ReferenceResources.

    Examples:
        Reference(implementation=fqn(Foo)                           # Returns an instance of Foo
        Reference[FooBase](implementation=fqn(Foo)).instantiate()   # Returns an instance of Foo
        Reference[FooBase](implementation=fqn(Bar))                 # Raises ValueError
        Reference[FooBase, Foo]().instantiate()                     # Returns an instance of Foo
        Reference[FooBase]().instantiate()                          # Returns an instance of FooBase

    Attributes:
        _bound: This is a type variable `B` that represents the bound type of the reference. It defaults to `object`.
        _default: This is a type variable `D` that represents the default type of the reference. It defaults to `None`.
        implementation: This is a string that represents the fully qualified name of the class that the reference points to. It is optional and can be set to `None`.
        **extra: This is a dictionary that can hold any additional specifications for the reference. It is optional and can be set to `None`.

    Methods:
        instantiate: This method is used to create an instance of the class that the reference points to.
    """

    _bound: ClassVar[Type[B]] = object
    _default: ClassVar[Type[D] | str] = None
    implementation: str = None

    model_config = ConfigDict(
        extra="allow",
    )

    def __class_getitem__(cls, params):
        if not isinstance(params, tuple):
            params = (params, fqn(params))

        class _Reference(cls):
            _bound = params[0]
            _default = params[1]

            @model_validator(mode="before")
            def _dump_ref(cls, value):
                return value.model_dump(exclude_defaults=True) if isinstance(value, Reference) else value

            def __reduce__(self):
                return (
                    _ReferenceGetter(),
                    (self._bound, self._default, self.model_dump(exclude_defaults=True)),
                    self.__getstate__(),
                )

        return _Reference

    @model_validator(mode="before")
    def _transform(cls, value):
        if isinstance(value, str):
            impl = value
            spec = {}
        else:
            spec = value.model_dump(exclude_defaults=True) if isinstance(value, BaseModel) else copy.deepcopy(value)
            impl = spec.pop("implementation", fqn(cls._default) if isinstance(cls._default, type) else cls._default)
            if not impl:
                raise ValueError(f'Unable to determine implementation for "{value}"')

        impl, spec = cls._expand(impl, spec)
        return dict(implementation=impl, **spec)

    @classmethod
    def _merge(cls, d1, d2):
        for k, v in d1.items():
            if isinstance(v, dict):
                d2[k] = d2.get(k, {})
                cls._merge(v, d2.get(k, {}))
            else:
                d2[k] = v

    @classmethod
    def _expand(cls, impl, extra):
        ref = AgentOS.get_resource(ReferenceResource, impl, default=None)
        if not ref:
            return impl, extra
        else:
            inner_spec = copy.deepcopy(ref.spec)
            impl = inner_spec.pop("implementation")
            cls._merge(extra or {}, inner_spec)
            return cls._expand(impl, inner_spec)

    @model_validator(mode="after")
    def _validate(self):
        reference_class = self._get_reference_class()
        spec_type = self.get_spec_type(reference_class)
        if spec_type:
            spec_type.model_validate(self.model_extra or {})
        elif issubclass(reference_class, BaseModel):
            reference_class.model_validate(self.model_extra or {})
        return self

    @staticmethod
    def get_spec_type(reference_class) -> Optional[Type[BaseModel]]:
        if issubclass(reference_class, Specable):
            bases = getattr(reference_class, "__orig_bases__", [])
            specable = next(
                (base for base in bases if getattr(base, "__origin__", None) is Specable),
                None,
            )
            if specable:
                return specable.__args__[0]
            else:
                logging.warning(f'Unable to find Specable definition on "{reference_class}", skipping validation')
                return None
        return None

    def _get_reference_class(self):
        return for_name(self.implementation, self._bound or object)

    def instantiate(self, *args, **kwargs):
        reference_class = self._get_reference_class()
        spec_type = self.get_spec_type(reference_class)
        if spec_type:
            kwargs["spec"] = spec_type.model_validate(self.model_extra or {})
        else:
            for k, v in (self.model_extra or {}).items():
                kwargs[k] = v

        return self._get_reference_class()(*args, **kwargs)


class AnnotatedReference(Reference):
    """
    Helper class to manage References with defaults.

    Default is set to the class name, which should be as a builtin pointing to the FQN of the class

    Example:
        class MySpec(BaseModel):
            ref1: AnnotatedReference[MyBound] = Field(description="My description")

    Note:
        The description can still be added via a Field annotation without affecting default behavior
    """

    def __class_getitem__(cls, params) -> Type[Reference]:
        if not isinstance(params, tuple):
            params = (params, params.__name__)
        return Annotated[Reference[params], Field(default_factory=Reference[params])]


class _ReferenceGetter(object):
    def __call__(self, p1, p2, dump):
        return Reference[(p1, p2)].model_validate(dump)
