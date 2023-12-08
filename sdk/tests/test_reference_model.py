from contextlib import contextmanager

from pydantic import BaseModel

from eidos.agent_os import AgentOS
from eidos.system.reference_model import Reference, Specable
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
    simple: Reference(Base, kind='TestResource', default=fqn(System))


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
        model = SimpleModel(simple="DEFAULT")
        instantiated = model.simple.instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == 'os foo'


def test_explicit_named_reference_spec_overriden_in_reference():
    with os_resource(spec=dict(foo='bar')):
        model = SimpleModel(simple="DEFAULT")
        instantiated = model.simple.instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == 'bar'


def test_default_named_reference_default_spec():
    with os_resource():
        model = SimpleModel()
        instantiated = model.simple.instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == 'os foo'


def test_default_named_reference_spec_overriden_in_reference():
    with os_resource(spec=dict(foo='bar')):
        model = SimpleModel()
        instantiated = model.simple.instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == 'bar'


def test_default_named_reference_spec_overriden_in_simple_model():
    with os_resource():
        model = SimpleModel(simple=dict(spec=dict(foo='baz')))
        instantiated = model.simple.instantiate()
        assert type(instantiated) == OS
        assert instantiated.spec.foo == 'baz'


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
