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
                path_parts = str(match.full_path).split('.')
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
                    if part.startswith('[') and part.endswith(']'):
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

                if path_parts[-1].startswith('[') and path_parts[-1].endswith(']'):
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
