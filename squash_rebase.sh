#!/bin/bash

# Create a temporary file with the rebase instructions
cat > /tmp/rebase_instructions << 'EOF'
pick 3c8f8a5 dev
squash 02f8c68 CI: Add weekly run
squash 401d2d7 CI: ignore .tmp directory on sanity test
squash e7e5f2f CI: skip no-smart-quotes for .tmp/.notes.md
squash 02f8c68 Update support matrix [ci skip]
squash d849202 dev
squash 6325629 add j2 based role
squash d586ad3 dev
squash 85ef3df dev
squash a9f366c ci-test
squash e7301f6 ci-test
squash bd4308f Update support matrix [ci skip]
squash f701d1b dev
squash 35da916 Remove dynamic_command_generator role and associated files; retain swm_prod.csv in .tmp directory for reference.
squash 2a003e6 Update support matrix [ci skip]
squash a43b617 Refactor HANA backup role to enhance command generation and configuration. Introduced global and SLA-specific parameters, removed obsolete command templates, and updated README for clarity. Adjusted playbook structure for improved command execution and error handling.
squash 5a9aac9 Merge branch 'ansible-roles' of https://github.com/pcg-sap/alpaca-operator-ansible into ansible-roles
squash 3b43b66 Remove obsolete HANA backup YAML files and update README for improved clarity on role functionality and command generation. Refactor role defaults and task structure to enhance configuration management and error handling.
squash 044856b Update HANA backup role configuration and testing playbooks. Replace obsolete command references with new commands in role defaults, enhance parameter handling in task generation, and adjust test playbook paths for consistency.
squash 1911b76 Refactor HANA backup role to streamline command generation and enhance configuration management. Introduced a new merging strategy for command defaults, improved SLA handling, and updated task structures for better readability and maintainability. Added debug statements for improved visibility during execution.
squash a2f1ceb Remove obsolete `hana_backup.zip` file and enhance the README with detailed role functionality, including a comprehensive overview, quick start guide, and updated command examples. Refactor role defaults to streamline command definitions and improve clarity on SLA configurations.
squash d25be10 Remove shebang line from `read_csv.py` for improved compatibility and maintainability. Added a blank line for better code readability.
squash b3b0005 Add release workflow to GitHub Actions for Ansible Collection. Includes steps for version extraction, release creation, and package upload, ensuring releases are only created if they do not already exist.
squash babcf70 Refactor release workflow in GitHub Actions to include branch-specific tagging and release notes. The workflow now generates development release tags for non-main branches and updates the release title and notes accordingly, ensuring better clarity and organization for versioning.
squash 4be5b36 Add PyYAML installation to GitHub Actions workflow for enhanced dependency management during testing.
squash 7a29709 Add GitHub Actions workflow environment variable for GitHub token to enhance authentication during testing.
squash 4bf51f7 Remove upload step for GitHub Packages from the release workflow in GitHub Actions, ensuring that releases are only created if they do not already exist.
squash be72a87 Enhance GitHub Actions release workflow by adding a temporary build directory for Ansible collection packaging. Streamline release creation process by checking for existing releases and updating them if necessary, improving overall efficiency and clarity.
squash 4199fa6 Update support matrix [ci skip]
squash 023885d Remove GitHub Actions test workflow for Ansible collection, streamlining CI processes by eliminating unnecessary complexity. This change simplifies the overall workflow management and focuses on essential tasks.
squash 38714d1 Refactor GitHub Actions release workflow to improve handling of existing releases. Added checks to delete existing releases before creating new ones, ensuring a clean release process. Streamlined the build process for the Ansible collection by removing unnecessary temporary directory steps.
squash 569c381 Update support matrix [ci skip]
squash b07cd8 Update GitHub Actions release workflow to allow clobbering of existing package uploads, ensuring that new versions can overwrite previous ones during the release process.
squash ab69ca3 Refactor README and QUICK_START documentation for clarity and accuracy. Update inventory paths and API connection examples to use variables. Enhance HANA backup role tasks with debugging information. Adjust playbook structure for better organization and usability.
squash a6612b8 Update README.md to include details about the new `hana_backup` role, its usage, CSV file requirements, and supported commands. Adjust API connection examples to use variables instead of hardcoded values. Modify CI/CD workflow to ignore all markdown files for push and pull request events.
squash bc4ff22 Update support matrix [ci skip]
squash 493939f Update QUICK_START documentation to include verification step for collection installation. Modify API configuration to use placeholder values for username and password. Adjust playbook host definition for consistency. Refactor HANA backup role defaults by commenting out unused commands and updating CSV file path in playbook template. Change permissions for read_csv.py script to make it executable. Add check mode option to CSV reading task for improved task management.
squash 2366af3 Update QUICK_START documentation to include verification step for collection installation. Modify API configuration to use placeholder values for username and password. Adjust playbook host definition for consistency. Refactor HANA backup role defaults by commenting out unused commands and updating CSV file path in playbook template. Change permissions for read_csv.py script to make it executable. Add check mode option to CSV reading task for improved task management.
squash 35e3eeb Merge branch 'ansible-roles' of https://github.com/pcg-sap/alpaca-operator-ansible into ansible-roles
squash 3c16a57 Refactor playbook templates by removing unused command and agent templates, and updating the HANA backup demo playbook path. Modify start-container script to reflect the new full stack deployment playbook name.
squash 35051a3 Update support matrix [ci skip]
squash a8ef551 Change permissions of read_csv.py script to non-executable and comment out unused command templates in the HANA backup playbook for clarity and maintainability.
squash ea45571 Update HANA backup role playbook to change default state from 'absent' to 'present' for improved clarity in command configuration.
squash cfbc2ee Update support matrix [ci skip]
squash e6dc276 Add target audience section to QUICK_START documentation for clarity on intended users and their setup needs.
squash 3ee6da4 Update license information across multiple files from GPL-3.0-or-later to Apache License, Version 2.0, and adjust related documentation accordingly.
squash c8346ad Update support matrix [ci skip]
squash b2148b4 Update support matrix [ci skip]
squash 6564d41 Update license information for multiple plugins to reflect the use of Apache-2.0 instead of GPLv3 in the ignore files.
squash 1dc1522 Update ignore files to clarify internal use only for certain scripts and enhance license information for multiple plugins to reflect Apache-2.0 usage with issue references.
squash 4828566 Fix license link in HANA backup README to point to the correct relative path for the LICENSE file.
squash c2b7992 Refactor QUICK_START documentation and remove obsolete test files
squash 30f34a6 Update support matrix [ci skip]
squash cf2dfbc Update support matrix [ci skip]
squash b5056b2 Remove obsolete Ansible configuration, scripts, and playbooks to streamline project structure
EOF

# Perform the rebase using the instructions
git rebase -i main --exec < /tmp/rebase_instructions

# Clean up
rm /tmp/rebase_instructions
EOF 