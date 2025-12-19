# Development Files

⚠️ **WARNING: This folder contains development files only!**

This `.dev` folder is **NOT** intended for normal use or production deployment. It contains files and configurations that are specifically designed for development and testing purposes.

## Contents

- `scripts/` - Development and testing scripts
  - `local-test.sh` - Run CI/CD tests locally using Docker
  - `test-matrix.sh` - Test multiple Python/Ansible version combinations
  - `generate_changelog.sh` - Generate changelog from fragments
- `test/` - Local test results and artifacts (see `test/README.md` for details)
- `ansible.cfg` - Development-specific Ansible configuration
- `playbooks/` - Test playbooks for development and debugging
- `inventories/` - Development inventory files

## Usage

These files should only be used by developers working on the alpaca-operator-ansible project for:

- Testing new features
- Debugging issues
- Development environment setup
- Local development workflows
- **Local CI/CD testing** - Test collection builds and sanity tests before pushing to the repository

## Local CI/CD Testing

The `.dev/scripts/local-test.sh` script allows you to run parts of the CI/CD workflow locally:

```bash
# Test with default versions (Python 3.11, Ansible 2.18)
./.dev/scripts/local-test.sh

# Test with custom versions
PYTHON_VERSION=3.12 ANSIBLE_VERSION=2.19 ./.dev/scripts/local-test.sh
```

The script will:
1. Build the Ansible collection in a Docker container
2. Save the built collection to `.dev/test/release-<VERSION>/collection/`
3. Install the collection in the container
4. Run ansible-test sanity tests
5. Save logs and results to `.dev/test/release-<VERSION>/`

For testing multiple version combinations, use `test-matrix.sh`:

```bash
./.dev/scripts/test-matrix.sh
```

See `test/README.md` for more details about the test results structure.

## For Production Use

For normal usage and production deployment, please refer to the main project documentation and use the files in the root directory and `templates/` folder.

**Do not use files from this `.dev` folder in production environments!**