import json

import pytest

from eidolon_ai_sdk.builtins.logic_units.openapi_helper import build_actions, Operation


@pytest.fixture(scope="module")
def pet_store(test_dir):
    docs_loc = test_dir / "builtins" / "logic_units" / "openapi_helper_files"
    # load the petstore.json file from docs_loc and return json object
    with open(docs_loc / "petstore.json") as f:
        data = json.load(f)
    return data


async def test_query_params(pet_store):
    tool_called = False

    def do_call(path_to_call, method, query_params, headers, body):
        nonlocal tool_called
        tool_called = True
        assert path_to_call == "/pets"
        assert method == "get"
        assert len(query_params) == 4
        for param in query_params:
            if param[0] == "limit":
                assert param[1] == '10'
            elif param[0] == "tags":
                assert param[1] == "tag1,tag2"
            elif param[0] == "categories":
                assert param[1] == 'cat1' or param[1] == 'cat2'
        assert headers == {}
        assert body == {}
        return {}

    actions = build_actions([Operation(name="pets", description="Find Pets", path="/pets", method="get", result_filters=None)],
                            pet_store, "PetStore", do_call)
    assert len(actions) == 1
    action = actions[0]
    assert action.name == "pets"
    assert action.description == "Find Pets"
    assert action.title == "PetStore"
    assert action.sub_title == "pets"
    assert action.schema == {
        "type": "object",
        'properties': {'limit': {'format': 'int32', 'type': 'integer'},
                       'tags': {'items': {'type': 'string'}, 'type': 'array'},
                       'categories': {'items': {'type': 'string'}, 'type': 'array'},
                       },
        "required": []
    }
    await action.tool_call(None, **{"limit": 10, "tags": ["tag1", "tag2"], "categories": ["cat1", "cat2"]})
    assert tool_called


async def test_path_params(pet_store):
    tool_called = False

    def do_call(path_to_call, method, query_params, headers, body):
        nonlocal tool_called
        tool_called = True
        assert path_to_call == "/pets/10"
        assert method == "get"
        assert len(query_params) == 0
        assert headers == {}
        assert body == {}
        return {}

    actions = build_actions([Operation(name="get_pet", description="Get Pet", path="/pets/{id}", method="get", result_filters=None)],
                            pet_store, "PetStore", do_call)
    assert len(actions) == 1
    action = actions[0]
    assert action.name == "get_pet"
    assert action.description == "Get Pet"
    assert action.title == "PetStore"
    assert action.sub_title == "get_pet"
    assert action.schema == {
        "type": "object",
        'properties': {'id': {'format': 'int64', 'type': 'integer'}},
        "required": ['id']
    }
    await action.tool_call(None, **{"id": 10})
    assert tool_called


async def test_header_params(pet_store):
    tool_called = False

    def do_call(path_to_call, method, query_params, headers, body):
        nonlocal tool_called
        tool_called = True
        assert path_to_call == "/pets/findWithHeader"
        assert method == "get"
        assert len(query_params) == 0
        assert headers == {"id": '10'}
        assert body == {}
        return {}

    actions = build_actions([Operation(name="find_pet", description="Find Pet", path="/pets/findWithHeader", method="get", result_filters=None)],
                            pet_store, "PetStore", do_call)
    assert len(actions) == 1
    action = actions[0]
    assert action.name == "find_pet"
    assert action.description == "Find Pet"
    assert action.title == "PetStore"
    assert action.sub_title == "find_pet"
    assert action.schema == {
        "type": "object",
        'properties': {'id': {'format': 'int64', 'type': 'integer'}},
        "required": ['id']
    }
    await action.tool_call(None, **{"id": 10})
    assert tool_called


async def test_body_params(pet_store):
    tool_called = False

    def do_call(path_to_call, method, query_params, headers, body):
        nonlocal tool_called
        tool_called = True
        assert path_to_call == "/pets"
        assert method == "post"
        assert len(query_params) == 0
        assert headers == {}
        assert body == {"name": "dog", "tag": "pet"}
        return {}

    actions = build_actions([Operation(name="add_pet", description=None, path="/pets", method="post", result_filters=None)],
                            pet_store, "PetStore", do_call)
    assert len(actions) == 1
    action = actions[0]
    assert action.name == "add_pet"
    assert action.description == "Creates a new pet in the store. Duplicates are allowed"
    assert action.title == "PetStore"
    assert action.sub_title == "add_pet"
    assert action.schema == {
        "type": "object",
        "required": [
          "name"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "tag": {
            "type": "string"
          }
        }
      }
    await action.tool_call(None, **{"__body__": {"name": "dog", "tag": "pet"}})
    assert tool_called
