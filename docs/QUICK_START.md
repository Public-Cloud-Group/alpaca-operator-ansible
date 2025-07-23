# Quick Start Guide - ALPACA Operator Collection

This guide will help you set up Ansible and the ALPACA Operator collection on SLES 15 for local execution with ALPACA API access.

## Prerequisites

- SLES 15 SP4 or later
- Root or sudo access
- Internet connectivity for package installation
- ALPACA Operator API accessible from the local machine

## Step 1: Check Python Version

First, determine your Python version to select the appropriate Ansible version:

```bash
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
```

## Step 4: Install Python Dependencies

After installing the collection, install the required Python packages from the collection's requirements:

```bash
# Install pip if not available (if not already installed)
sudo zypper install python3-pip

# Install required packages from the collection
pip3 install -r /usr/share/ansible/collections/ansible_collections/pcg/alpaca_operator/requirements.txt
```

**Note**: If you installed the collection manually, the path might be different. Adjust the path to where you extracted the collection.

## Step 5: Create Project Directory

Create a working directory for your ALPACA automation:

```bash
mkdir -p ~/alpaca-automation
cd ~/alpaca-automation
```

## Step 6: Configure Ansible

Create an Ansible configuration file:

```bash
cat > ansible.cfg << 'EOF'
[defaults]
inventory = ./inventory
host_key_checking = False
stdout_callback = yaml
gathering = smart
fact_caching = memory

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
EOF
```

## Step 7: Create Inventory

Create a simple inventory for local execution with ALPACA API configuration:

```bash
mkdir inventory
cat > inventory/hosts << 'EOF'
[alpaca]
localhost ansible_connection=local

[alpaca:vars]
ansible_python_interpreter=/usr/bin/python3

# ALPACA API Configuration
ALPACA_Operator_API_Host: "localhost"  # or your ALPACA host
ALPACA_Operator_API_Protocol: "https"
ALPACA_Operator_API_Port: 8443
ALPACA_Operator_API_Username: "your_username"
ALPACA_Operator_API_Password: "your_password"
ALPACA_Operator_API_Validate_Certs: false  # Set to true for production
EOF
```

**Note**: If you have multiple Python versions installed, you can specify the exact interpreter path. Common alternatives:
- `/usr/bin/python3.9` - Python 3.9
- `/usr/bin/python3.10` - Python 3.10
- `/usr/bin/python3.11` - Python 3.11
- `/usr/bin/python3.12` - Python 3.12

You can check available Python versions with:
```bash
ls /usr/bin/python*
which python3
python3 --version
```

## Step 8: Create Sample CSV File

Create a sample CSV file for the HANA backup role:

```bash
cat > systems.csv << 'EOF'
hdb_nw_sid;system_vdns;system_sla;system_type;system_staging;Instance_no
HDB;localhost;SLA1;PROD;PROD;00
EOF
```

## Step 9: Create First Playbook

Copy the HANA backup template and customize it:

```bash
# Copy the template
cp /usr/share/ansible/collections/ansible_collections/pcg/alpaca_operator/templates/playbooks/template_commands_hana_backup_role.yml hana_backup_demo.yml

# Or if using manual installation, copy from your extracted directory
# cp /path/to/extracted/alpaca-operator-ansible/templates/playbooks/template_commands_hana_backup_role.yml hana_backup_demo.yml
```

Edit the playbook (the ALPACA API configuration is now in the inventory):

```yaml
---
- name: HANA Backup - Generate and Execute Commands from CSV
  hosts: localhost
  gather_facts: false

  vars:
    csv_file: "./systems.csv"

  tasks:
    - name: Include hana_backup role
      include_role:
        name: hana_backup
```

## Step 10: Test Connection

Before running the full playbook, test the ALPACA API connection (using variables from inventory):

```bash
cat > test_connection.yml << 'EOF'
---
- name: Test ALPACA API Connection
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Test API connection
      uri:
        url: "{{ ALPACA_Operator_API_Protocol }}://{{ ALPACA_Operator_API_Host }}:{{ ALPACA_Operator_API_Port }}/api/v1/health"
        method: GET
        user: "{{ ALPACA_Operator_API_Username }}"
        password: "{{ ALPACA_Operator_API_Password }}"
        validate_certs: "{{ ALPACA_Operator_API_Validate_Certs }}"
        status_code: [200, 401, 403]
      register: api_test

    - name: Display connection result
      debug:
        var: api_test
EOF

# Run the test
ansible-playbook test_connection.yml
```

## Step 11: Run Your First Playbook

Execute the HANA backup playbook:

```bash
# Run in check mode first (dry run)
ansible-playbook hana_backup_demo.yml --check

# Run the actual playbook
ansible-playbook hana_backup_demo.yml
```

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
   ```

3. **API Connection Issues**
   - Verify ALPACA Operator is running
   - Check firewall settings
   - Verify API credentials
   - Test with curl:
     ```bash
     curl -k -u username:password https://localhost:8443/api/v1/health
     ```

4. **CSV File Issues**
   - Ensure semicolon (`;`) delimiter
   - Check file permissions
   - Verify required columns are present

### Logging

Enable verbose output for debugging:

```bash
ansible-playbook hana_backup_demo.yml -vvv
```

## Next Steps

1. **Customize CSV Data**: Update `systems.csv` with your actual HANA systems
2. **Configure SLA Variables**: Modify retention settings in the playbook
3. **Set Up Vault**: Use Ansible Vault for secure credential storage
4. **Create Custom Commands**: Extend the role with your specific backup requirements

## Security Notes

- Store sensitive credentials in Ansible Vault
- Use HTTPS with valid certificates in production
- Restrict file permissions on configuration files
- Regularly update Ansible and the collection

## Support

For issues and questions:
- Check the [main README](../README.md)
- Review the [HANA Backup Role documentation](../roles/hana_backup/README.md)
- Create an issue in the [GitHub repository](https://github.com/pcg-sap/alpaca-operator-ansible/issues)