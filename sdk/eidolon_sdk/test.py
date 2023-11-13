from fastapi import FastAPI
from typing import Dict, Any

from eidolon_sdk.util.schema_to_model import schema_to_model
from eidolon_sdk.util.dynamic_endpoint import add_dynamic_route

app = FastAPI()

# Function to create a dynamic endpoint

# Function to add the dynamic endpoint to the app


simple_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "The name of the person."},
        "age": {"type": "integer"}
    },
    "required": ["name"]
}

response_schema = {
    "type": "object",
    "properties": {
        "answer": {"type": "string", "description": "The name of the person."},
    },
    "required": ["answer"]
}


def response(input: Dict[str, Any]):
    print(input)
    return {'answer': '42'}


# Add a dynamic route to the app
add_dynamic_route(app, '/example', schema_to_model(simple_schema, 'SimpleModel'), schema_to_model(response_schema, 'ResponseModel'), response)

# Now the FastAPI app has a dynamically added endpoint that accepts a request body
# matching the DynamicExampleModel, and the documentation will correctly show the
# model with its fields.

