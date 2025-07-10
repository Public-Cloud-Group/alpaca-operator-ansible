# SWM Backup New Role

## Overview

The `swm_backup_new` role is an Ansible role designed to create SLA-based ALPACA Operator commands from CSV data. It reads system information from a CSV file, maps the data to appropriate fields, and automatically creates backup commands in the ALPACA Operator based on predefined SLA configurations.

## Key Features

- **CSV Processing**: Reads and processes CSV files containing system information
- **Remote Host Support**: Automatically copies CSV files to remote hosts when needed
- **SLA-based Configuration**: Automatically applies different command configurations based on SLA levels (SLA1, SLA2, SLA3, SLA4)
- **Data Validation**: Validates CSV data integrity before processing
- **ALPACA Integration**: Uses the `alpaca_command` module to create commands in ALPACA Operator
- **Flexible Configuration**: Allows customization of SLA definitions and processing options

## CSV Format

The role expects a CSV file with the following structure:

```csv
primary_system;hdb_nw_sid;hdb_tenant;system_type;system_staging;system_sla;system_vm_type;system_vm_flavor;system_vdns;system_az;hdb_data_min;hdb_data_max;hdb_log_min;hdb_log_max;hdb_shared_min;hdb_shared_max;Instance_no
MUP;MHP;MUP;HDB;rg-sap-010msb-prod;SLA1;Standard_E32ds_v5;hdb-t-e;hdbmhpa;3;1;2;3;4;5;6;05
MUP;MHP;MUP;HDB-HA;rg-sap-010msb-prod;SLA1;Standard_E32ds_v5;hdb-t-e;hdbmhpb;2;1;2;3;4;5;6;05
```

### Column Mapping

- `hdb_nw_sid` → SystemName (for ALPACA command module)
- `system_vdns` → AgentName (for ALPACA command module)
- `system_sla` → SLA level (SLA1, SLA2, SLA3, SLA4)

### Parameter Placeholders

In SLA command parameters, the following placeholders are automatically replaced with CSV data:
- `__SYSTEM_TYPE__` → Replaced with `system_type` from CSV
- `__HDB_NW_SID__` → Replaced with `hdb_nw_sid` from CSV
- `__SYSTEM_AZ__` → Replaced with `system_az` from CSV

## SLA Definitions

The role includes four predefined SLA levels:

### SLA1 - Production
- **Description**: High-availability production systems
- **Schedule**: Hourly execution
- **Escalation**: Email alerts enabled
- **Retention**: 7 days
- **Critical**: Yes

### SLA2 - Staging
- **Description**: Staging / Pre-production systems
- **Schedule**: Every 5 minutes
- **Escalation**: Email and SMS alerts
- **Retention**: 14 days
- **Critical**: Yes

### SLA3 - Development
- **Description**: Development environment
- **Schedule**: Daily execution (weekdays only)
- **Escalation**: Email alerts only
- **Retention**: 3 days
- **Critical**: No

### SLA4 - Backup
- **Description**: Backup environment
- **Schedule**: Daily execution (weekdays only)
- **Escalation**: Email alerts only
- **Retention**: 3 days
- **Critical**: No

## Requirements

- Ansible >= 2.11
- ALPACA Operator >= 5.5.1
- `pcg.alpaca_operator` collection
- **Important**: Playbooks must have `gather_facts: true` for remote host CSV file copying

## Role Variables

### Required Variables

```yaml
# ALPACA API Configuration
ALPACA_Operator_API_Protocol: "https"        # Optional, defaults to 'https'
ALPACA_Operator_API_Port: 8443               # Optional, defaults to 8443
ALPACA_Operator_API_Username: "admin"        # Required
ALPACA_Operator_API_Password: "your_password" # Required - use vault in production
ALPACA_Operator_API_Validate_Certs: false    # Optional, defaults to false
```

### Optional Variables

```yaml
# CSV Processing Configuration
csv_processor:
  input_file: "{{ role_path }}/files/swm_prod.csv"
  delimiter: ";"
  encoding: "utf-8"
  skip_header: true

# Processing Options
processing_options:
  create_commands: true
  validate_data: true
  log_level: "info"

# Custom SLA Definitions (optional)
sla_definitions:
  "SLA1":
    name: "Production"
    description: "High-availability production systems"
    command_defaults:
      processId: 801
      parameters: "-p prod -t __SYSTEM_TYPE__ -s __HDB_NW_SID__ -az __SYSTEM_AZ__"
      # ... additional configuration
```

## Remote Host Support

The role automatically handles CSV file copying for remote hosts:

- **Local Execution**: When running on `localhost`, `127.0.0.1`, or with `connection: local`, the CSV file is used directly
- **Remote Execution**: When running on remote hosts, the CSV file is automatically copied to `/tmp/` with a unique filename
- **Automatic Cleanup**: Temporary CSV files are automatically removed after processing
- **Fact Gathering Required**: Remote host detection requires `gather_facts: true` in playbooks

### Remote Host Detection Logic

The role uses the following logic to determine if execution is on a remote host:
```yaml
is_remote_execution: "{{ inventory_hostname != 'localhost' and inventory_hostname != '127.0.0.1' and inventory_hostname != ansible_connection | default('ssh') != 'local' }}"
```

## Usage

### Basic Usage

```yaml
- name: Create SLA-based ALPACA backup commands
  hosts: alpaca_servers
  gather_facts: true  # Required for remote host CSV file copying
  roles:
    - swm_backup_new
  vars:
    ALPACA_Operator_API_Username: "admin"
    ALPACA_Operator_API_Password: "your_password"  # Use vault in production
```

### Advanced Usage with Custom SLA

```yaml
- name: Create commands with custom SLA configuration
  hosts: alpaca_servers
  gather_facts: true  # Required for remote host CSV file copying
  roles:
    - role: swm_backup_new
      vars:
        sla_definitions:
          "SLA1":
            name: "Critical Production"
            command_defaults:
              processId: 901
              parameters: "-p critical --priority high"
              schedule:
                period: "every_5min"
```

### Validation-Only Mode

```yaml
- name: Validate CSV data without creating commands
  hosts: alpaca_servers
  gather_facts: true  # Required for remote host CSV file copying
  roles:
    - role: swm_backup_new
      vars:
        processing_options:
          create_commands: false
          validate_data: true
```

## Tasks Overview

The role performs the following tasks:

1. **Configuration Validation**: Validates required variables and configuration
2. **Remote Host Detection**: Automatically detects if execution is on a remote host
3. **CSV File Copying**: Copies CSV file to remote hosts when needed (with automatic cleanup)
4. **CSV Processing**: Reads and parses the CSV file
5. **Data Validation**: Validates CSV data integrity and SLA values
6. **Command Creation**: Creates ALPACA commands based on SLA configurations
7. **Summary Reporting**: Provides detailed processing summary

## File Structure

```
roles/swm_backup_new/
├── defaults/
│   └── main.yml          # Default variables and SLA definitions
├── files/
│   └── swm_prod.csv      # Sample CSV file
├── meta/
│   └── main.yml          # Role metadata
├── tasks/
│   ├── main.yml          # Main task coordination
│   ├── process_csv.yml   # CSV processing tasks
│   ├── validate_csv.yml  # Data validation tasks
│   └── create_commands.yml # Command creation tasks
├── example_playbook.yml         # Basic usage example
├── example_advanced_playbook.yml # Advanced usage example
└── README.md                    # This file
```

## Error Handling

The role includes comprehensive error handling:

- **CSV File Validation**: Checks if CSV file exists and is readable
- **Data Validation**: Validates required fields and SLA values
- **Duplicate Detection**: Checks for duplicate system names
- **API Error Handling**: Handles ALPACA API errors gracefully
- **Rollback Support**: Provides detailed error messages for troubleshooting

## Troubleshooting

### Common Issues

1. **CSV File Not Found**
   - Ensure the CSV file exists in the `files/` directory
   - Check the `csv_processor.input_file` path

2. **Invalid SLA Values**
   - Verify SLA values are one of: SLA1, SLA2, SLA3, SLA4
   - Check for typos in the CSV file

3. **ALPACA API Connection Issues**
   - Verify API credentials and connection settings
   - Check network connectivity to ALPACA Operator

4. **Missing Required Fields**
   - Ensure all required CSV columns are present
   - Check for empty values in critical fields

### Debug Mode

Enable debug logging for detailed troubleshooting:

```yaml
processing_options:
  log_level: "debug"
```

## Examples

See the example playbooks for complete usage examples:

### Basic Usage
`example_playbook.yml` includes:
- Basic command creation with default SLA definitions
- Validation-only mode
- Inventory and vault file examples

### Advanced Usage
`example_advanced_playbook.yml` includes:
- Custom SLA configuration
- Override of default SLA definitions
- Advanced processing options
- Multiple execution modes

## License

GPL-3.0-or-later

## Author

PCG Team

## Support

For issues and questions, please contact the PCG team or create an issue in the project repository. 