from typing import TypeVar, Generic

import pytest
from pydantic import BaseModel, ValidationError

from eidolon_sdk.reference_model import Reference, Plugable


class TestSchema(BaseModel):
    foo: str


T = TypeVar('T', bound=BaseModel)


class BaseTestPlugable(Generic[T], Plugable[T]):
    pass


class TestConfigurable(BaseTestPlugable[TestSchema]):
    pass


class AlternativeTestConfigurable(Plugable[TestSchema]):
    pass


class CustomReferenceLogicUnitBase(Reference):
    _sub_class = BaseTestPlugable


def test_plugable_instantiation():
    plugable = Reference(implementation='tests.test_machine_definition.TestConfigurable', schema={'foo': 'bar'})
    assert plugable.instantiate().schema.foo == 'bar'


def test_reference_with_restricted_sub_class():
    plugable = CustomReferenceLogicUnitBase(implementation='tests.test_machine_definition.TestConfigurable', schema={'foo': 'bar'})
    assert plugable.instantiate().schema.foo == 'bar'


def test_enforces_sub_class():
    with pytest.raises(ValidationError) as e:
        Reference(implementation='tests.test_machine_definition.TestSchema', schema={'foo': 'bar'})
    assert e.value.errors()
