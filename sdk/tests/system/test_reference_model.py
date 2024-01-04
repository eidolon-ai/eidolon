from contextlib import contextmanager

import pytest
from pydantic import BaseModel, Field

from eidos_sdk.agent_os import AgentOS
from eidos_sdk.system.reference_model import Reference, Specable, AnnotatedReference
from eidos_sdk.system.resources.eidos_ref_resource import EidosRef
from eidos_sdk.system.resources.resources_base import Metadata
from eidos_sdk.util.class_utils import fqn


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
def resource(name="TestResource", implementation=fqn(OS), spec=None):
    spec = spec or {}
    try:
        AgentOS.register_resource(
            EidosRef(
                apiVersion="eidolon/v1",
                metadata=Metadata(name=name),
                spec=dict(implementation=implementation, **spec),
            )
        )
        yield
    finally:
        AgentOS._resources = {}


def test_explicit_reference_default_spec():
    model = SimpleModel(simple=dict(implementation=fqn(Random)))
    instantiated = model.simple.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == "random foo"


def test_explicit_reference_override_spec():
    model = SimpleModel(simple=dict(implementation=fqn(Random), foo="bar"))
    instantiated = model.simple.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == "bar"


def test_explicit_named_reference_default_spec():
    with resource():
        model = SimpleModel(simple="TestResource")
        instantiated = model.simple.instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == "os foo"


def test_explicit_named_reference_spec_overriden_in_reference():
    with resource(spec=dict(foo="bar")):
        model = SimpleModel(simple="TestResource")
        instantiated = model.simple.instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == "bar"


@pytest.fixture
def nested_random_resource():
    with resource(name="outer", implementation="middle"):
        with resource(name="middle", implementation="inner", spec=dict(foo="bar")):
            with resource(name="inner", implementation=fqn(Random)):
                yield


def test_nested_resources(nested_random_resource):
    model = SimpleModel(simple="outer")
    instantiated = model.simple.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == "bar"  # bar comes from override on middle resource


def test_nested_resources_with_override(nested_random_resource):
    model = SimpleModel(simple=dict(implementation="outer", foo="baz"))
    instantiated = model.simple.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == "baz"


def test_system_fallback_default_spec():
    model = SimpleModel()
    instantiated = model.simple.instantiate()
    assert type(instantiated) == System
    assert instantiated.spec.foo == "system foo"


def test_system_fallback_default_override_spec():
    model = SimpleModel(simple=dict(foo="baz"))
    instantiated = model.simple.instantiate()
    assert type(instantiated) == System
    assert instantiated.spec.foo == "baz"


class ExtendedModel(Reference[object, Random]):
    ...


class Wrapper(BaseModel):
    extended: ExtendedModel = ExtendedModel()


def test_extending_reference_wrapped():
    instantiated = Wrapper().extended.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == "random foo"


def test_extended_reference_wrapped_with_overrides():
    instantiated = Wrapper(extended=dict(foo="bar")).extended.instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == "bar"


def test_extended_reference_raw():
    instantiated = ExtendedModel().instantiate()
    assert type(instantiated) == Random
    assert instantiated.spec.foo == "random foo"


def test_reference_with_no_default():
    random_ = Reference[Random]
    instantiated = random_().instantiate()
    instantiated.spec.foo = "random_foo"


def test_reference_with_default():
    random_ = Reference[Base, Random]
    instantiated = random_().instantiate()
    instantiated.spec.foo = "random_foo"


def test_reference_with_string_default():
    with resource():
        test_resource = Reference[Base, "TestResource"]
        instantiated = test_resource().instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == "os foo"


def test_annotated_ref_plays_nicely_with_descriptions():
    class Fielded(BaseModel):
        simple: AnnotatedReference[System] = Field(description="A simple reference")

    Fielded().simple.instantiate().spec.foo = "system foo"


def test_loosely_validated_type_bounds_dumping_dict():
    class Fielded(BaseModel):
        simple: Reference[Base] = Field(description="A simple reference")

    dumped = dict(simple=Reference[System]().model_dump())
    fielded = Fielded.model_validate(dumped)
    assert fielded.simple.instantiate().spec.foo == "system foo"


def test_loosely_validated_type_bounds():
    class Fielded(BaseModel):
        simple: Reference[Base] = Field(description="A simple reference")

    reference = Reference(implementation=fqn(System))
    fielded = Fielded(simple=reference)
    assert fielded.simple.instantiate().spec.foo == "system foo"
