from eidolon_ai_sdk.util.filter_json import filter_and_reconstruct_json, filter_and_reconstruct_json_from_paths


def test_filter_json():
    original_json = [
        {
            "id": 1,
            "category": {"id": 2, "name": "Cats"},
            "name": "Cat 1",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag1"}, {"id": 2, "name": "tag2"}],
            "status": "available",
        },
        {
            "id": 2,
            "category": {"id": 2, "name": "Cats"},
            "name": "Cat 2",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag2"}, {"id": 2, "name": "tag3"}],
            "status": "available",
        },
        {
            "id": 4,
            "category": {"id": 1, "name": "Dogs"},
            "name": "Dog 1",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag1"}, {"id": 2, "name": "tag2"}],
            "status": "available",
        },
        {
            "id": 7,
            "category": {"id": 4, "name": "Lions"},
            "name": "Lion 1",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag1"}, {"id": 2, "name": "tag2"}],
            "status": "available",
        },
        {
            "id": 8,
            "category": {"id": 4, "name": "Lions"},
            "name": "Lion 2",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag2"}, {"id": 2, "name": "tag3"}],
            "status": "available",
        },
        {
            "id": 9,
            "category": {"id": 4, "name": "Lions"},
            "name": "Lion 3",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag3"}, {"id": 2, "name": "tag4"}],
            "status": "available",
        },
        {
            "id": 10,
            "category": {"id": 3, "name": "Rabbits"},
            "name": "Rabbit 1",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag3"}, {"id": 2, "name": "tag4"}],
            "status": "available",
        },
    ]

    result_filters = ["$.[*].name", "$.[*].status", "$.[*].tags[*].name", "$.[*].category[*].name"]

    reconstructed_json = filter_and_reconstruct_json(original_json, result_filters)
    assert reconstructed_json == [
        {
            "name": "Cat 1",
            "status": "available",
            "tags": [{"name": "tag1"}, {"name": "tag2"}],
            "category": [{"name": "Cats"}],
        },
        {
            "name": "Cat 2",
            "status": "available",
            "tags": [{"name": "tag2"}, {"name": "tag3"}],
            "category": [{"name": "Cats"}],
        },
        {
            "name": "Dog 1",
            "status": "available",
            "tags": [{"name": "tag1"}, {"name": "tag2"}],
            "category": [{"name": "Dogs"}],
        },
        {
            "name": "Lion 1",
            "status": "available",
            "tags": [{"name": "tag1"}, {"name": "tag2"}],
            "category": [{"name": "Lions"}],
        },
        {
            "name": "Lion 2",
            "status": "available",
            "tags": [{"name": "tag2"}, {"name": "tag3"}],
            "category": [{"name": "Lions"}],
        },
        {
            "name": "Lion 3",
            "status": "available",
            "tags": [{"name": "tag3"}, {"name": "tag4"}],
            "category": [{"name": "Lions"}],
        },
        {
            "name": "Rabbit 1",
            "status": "available",
            "tags": [{"name": "tag3"}, {"name": "tag4"}],
            "category": [{"name": "Rabbits"}],
        },
    ]


def test_filter_json_for_path_list():
    original_json = [
        {
            "id": 1,
            "category": {"id": 2, "name": "Cats"},
            "name": "Cat 1",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag1"}, {"id": 2, "name": "tag2"}],
            "status": "available",
        },
        {
            "id": 2,
            "category": {"id": 2, "name": "Cats"},
            "name": "Cat 2",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag2"}, {"id": 2, "name": "tag3"}],
            "status": "available",
        },
        {
            "id": 4,
            "category": {"id": 1, "name": "Dogs"},
            "name": "Dog 1",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag1"}, {"id": 2, "name": "tag2"}],
            "status": "available",
        },
        {
            "id": 7,
            "category": {"id": 4, "name": "Lions"},
            "name": "Lion 1",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag1"}, {"id": 2, "name": "tag2"}],
            "status": "available",
        },
        {
            "id": 8,
            "category": {"id": 4, "name": "Lions"},
            "name": "Lion 2",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag2"}, {"id": 2, "name": "tag3"}],
            "status": "available",
        },
        {
            "id": 9,
            "category": {"id": 4, "name": "Lions"},
            "name": "Lion 3",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag3"}, {"id": 2, "name": "tag4"}],
            "status": "available",
        },
        {
            "id": 10,
            "category": {"id": 3, "name": "Rabbits"},
            "name": "Rabbit 1",
            "photoUrls": ["url1", "url2"],
            "tags": [{"id": 1, "name": "tag3"}, {"id": 2, "name": "tag4"}],
            "status": "available",
        },
    ]

    result_filters = ["name", "status", "tags.name", "category.name"]

    reconstructed_json = filter_and_reconstruct_json_from_paths(original_json, result_filters)
    assert reconstructed_json == [
        {
            "name": "Cat 1",
            "status": "available",
            "tags": [{"name": "tag1"}, {"name": "tag2"}],
            "category": {"name": "Cats"},
        },
        {
            "name": "Cat 2",
            "status": "available",
            "tags": [{"name": "tag2"}, {"name": "tag3"}],
            "category": {"name": "Cats"},
        },
        {
            "name": "Dog 1",
            "status": "available",
            "tags": [{"name": "tag1"}, {"name": "tag2"}],
            "category": {"name": "Dogs"},
        },
        {
            "name": "Lion 1",
            "status": "available",
            "tags": [{"name": "tag1"}, {"name": "tag2"}],
            "category": {"name": "Lions"},
        },
        {
            "name": "Lion 2",
            "status": "available",
            "tags": [{"name": "tag2"}, {"name": "tag3"}],
            "category": {"name": "Lions"},
        },
        {
            "name": "Lion 3",
            "status": "available",
            "tags": [{"name": "tag3"}, {"name": "tag4"}],
            "category": {"name": "Lions"},
        },
        {
            "name": "Rabbit 1",
            "status": "available",
            "tags": [{"name": "tag3"}, {"name": "tag4"}],
            "category": {"name": "Rabbits"},
        },
    ]
