#!/usr/bin/env python3
import pandas as pd
import sys
from distutils.version import LooseVersion

df = pd.read_csv(sys.argv[1], sep=';', names=['python', 'ansible', 'status'], dtype={'python': str, 'ansible': str, 'status': str})

if df.empty:
    print("No results found.")
    sys.exit(0)

py_versions = sorted([v for v in df['python'].unique() if isinstance(v, str) and v.startswith("3.")], key=LooseVersion)
ansible_versions = sorted(df['ansible'].unique(), key=lambda x: list(map(int, x.split('.'))))

header = "|             | " + " | ".join([f"Ansible {v}.*" for v in ansible_versions]) + " |"
separator = "| ----------- |" + " -------------- |" * len(ansible_versions)

print(header)
print(separator)

for py in py_versions:
    row = [f"Python {py}"]
    for ans in ansible_versions:
        match = df[(df['python'] == py) & (df['ansible'] == ans)]
        if match.empty:
            row.append("⬜")  # not tested
        else:
            status = match.iloc[0]['status']
            symbol = {"tested": "✅", "failed": "❌", "unsupported": "⚠️"}.get(str(status).strip(), "❓")
            row.append(symbol)
    print("| " + " | ".join(row) + " |")
