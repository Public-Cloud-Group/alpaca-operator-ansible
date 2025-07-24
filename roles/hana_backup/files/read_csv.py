# Copyright: Contributors to the Ansible project
# Apache License, Version 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)


import csv
import json
import sys


def read_csv_file(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        return []


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 read_csv.py <csv_file_path>", file=sys.stderr)
        sys.exit(1)

    csv_file_path = sys.argv[1]
    data = read_csv_file(csv_file_path)
    print(json.dumps(data))
