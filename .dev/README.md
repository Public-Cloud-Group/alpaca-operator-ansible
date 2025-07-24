# Development Files

⚠️ **WARNING: This folder contains development files only!**

This `.dev` folder is **NOT** intended for normal use or production deployment. It contains files and configurations that are specifically designed for development and testing purposes.

## Contents

- `start-container.sh` - Development container startup script
- `ansible.cfg` - Development-specific Ansible configuration
- `playbooks/` - Test playbooks for development and debugging
- `inventories/` - Development inventory files

## Usage

These files should only be used by developers working on the alpaca-operator-ansible project for:

- Testing new features
- Debugging issues
- Development environment setup
- Local development workflows

## For Production Use

For normal usage and production deployment, please refer to the main project documentation and use the files in the root directory and `templates/` folder.

**Do not use files from this `.dev` folder in production environments!**