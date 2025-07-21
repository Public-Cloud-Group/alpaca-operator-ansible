#!/usr/bin/env python3
import json
import sys

def recursive_merge(base_dict, override_dict):
    """
    Recursively merge two dictionaries, with override_dict taking precedence.
    None values in override_dict are ignored (they don't override base values).
    """
    if not isinstance(base_dict, dict):
        return override_dict

    if not isinstance(override_dict, dict):
        return base_dict

    result = base_dict.copy()

    for key, value in override_dict.items():
        if value is None:
            # Skip None values - they don't override base values
            continue
        elif key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = recursive_merge(result[key], value)
        elif key in result and isinstance(result[key], list) and isinstance(value, list):
            # For lists, we need to merge by index or by matching keys
            result[key] = merge_lists(result[key], value)
        else:
            # Override the value (only if it's not None)
            result[key] = value

    return result

def merge_lists(base_list, override_list):
    """
    Merge two lists. If both lists contain dictionaries with 'name' keys,
    merge them by matching the 'name' field. Otherwise, override the base list.
    """
    if not base_list:
        return override_list

    if not override_list:
        return base_list

    # Check if both lists contain dictionaries with 'name' keys
    if (isinstance(base_list[0], dict) and isinstance(override_list[0], dict) and
        'name' in base_list[0] and 'name' in override_list[0]):

        # Create a mapping of base items by name
        base_map = {item['name']: item for item in base_list}

        # Merge override items
        for override_item in override_list:
            if override_item['name'] in base_map:
                # Recursively merge the matching items
                base_map[override_item['name']] = recursive_merge(
                    base_map[override_item['name']], override_item
                )
            else:
                # Add new item
                base_map[override_item['name']] = override_item

        return list(base_map.values())
    else:
        # If not dictionaries with 'name' keys, override the base list
        return override_list

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: python3 merge_definitions.py <base_json> <override_json>"}))
        sys.exit(1)

    try:
        base_json = sys.argv[1]
        override_json = sys.argv[2]

        # Debug output to stderr
        print(f"Base JSON: {base_json}", file=sys.stderr)
        print(f"Override JSON: {override_json}", file=sys.stderr)

        base_dict = json.loads(base_json)
        override_dict = json.loads(override_json)

        # Debug output to stderr
        print(f"Base dict: {base_dict}", file=sys.stderr)
        print(f"Override dict: {override_dict}", file=sys.stderr)

        merged_dict = recursive_merge(base_dict, override_dict)

        # Debug output to stderr
        print(f"Merged dict: {merged_dict}", file=sys.stderr)

        print(json.dumps(merged_dict))

    except Exception as e:
        error_msg = {"error": f"Error during merge: {e}"}
        print(json.dumps(error_msg))
        sys.exit(1)