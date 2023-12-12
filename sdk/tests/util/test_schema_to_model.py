import pytest
from pydantic import BaseModel, ValidationError

from eidos.util.schema_to_model import schema_to_model


# Define a pytest class for grouping the tests
class TestSchemaToModel:

    def test_simple_model_creation(self):
        """Test creation of a simple model with primitive types."""
        json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name"]
        }
        SimpleModel = schema_to_model(json_schema, 'SimpleModel')
        assert issubclass(SimpleModel, BaseModel)
        model = SimpleModel(name='John Doe', age=30)
        assert model.name == 'John Doe'
        assert model.age == 30

    def test_nested_model_creation(self):
        """Test creation of a model with nested objects."""
        json_schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    },
                    "required": ["name"]
                }
            }
        }
        NestedModel = schema_to_model(json_schema, 'NestedModel')
        assert issubclass(NestedModel, BaseModel)
        nested_model = NestedModel(user={'name': 'Jane Doe', 'age': 25})
        assert nested_model.user.name == 'Jane Doe'
        assert nested_model.user.age == 25

    def test_array_model_creation(self):
        """Test creation of a model with array properties."""
        json_schema = {
            "type": "object",
            "properties": {
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
        ArrayModel = schema_to_model(json_schema, 'ArrayModel')
        assert issubclass(ArrayModel, BaseModel)
        array_model = ArrayModel(tags=['tag1', 'tag2'])
        assert array_model.tags == ['tag1', 'tag2']

    def test_required_fields(self):
        """Test that required fields are correctly identified and enforced."""
        json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name"]
        }
        RequiredFieldModel = schema_to_model(json_schema, 'RequiredFieldModel')
        with pytest.raises(ValidationError):
            RequiredFieldModel(age=30)  # 'name' is required

    def test_default_values(self):
        """Test that default values are correctly assigned."""
        json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Anonymous"},
                "age": {"type": "integer"}
            }
        }
        DefaultModel = schema_to_model(json_schema, 'DefaultModel')
        model = DefaultModel(age=30)
        assert model.name == 'Anonymous'
        assert model.age == 30

        model = DefaultModel()
        assert model.name == 'Anonymous'
        assert model.age is None

    def test_required_values(self):
        """Test that default values are correctly assigned."""
        json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Anonymous"},
                "age": {"type": "integer"}
            },
            "required": ["age"]
        }
        DefaultModel = schema_to_model(json_schema, 'DefaultModel')
        with pytest.raises(ValueError) as exc_info:
            DefaultModel()
        assert ('1 validation error for DefaultModel\n'
                'age\n'
                '  Field required [type=missing, input_value={}, input_type=dict]\n'
                '    For further information visit https://errors.pydantic.dev/2.5/v/missing') in str(exc_info.value)

    def test_invalid_schema(self):
        """Test that an invalid schema raises the appropriate error."""
        json_schema = {
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        with pytest.raises(ValueError) as exc_info:
            schema_to_model(json_schema, 'InvalidModel')
        assert "Schema must be an object with properties." in str(exc_info.value)

    def test_unsupported_type(self):
        """Test that an unsupported type raises the appropriate error."""
        json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "unsupported"}
            }
        }
        with pytest.raises(ValueError) as exc_info:
            schema_to_model(json_schema, 'UnsupportedModel')
        assert "Error creating field 'name'" in str(exc_info.value)

# Run the tests with pytest from the command line
# pytest test_schema_to_model.py
