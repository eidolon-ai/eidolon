from __future__ import annotations

import copy
import logging
import textwrap
from functools import cache
from typing import TypeVar, Type, Annotated, Optional, ClassVar

from pydantic import BaseModel, model_validator, Field, ConfigDict, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema as cs, PydanticCustomError

from eidolon_ai_sdk.system.resources.reference_resource import ReferenceResource
from eidolon_ai_sdk.system.specable import Specable
from eidolon_ai_sdk.util.class_utils import fqn, get_from_fqn, InvalidFQN
from eidolon_ai_sdk.util.schema_to_model import schema_to_model

B = TypeVar("B")
D = TypeVar("D")


class Reference(BaseModel):
    """
    Used to create references to other classes. It is designed to be used with two type variables, `B` and `D` which are
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
    _membership: ClassVar[Type[D] | str] = object
    implementation: str = None

    model_config = ConfigDict(
        extra="allow",
    )

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        if cls._bound == object:
            json_schema = handler(core_schema)
            json_schema = handler.resolve_ref_schema(json_schema)
            json_schema["properties"] = dict(implementation=dict(type="string", title="Implementation"))
            if "Used to create references to other classes." in json_schema.get('description', ""):  # delete description if it is not overridden
                del json_schema['description']
            return json_schema

        from eidolon_ai_sdk.system.kernel import AgentOSKernel

        title = (cls._bound if isinstance(cls._bound, str) else cls._bound.__name__)

        core_schema['ref'] = f"Reference[{title}]"
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema["title"] = title
        if not isinstance(cls._bound, str) and cls._bound.__doc__:
            json_schema['description'] = textwrap.dedent(cls._bound.__doc__).strip()
        json_schema["reference_pointer"] = {
            "type": cls._bound if isinstance(cls._bound, str) else cls._bound.__name__,
            "default_impl": cls._default,
        }

        del json_schema['type']
        del json_schema['properties']
        del json_schema["additionalProperties"]

        json_schema["anyOf"] = []
        group_component_ref = None
        for r in AgentOSKernel.get_resources(ReferenceResource).values():
            # there is not a class for these psudo references, we can either make those classes dynamically, or create a custom ?generator? to handle them
            overrides = Reference[object, r.metadata.name]._transform(r.spec)
            pointer = overrides.pop("implementation")
            clz = get_from_fqn(pointer)
            if hasattr(clz, "specable"):
                clz = clz.specable()
            if issubclass(clz, cls._membership):
                reference_details = dict(
                    overrides=overrides,
                    clz=pointer,
                    name=r.metadata.name,
                    group=json_schema["reference_pointer"]['type'],
                )
                ref = handler(_pseudo_pointer(r.metadata.name).__pydantic_core_schema__)
                if r.metadata.name == json_schema["reference_pointer"]['type']:
                    group_component_ref = ref
                ref_schema = handler.resolve_ref_schema(ref)
                if 'reference_details' not in ref_schema:
                    ref_schema['reference_details'] = reference_details
                    if hasattr(clz, "__pydantic_core_schema__"):
                        obj_ref = clz.__get_pydantic_json_schema__(clz.__pydantic_core_schema__, handler)
                    else:
                        obj_ref = dict(
                            type="object",
                            properties=dict(implementation=dict(type="string")),
                            additionalProperties=True,
                        )
                    desired_ref_schema = handler.resolve_ref_schema(obj_ref)
                    desired_ref_schema['properties']['implementation'] = dict(const=r.metadata.name, title="Implementation")
                    desired_ref_schema['properties'] = dict(  # put implementation at the top
                        implementation=desired_ref_schema['properties'].pop('implementation'),
                        **desired_ref_schema['properties']
                    )
                    desired_ref_schema.pop("$defs", None)
                    desired_ref_schema.setdefault("required", []).append("implementation")
                    ref_schema.update(desired_ref_schema)
                    ref_schema['title'] = r.metadata.name
                    for key, value in overrides.items():
                        ref_schema['properties'].setdefault(key, {})['default'] = value
                json_schema["anyOf"].append(ref)

        json_schema["anyOf"] = sorted(json_schema["anyOf"], key=lambda x: x['$ref'])
        if len(json_schema["anyOf"]) > 1:
            json_schema["anyOf"] = [js for js in json_schema["anyOf"] if js != group_component_ref]
            json_schema["anyOf"] = json_schema["anyOf"][1:] + json_schema["anyOf"][:1]

        return json_schema

    def __class_getitem__(cls, params):
        if not isinstance(params, tuple):
            params = (params, fqn(params), params)
        elif len(params) == 2:
            params = (params[0], params[1], params[0])

        class _Reference(cls):
            _bound = params[0]
            _default = params[1]
            _membership = params[2]

            @classmethod
            def _transformed_impl(cls):
                impl = cls._transform({})["implementation"]
                if "." in impl:
                    impl = impl.split(".")[-1]
                return impl

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
                d2v = d2.setdefault(k, {})
                if isinstance(d2v, str):
                    d2v = dict(implementation=d2v)
                    d2[k] = d2v
                cls._merge(v, d2v)
            else:
                d2[k] = v

    @classmethod
    def _expand(cls, impl, extra):
        from eidolon_ai_sdk.system.kernel import AgentOSKernel

        ref = AgentOSKernel.get_resource(ReferenceResource, impl, default=None)
        if not ref:
            return impl, extra
        else:
            inner_spec = copy.deepcopy(ref.spec)
            impl = inner_spec.pop("implementation")
            cls._merge(extra or {}, inner_spec)
            return cls._expand(impl, inner_spec)

    @model_validator(mode="after")
    def _validate(self):
        try:
            reference_class = self._get_reference_class()
        except InvalidFQN as e:
            raise PydanticCustomError("reference_error", "{e}", dict(e=f"'{e.fqn}' is not a valid reference or fully qualified name"))
        except Exception as e:
            raise PydanticCustomError("reference_error", "{e}", dict(e=e))
        spec = Reference.get_spec_type(reference_class)
        if spec:
            spec.model_validate(self.model_extra or {})
        return self

    @staticmethod
    def get_spec_type(reference_class):
        specable = Reference.get_specable_type(reference_class)
        return specable if specable else reference_class if issubclass(reference_class, BaseModel) else None

    @staticmethod
    def get_specable_type(reference_class) -> Optional[Type[BaseModel]]:
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
        found = get_from_fqn(self.implementation)
        if hasattr(found, "specable"):
            found = found.specable()
        if not found:
            raise ValueError(f'Unable to find reference implementation "{self.implementation}"')
        if self._bound and (not isinstance(found, type) or not issubclass(found, self._bound)):
            raise ValueError(f'Implementation "{self.implementation}" is not a subclass of "{self._bound}"')
        return found

    def instantiate(self, *args, **kwargs):
        reference_class = self._get_reference_class()
        spec_type = self.get_specable_type(reference_class)
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


@cache
def _pseudo_pointer(name) -> Type[BaseModel]:
    return schema_to_model(dict(type="object", properties={}), name)
