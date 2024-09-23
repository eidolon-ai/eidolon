from typing import List

from jsonpath_ng.ext import parse


def filter_and_reconstruct_json(original_json, result_filters):
    # Parse the original JSON string into a Python object
    original_data = original_json

    def process_item(item):
        if isinstance(item, list):
            filtered_item = []
        else:
            filtered_item = {}

        # Iterate over the result filters
        for result_filter in result_filters:
            # Parse the JSON path expression
            json_path = parse(result_filter)

            # Find the matching nodes in the item
            matches = json_path.find(item)

            # Extract the values and add them to the filtered item
            for match in matches:
                path_parts = str(match.full_path).split(".")
                current = filtered_item

                def update_current(parent, path):
                    nonlocal current

                    def _fn(value):
                        nonlocal current
                        parent[path] = value
                        return value

                    return _fn

                current_updater = None

                for part in path_parts[:-1]:
                    if part.startswith("[") and part.endswith("]"):
                        index = int(part[1:-1])
                        if not isinstance(current, list):
                            current = current_updater([])
                        if len(current) <= index:
                            current.extend([{}] * (index - len(current) + 1))
                        current = current[index]
                    else:
                        if part not in current:
                            current_updater = update_current(current, part)
                            current[part] = {}
                        current = current[part]

                if path_parts[-1].startswith("[") and path_parts[-1].endswith("]"):
                    index = int(path_parts[-1][1:-1])
                    if not isinstance(current, list):
                        current = []
                    if len(current) <= index:
                        current.extend([{}] * (index - len(current) + 1))
                    current[index] = match.value
                else:
                    current[path_parts[-1]] = match.value

        return filtered_item

    filtered_data = process_item(original_data)

    # Convert the filtered data back to a JSON string
    reconstructed_json = filtered_data
    return reconstructed_json


def _process_item(item, path_obj: dict):
    if isinstance(item, list):
        filtered_item = []
        for i in item:
            filtered_item.append(_process_item(i, path_obj))
        return filtered_item
    elif isinstance(item, dict):
        filtered_item = {}
        for key, value in item.items():
            if key in path_obj:
                filtered_item[key] = _process_item(value, path_obj[key])
        return filtered_item
    else:
        return item


def filter_and_reconstruct_json_from_paths(original_json, paths: List[str]):
    # convert the paths into an object
    path_obj = {}
    for path in paths:
        path_parts = path.split(".")
        current = path_obj
        for part in path_parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    return _process_item(original_json, path_obj)
