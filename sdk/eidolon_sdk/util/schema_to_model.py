from datetime import date, datetime, time
from typing import Dict, Any, Type
from typing import List
from uuid import UUID

from pydantic import BaseModel, HttpUrl, EmailStr, Field
from pydantic import create_model, ValidationError

type_mapping = {
    'string': str,
    'number': float,
    'integer': int,
    'boolean': bool,
    'null': type(None),
    'date': date,
    'time': time,
    'datetime': datetime,
    'uuid': UUID,
    'email': EmailStr,
    'uri': HttpUrl,
    # More complex types like 'format' can be handled by specific Pydantic types or custom validators
}


def schema_to_model(schema: Dict[str, Any], model_name: str) -> Type[BaseModel]:
    """
    Recursively converts a JSON Schema into a Pydantic model.

    The function interprets the JSON Schema definitions and constructs a corresponding
    Pydantic model with fields that match the schema's properties. It handles nested
    objects and arrays by creating nested Pydantic models as needed.

    Parameters:
        schema (Dict[str, Any]): A dictionary representing the JSON Schema from which
                                 the Pydantic model will be generated. The schema should
                                 follow the structure of JSON Schema, including `properties`,
                                 and `type` for each property.
        model_name (str): The name of the Pydantic model to be created. For nested models,
                          the function appends the property name, capitalized, to the
                          parent model name.

    Returns:
        Type[BaseModel]: A Pydantic BaseModel class constructed based on the provided
                         JSON Schema. Nested structures within the schema result in
                         nested Pydantic models.
   Raises:
        ValueError: If there is an error in creating the model from the schema.

    Example Usage:
        json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                    },
                    "required": ["street", "city"],
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
        }

        UserModel = schema_to_model(json_schema, 'UserModel')

    Notes:
        - The function does not handle JSON Schema `$ref` references or other advanced features
          such as `additionalProperties`, `allOf`, `anyOf`, etc.
    """
    required_fields = set(schema.get('required', []))
    fields = {}

    if (not schema.get('type') == 'object') or (not schema.get('properties')):
        raise ValueError("Schema must be an object with properties.")

    for property_name, property_schema in schema.get('properties', {}).items():
        def makeFieldOrDefaultValue():
            description = property_schema.get('description')
            default = ... if property_name in required_fields else None
            if description is None:
                return default
            else:
                return Field(default=default, description=description)

        try:
            field_type = property_schema.get('type')
            if field_type == 'object':
                # Recursive call for nested object
                nested_model = schema_to_model(property_schema, f'{model_name}_{property_name.capitalize()}Model')
                fields[property_name] = (nested_model, makeFieldOrDefaultValue())
            elif field_type == 'array':
                # Recursive call for arrays of objects
                items_schema = property_schema.get('items', {})
                if isinstance(items_schema, dict) and items_schema.get('type') == 'object':
                    nested_item_model = schema_to_model(items_schema, f'{model_name}_{property_name.capitalize()}ItemModel')
                    fields[property_name] = (List[nested_item_model], makeFieldOrDefaultValue())
                else:
                    item_type = items_schema.get('type', 'string')  # Default to string type
                    fields[property_name] = (List[item_type], makeFieldOrDefaultValue())
            else:
                # Simple field
                python_type = type_mapping.get(field_type, str)
                fields[property_name] = (python_type, makeFieldOrDefaultValue())
        except Exception as e:
            raise ValueError(f"Error creating field '{property_name}': {e}")

    try:
        return create_model(model_name, **fields, __base__=BaseModel)
    except ValidationError as e:
        raise ValueError(f"Error creating model '{model_name}': {e}")
