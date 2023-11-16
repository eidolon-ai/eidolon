from typing import TypeVar, Generic

import pytest
from pydantic import BaseModel, ValidationError

from eidolon_sdk.reference_model import Reference, Specable


class TestSchema(BaseModel):
    foo: str


class Base:
    kwargs: dict
    ref = 'tests.test_reference_model.Base'

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class Extension(Base, Specable[TestSchema]):
    ref = 'tests.test_reference_model.Extension'


class ReversedExtension(Base, Specable[TestSchema]):
    ref = 'tests.test_reference_model.ReversedExtension'


def test_plugable_instantiation():
    ref = Reference[Base](implementation=Base.ref, spec={'foo': 'bar'})
    assert ref.build_reference_spec() == {'foo': 'bar'}
    assert ref.instantiate(baz="BAZ").kwargs == dict(baz='BAZ', spec={'foo': 'bar'})


def test_specable_reference():
    ref = Reference[Base](implementation=Extension.ref, spec={'foo': 'bar'})
    assert ref.build_reference_spec() == TestSchema(foo='bar')
    assert ref.instantiate().kwargs == dict(spec=TestSchema(foo='bar'))


def test_spec_backwards_ref():
    ref = Reference[Base](implementation=ReversedExtension.ref, spec={'foo': 'bar'})
    assert ref.build_reference_spec() == TestSchema(foo='bar')
    assert ref.instantiate().kwargs == dict(spec=TestSchema(foo='bar'))


def test_enforces_sub_class():
    with pytest.raises(ValidationError) as e:
        Reference[Extension](implementation=ReversedExtension.ref, spec={'foo': 'bar'})
    assert e.value.errors()
