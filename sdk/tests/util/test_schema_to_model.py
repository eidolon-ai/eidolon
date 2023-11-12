import pytest
from pydantic import BaseModel, ValidationError
from eidolon_sdk.util.schema_to_model import schema_to_model


class TestSchemaToModel:
    def test_simple_schema(self):
        simple_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name"]
        }
        SimpleModel = schema_to_model(simple_schema, 'SimpleModel')
        assert issubclass(SimpleModel, BaseModel)

        instance = SimpleModel(name='John')
        assert hasattr(instance, 'name')
        assert hasattr(instance, 'age')
        assert instance.name == 'John'
        with pytest.raises(ValidationError):
            SimpleModel()

    def test_nested_schema(self):
        nested_schema = {
            "type": "object",
            "properties": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    },
                    "required": ["name"]
                }
            }
        }
        NestedModel = schema_to_model(nested_schema, 'NestedModel')
        assert issubclass(NestedModel, BaseModel)

        instance = NestedModel(person={'name': 'John'})
        assert hasattr(instance, 'person')
        assert instance.person.name == 'John'

    def test_optional_fields(self):
        optional_field_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        OptionalFieldModel = schema_to_model(optional_field_schema, 'OptionalFieldModel')
        assert issubclass(OptionalFieldModel, BaseModel)

        instance = OptionalFieldModel(name='John')
        assert hasattr(instance, 'name')
        assert hasattr(instance, 'age')
        assert instance.name == 'John'
        assert instance.age is None

    def test_incorrect_schema(self):
        incorrect_schema = {"foo": "not a valid schema"}
        with pytest.raises(ValueError):
            schema_to_model(incorrect_schema, 'IncorrectModel')
