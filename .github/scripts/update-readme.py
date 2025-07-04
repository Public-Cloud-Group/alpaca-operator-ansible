#!/usr/bin/env python3
import re

start_tag = "<!-- support-matrix:start -->"
end_tag = "<!-- support-matrix:end -->"

with open("support_matrix.md", encoding="utf-8") as matrix_file:
    matrix_content = matrix_file.read().strip()

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

pattern = re.compile(
    f"{re.escape(start_tag)}(.*?){re.escape(end_tag)}",
    re.DOTALL,
)
replacement = f"{start_tag}\n\n{matrix_content}\n\n{end_tag}"
updated = pattern.sub(replacement, readme)

with open("README.md", "w", encoding="utf-8") as readme_file:
    readme_file.write(updated)
