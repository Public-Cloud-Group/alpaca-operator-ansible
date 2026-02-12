## Release Workflow for `pcg.alpaca_operator`

This document describes the standard workflow for publishing a new version of the `pcg.alpaca_operator` collection.

---

## 1. Create the release branch

- Create a new branch from `main` with the name:
  - `release-X.X.X` (for example: `release-2.1.2`)

---

## 2. Bump the version in relevant files

Update the collection version:

- `galaxy.yml`
  - Set the `version` field to the new version:
    ```yaml
    version: X.X.X
    ```

---

## 3. Create a changelog fragment

Create a new fragment file:

- Path: `changelogs/fragments/release-X.X.X.yml`

Suggested template:

```yaml
---
release_summary: |
  Release X.X.X <short 1–3 sentence summary of what this release delivers>.

major_changes:
  - "Optional: list major / headline changes for this release."

minor_changes:
  - "Optional: list smaller features or improvements."

bugfixes:
  - "Describe each bugfix in a short, precise sentence."
  - "Add one entry per relevant fix."

breaking_changes:
  - "Optional: describe breaking changes and include a short porting guide if needed."

trivial:
  - "Optional: documentation-only, CI-only, or purely internal refactoring changes."
```

You can remove any sections (`major_changes`, `breaking_changes`, `trivial`, etc.) that are not needed for a given release.
At minimum, `release_summary` should be present, and usually `minor_changes` and/or `bugfixes`.

---

## 4. Implement the release changes

Implement all code, documentation, and test changes planned for this release:

- Update modules, utilities, and documentation as needed.
- Keep the changelog fragment (`changelogs/fragments/release-X.X.X.yml`) in sync with the implemented changes.

---

## 5. Verify (and update) Support Matrix

Verify that the [Ansible support matrix](https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html) aligns with our support and test matrix in GitLab CI.

---

## 6. Open a Pull Request into `main`

- Open a Pull Request from `release-X.X.X` into `main`.
- Ensure:
  - CI passes.
  - The release notes in the changelog fragment are correct and complete.
  - The version in `galaxy.yml` is correct.

Once the PR is reviewed and approved, merge it into `main`.
