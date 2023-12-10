from contextlib import contextmanager

from pydantic import BaseModel, Field

from eidos.agent_os import AgentOS
from eidos.system.reference_model import Reference, Specable, AnnotatedReference
from eidos.system.resources_base import Resource
from eidos.util.class_utils import fqn


class BaseSpec(BaseModel):
    foo: str = "simple foo"


class OSSpec(BaseSpec):
    foo: str = "os foo"


class SystemSpec(BaseSpec):
    foo: str = "system foo"


class RandomSpec(BaseSpec):
    foo: str = "random foo"


class Base(Specable[BaseSpec]):
    ...


class OS(Base, Specable[OSSpec]):
    ...


class System(Base, Specable[SystemSpec]):
    ...


class Random(Base, Specable[RandomSpec]):
    ...


class SimpleModel(BaseModel):
    simple: AnnotatedReference[Base, System]


@contextmanager
def os_resource(**kwargs):
    try:
        AgentOS.register_resource(Resource(
            apiVersion='eidolon/v1',
            kind='TestResource',
            implementation=fqn(OS),
            **kwargs
        ))
        yield
    finally:
        AgentOS._resources = {}


def test_explicit_reference_default_spec():
    model = SimpleModel(simple=dict(implementation=fqn(Random)))
    instantiated = model.simple.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == 'random foo'


def test_explicit_reference_override_spec():
    model = SimpleModel(simple=dict(implementation=fqn(Random), spec=dict(foo='bar')))
    instantiated = model.simple.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == 'bar'


def test_explicit_named_reference_default_spec():
    with os_resource():
        model = SimpleModel(simple='TestResource')
        instantiated = model.simple.instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == 'os foo'


def test_explicit_named_reference_spec_overriden_in_reference():
    with os_resource(spec=dict(foo='bar')):
        model = SimpleModel(simple='TestResource')
        instantiated = model.simple.instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == 'bar'


def test_system_fallback_default_spec():
    model = SimpleModel()
    instantiated = model.simple.instantiate()
    assert type(instantiated) == System
    assert instantiated.spec.foo == 'system foo'


def test_system_fallback_default_override_spec():
    model = SimpleModel(simple=dict(spec=dict(foo='baz')))
    instantiated = model.simple.instantiate()
    assert type(instantiated) == System
    assert instantiated.spec.foo == 'baz'


class ExtendedModel(Reference[object, Random]):
    ...


class Wrapper(BaseModel):
    extended: ExtendedModel = ExtendedModel()


def test_extending_reference_wrapped():
    instantiated = Wrapper().extended.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == 'random foo'


def test_extended_reference_wrapped_with_overrides():
    instantiated = Wrapper(extended=dict(spec=dict(foo='bar'))).extended.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == 'bar'


def test_extended_reference_raw():
    instantiated = ExtendedModel().instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == 'random foo'


def test_reference_with_no_default():
    random_ = Reference[Random]
    instantiated = random_().instantiate()
    instantiated.spec.foo = 'random_foo'


def test_annotated_ref_plays_nicely_with_descriptions():
    class Fielded(BaseModel):
        simple: AnnotatedReference[System] = Field(description="A simple reference")

    Fielded().simple.instantiate().spec.foo = 'system foo'


# generics create a too strict type bound when validating with actual class instances, which is unfortunate
# we can probably work around this by removing generics ans having a custom getitem method to inject the types to a non-pydantic field
def test_loosly_validated_type_bounds():
    class Fielded(BaseModel):
        simple: Reference[Base] = Field(description="A simple reference")

    fielded = Fielded.model_validate(dict(simple=Reference[System]().model_dump()))
    # fielded = Fielded(simple=Reference[System]())
    assert fielded.simple.instantiate().spec.foo == 'system foo'
