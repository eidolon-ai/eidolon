import json
from datetime import date, datetime, time
from typing import Dict, Any, Type, Literal
from typing import List
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl, EmailStr, Field, model_validator
from pydantic import create_model, ValidationError
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

type_mapping = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "null": type(None),
    "date": date,
    "time": time,
    "datetime": datetime,
    "uuid": UUID,
    "email": EmailStr,
    "uri": HttpUrl,
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
    fields = {}

    if not schema.get("type") == "object":
        raise ValueError("Schema must be an object with properties.")

    required = schema.get("required", [])
    for property_name, property_schema in schema.get("properties", {}).items():
        if "allOf" in property_schema and len(property_schema["allOf"]) == 1:
            property_schema.update(property_schema.pop("allOf")[0])

        def makeFieldOrDefaultValue():
            description = property_schema.get("description")
            kwargs = {}
            if "default" in property_schema:
                kwargs["default"] = property_schema["default"]
            if description:
                kwargs["description"] = description
            return Field(**kwargs)

        def wrap_optional(t: Type[Any], field: FieldInfo) -> (Type[BaseModel], FieldInfo):
            if property_name in required:
                return t, field
            else:
                if field.default == PydanticUndefined:
                    field.default = None
                return t, field

        try:
            field_type = property_schema.get("type")
            if field_type == "object":
                # Recursive call for nested object
                nested_model = schema_to_model(property_schema, f"{model_name}_{property_name.capitalize()}Model")
                fields[property_name] = wrap_optional(nested_model, makeFieldOrDefaultValue())
            elif field_type == "array":
                # Recursive call for arrays of objects
                items_schema = property_schema.get("items", {})
                if isinstance(items_schema, dict) and items_schema.get("type") == "object":
                    nested_item_model = schema_to_model(
                        items_schema,
                        f"{model_name}_{property_name.capitalize()}ItemModel",
                    )
                    fields[property_name] = wrap_optional(List[nested_item_model], makeFieldOrDefaultValue())
                else:
                    python_type = get_python_type(property_name, items_schema, str)
                    fields[property_name] = wrap_optional(List[python_type], makeFieldOrDefaultValue())
            else:
                fields[property_name] = wrap_optional(
                    get_python_type(property_name, property_schema), makeFieldOrDefaultValue()
                )
        except Exception as e:
            raise ValueError(f"Error creating field '{property_name}': {e}")

    try:
        return create_model(model_name, **fields, __base__=JsonProofModel)
    except ValidationError as e:
        raise ValueError(f"Error creating model '{model_name}': {e}")


class JsonProofModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


def get_python_type(property_name, property_schema, default=None):
    field_type = property_schema.get("type")
    if field_type == "string" and "format" in property_schema and property_schema["format"] == "binary":
        return UploadFile
    else:
        if field_type == "string" and "enum" in property_schema and property_schema["enum"]:
            # noinspection PyTypeHints
            literal_ = Literal[tuple(property_schema["enum"])]
            return literal_
        python_type = type_mapping.get(field_type, default)
        if python_type is None:
            raise ValueError(f"Unsupported type '{field_type}'")
        return python_type
