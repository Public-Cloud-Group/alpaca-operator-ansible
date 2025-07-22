#!/usr/bin/env python3
import json
import sys

def merge_dicts(default_dict, override_dict):
    """
    Recursively merge two dictionaries, with override_dict taking precedence.
    Handles nested dictionaries and lists properly.
    """
    if not isinstance(default_dict, dict):
        return override_dict

    if not isinstance(override_dict, dict):
        return default_dict

    result = default_dict.copy()

    for key, value in override_dict.items():
        if value is None:
            # Skip None values - they don't override default values
            continue
        elif key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = merge_dicts(result[key], value)
        elif key in result and isinstance(result[key], list) and isinstance(value, list):
            # Merge lists by matching items with 'name' key, or combine them
            result[key] = merge_lists(result[key], value)
        else:
            # Override the value (only if it's not None)
            result[key] = value

    return result

def merge_lists(default_list, override_list):
    """
    Merge two lists. If both lists contain dictionaries with 'name' keys,
    merge them by matching the 'name' field. Otherwise, override the default list.
    """
    if not default_list:
        return override_list

    if not override_list:
        return default_list

    # Check if both lists contain dictionaries with 'name' keys
    if (isinstance(default_list[0], dict) and isinstance(override_list[0], dict) and
        'name' in default_list[0] and 'name' in override_list[0]):

        # Create a mapping of default items by name
        default_map = {item['name']: item for item in default_list}

        # Process override items
        for override_item in override_list:
            override_name = override_item['name']
            if override_name in default_map:
                # Recursively merge the matching items
                default_map[override_name] = merge_dicts(
                    default_map[override_name], override_item
                )
            else:
                # Add new item
                default_map[override_name] = override_item

        return list(default_map.values())
    else:
        # If not dictionaries with 'name' keys, override the default list
        return override_list

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: python3 merge_definitions.py <default_json> <override_json>"}))
        sys.exit(1)

    try:
        default_json = sys.argv[1]
        override_json = sys.argv[2]

        # Debug output to stderr
        print(f"Default JSON: {default_json}", file=sys.stderr)
        print(f"Override JSON: {override_json}", file=sys.stderr)

        default_dict = json.loads(default_json)
        override_dict = json.loads(override_json)

        # Debug output to stderr
        print(f"Default dict: {default_dict}", file=sys.stderr)
        print(f"Override dict: {override_dict}", file=sys.stderr)

        merged_dict = merge_dicts(default_dict, override_dict)

        # Debug output to stderr
        print(f"Merged dict: {merged_dict}", file=sys.stderr)

        print(json.dumps(merged_dict))

    except Exception as e:
        error_msg = {"error": f"Error during merge: {e}"}
        print(json.dumps(error_msg))
        sys.exit(1)