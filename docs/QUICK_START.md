# Quick Start Guide - ALPACA Operator Collection

## Target Audience

This guide is specifically designed for **Public Cloud Group GmbH Delivery** who need to:
- Set up and configure Ansible automation for ALPACA Operator environments
- Deploy and manage ALPACA Operator commands and workflows

---

This guide will help you set up Ansible and the ALPACA Operator collection on SLES for local execution with ALPACA API access. The instructions describe the installation directly on the ALPACA Operator server itself.

## Prerequisites

- SLES 15 SP4 or later
- Root or sudo access
- Internet connectivity for package installation
- ALPACA Operator API accessible from the local machine

## Step 1: Check Python Version

First, determine your Python version to select the appropriate Ansible version:

```bash
ls /usr/bin/python*
python3 --version
```

Refer to the [Support Matrix](../README.md#support-matrix) in the main README to determine which Ansible version is compatible with your Python version.

## Step 2: Install Ansible

### Option A: Install via Zypper (Recommended)

```bash
# Add the Ansible repository
sudo zypper addrepo https://download.opensuse.org/repositories/systemsmanagement:/ansible/SLE_15_SP4/ ansible

# Refresh repositories
sudo zypper refresh

# Install Ansible (replace X.Y with your chosen version, e.g., 2.17)
sudo zypper install ansible-2.17
```

### Option B: Install via pip

```bash
# Install pip if not available
sudo zypper install python3-pip

# Install specific Ansible version (replace X.Y.Z with your chosen version)
pip3 install ansible==2.17.0
```

### Verify Installation

```bash
ansible --version
```

## Step 3: Install ALPACA Operator Collection

### Option A: Install from Ansible Galaxy (Recommended)

```bash
ansible-galaxy collection install pcg.alpaca_operator
```

### Option B: Install from Git Repository

```bash
ansible-galaxy collection install git+https://github.com/pcg-sap/alpaca-operator-ansible.git
```

### Option C: Manual Installation from Release

1. Download the latest release from [GitHub Releases](https://github.com/pcg-sap/alpaca-operator-ansible/releases)
2. Extract the archive
3. Install manually:

```bash
# Navigate to the extracted directory
cd alpaca-operator-ansible-*

# Install the collection
ansible-galaxy collection install .

# Verify collection was installed
ansible-galaxy collection list
```

## Step 4: Install Python Dependencies

After installing the collection, install the required Python packages from the collection's requirements:

```bash
# Install pip if not available (if not already installed)
sudo zypper install python3-pip

# Install required packages from the collection
pip3 install -r ~/.ansible/collections/ansible_collections/pcg/alpaca_operator/requirements.txt
```

**Note**: If you installed the collection manually, the path might be different. Adjust the path to where you extracted the collection.

## Step 5: Create Project Directory

Create a working directory:

```bash
mkdir -p ~/alpaca-ansible-automation
cd ~/alpaca-ansible-automation
```

## Step 6: Configure Ansible

Create an Ansible configuration file:

```bash
cat > ansible.cfg << 'EOF'
[defaults]
inventory = ./inventory.ini
host_key_checking = False
EOF
```

## Step 7: Create Inventory

Create a simple inventory for local execution with ALPACA API configuration:

```bash
cat > inventory.ini << 'EOF'
[local]
localhost ansible_connection=local

[local:vars]
ansible_python_interpreter=/usr/bin/python3

# ALPACA API Configuration
ALPACA_Operator_API_Host='localhost'
ALPACA_Operator_API_Protocol='https'
ALPACA_Operator_API_Port='8443'
ALPACA_Operator_API_Username='<username>'
ALPACA_Operator_API_Password='<password>'
ALPACA_Operator_API_Validate_Certs=False
EOF
```

**Note**: Ensure to customize API username and password here according to your needs.

**Note**: If you have multiple Python versions installed, you can specify the exact interpreter path. Common alternatives:
- `/usr/bin/python3.9` - Python 3.9
- `/usr/bin/python3.10` - Python 3.10
- `/usr/bin/python3.11` - Python 3.11
- `/usr/bin/python3.12` - Python 3.12

You can check available Python versions with:
```bash
ls /usr/bin/python*
python3 --version
```

## Step 8: Test Connection

Test the ALPACA API connection (using variables from inventory):

```bash
mkdir playbooks
cat > playbooks/test_connection.yml << 'EOF'
---
- name: Test ALPACA API Connection
  hosts: local
  gather_facts: false

  tasks:
    - name: Test API connection using ALPACA module utilities
      block:
        - name: Import ALPACA API utilities
          set_fact:
            api_url: "{{ ALPACA_Operator_API_Protocol }}://{{ ALPACA_Operator_API_Host }}:{{ ALPACA_Operator_API_Port }}/api"

        - name: Test authentication and API access
          uri:
            url: "{{ api_url }}/auth/login"
            method: POST
            body_format: json
            body: '{"username": "{{ ALPACA_Operator_API_Username }}", "password": "{{ ALPACA_Operator_API_Password }}"}'
            validate_certs: "{{ ALPACA_Operator_API_Validate_Certs }}"
            status_code: [200, 401, 403]
          register: auth_test

        - name: Display authentication result
          debug:
            msg: "Authentication test: {{ 'SUCCESS' if auth_test.status == 200 else 'FAILED' }} (Status: {{ auth_test.status }})"

        - name: Show API token (if authentication successful)
          debug:
            msg: "API Token obtained: {{ auth_test.json.token | default('None') | truncate(20, true, '...') }}"
          when: auth_test.status == 200

      rescue:
        - name: Display connection error
          debug:
            msg: "Connection failed: {{ ansible_failed_result.msg | default('Unknown error') }}"
          failed_when: true

EOF

# Run the test
ansible-playbook playbooks/test_connection.yml
```

## Step 9: Create Sample CSV File

Create a sample CSV file for the HANA backup role:

```bash
cat > systems.csv << 'EOF'
primary_system;hdb_nw_sid;hdb_tenant;system_type;system_staging;system_sla;system_vm_type;system_vm_flavor;system_vdns;system_az;hdb_data_min;hdb_data_max;hdb_log_min;hdb_log_max;hdb_shared_min;hdb_shared_max;Instance_no
MUP;MHP;MUP;HDB;rg-sap-010msb-prod;SLA2;Standard_E32ds_v5;hdb-t-e;hdbmhpa;3;1;2;3;4;5;6;05
EOF
```

## Step 10: Create First Playbook

Copy the HANA backup template and customize it:

```bash
mkdir playbooks
cp ~/.ansible/collections/ansible_collections/pcg/alpaca_operator/templates/playbooks/hana_backup_role.yml playbooks/hana_backup_demo.yml
```

Edit the playbook (the ALPACA API configuration is now in the inventory):

```yaml
---
- name: HANA Backup - Generate and Execute Commands from CSV
  hosts: local
  gather_facts: false

  vars:
    csv_file: "../systems.csv"

  tasks:
    - name: Execute hana_backup role
      include_role:
        name: pcg.alpaca_operator.hana_backup
```

### Understanding CSV Variables

The HANA backup role automatically maps CSV columns to variables that you can use in your playbooks. Here are the available variables:

| CSV Column            | Variable Name          | Description | Example Value          |
| --------------------- | ---------------------- | ----------- | ---------------------- |
| `primary_system`      | `{ primarySystem }`    | N/A         | `"MUP"`                |
| `hdb_nw_sid`          | `{ systemName }`       | N/A         | `"MHP"`                |
| `hdb_tenant`          | `{ hdbTenant }`        | N/A         | `"MUP"`                |
| `system_vdns`         | `{ agentName }`        | N/A         | `"hdbmhpa"`            |
| `system_sla`          | `{ systemSla }`        | N/A         | `"SLA2"`               |
| `system_type`         | `{ systemType }`       | N/A         | `"HDB"`                |
| `system_staging`      | `{ systemStaging }`    | N/A         | `"rg-sap-010msb-prod"` |
| `system_vm_type`      | `{ systemVmType }`     | N/A         | `"Standard_E32ds_v5"`  |
| `system_vm_flavor`    | `{ systemVmFlavor }`   | N/A         | `"hdb-t-e"`            |
| `system_az`           | `{ systemAz }`         | N/A         | `"3"`                  |
| `hdb_data_min`        | `{ hdbDataMin }`       | N/A         | `"1"`                  |
| `hdb_data_max`        | `{ hdbDataMax }`       | N/A         | `"2"`                  |
| `hdb_log_min`         | `{ hdbLogMin }`        | N/A         | `"3"`                  |
| `hdb_log_max`         | `{ hdbLogMax }`        | N/A         | `"4"`                  |
| `hdb_shared_min`      | `{ hdbSharedMin }`     | N/A         | `"5"`                  |
| `hdb_shared_max`      | `{ hdbSharedMax }`     | N/A         | `"6"`                  |
| `Instance_no`         | `{ instanceNo }`       | N/A         | `"05"`                 |
| `alpaca_ext_pool_old` | `{ alpacaExtPoolOld }` | N/A         | `"SomeValue"`          |
| `alpaca_ext_pool_new` | `{ alpacaExtPoolNew }` | N/A         | `"SomeValue"`          |

**⚠️ IMPORTANT**: CSV variables must be enclosed in curly braces `{ variableName }` when used in command parameters. This is mandatory for proper variable substitution.

### Example: Using CSV Variables in Command Parameters

```yaml
---
- name: HANA Backup with CSV Variables
  hosts: local
  gather_facts: false

  vars:
    csv_file: "../systems.csv"

  tasks:
    - name: Execute hana_backup role with custom commands
      include_role:
        name: pcg.alpaca_operator.hana_backup
      vars:
        override:
          commands:
            - name: "HANA BACKUP SNAP"
              processCentralId: 8990048
              parameters: "-s { systemName } -i { hdbTenant } -m pms_onl_cons -c localhost -t 3 -p $LOCAL_SNAP_RET -u BACKUP"
            - name: "HANA BACKUP FILE DAILY"
              processCentralId: 8990048
              parameters: "-s { systemName } -d <BKP_DATA_DEST1> -r - -b { local_file_ret } -t ALL -m file -p full -u BACKUP -A blob -B <BKP_LB_DATA_01> -C $SKEY -D { blob_file_ret }"
```

## Step 11: Run Your First Playbook

Execute the HANA backup playbook:

```bash
# Run in check mode first (dry run)
ansible-playbook playbooks/hana_backup_demo.yml --check -v
```

**Note**: The playbook will most likely fail on the first run when trying to create the first command, because the specified system (e.g., `HDB`) in the example CSV file we created here does not exist in the ALPACA Operator. This is normal and expected.

## Troubleshooting

### Common Issues

1. **Python Version Mismatch**
   ```bash
   # Check Python version used by Ansible
   ansible localhost -m setup -a 'filter=ansible_python_version'
   ```

2. **Collection Not Found**
   ```bash
   # List installed collections
   ansible-galaxy collection list

   # Reinstall if needed
   ansible-galaxy collection install pcg.alpaca_operator --force

3. **CSV File Issues**
   - Ensure semicolon (`;`) delimiter
   - Check file permissions
   - Verify required columns are present

### Logging

Enable verbose output for debugging:

```bash
ansible-playbook playbooks/hana_backup_demo.yml -v
ansible-playbook playbooks/hana_backup_demo.yml -vv
ansible-playbook playbooks/hana_backup_demo.yml -vvv
```

## Next Steps

1. **Customize CSV Data**: Update `systems.csv` with your actual HANA systems or link to another CSV file
2. **Configure playbook**: Create a new or modify one of the template playbooks