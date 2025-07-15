# Dynamic Command Generator Role

## Overview

The `dynamic_command_generator` role automatically generates ALPACA command playbooks based on CSV data with SLA-based configurations. This role processes CSV files containing system information and creates individual or consolidated playbooks for ALPACA command management.

**Important**: This role processes CSV data **locally** and generates playbooks that will be executed **locally** to communicate with the ALPACA API on remote hosts. The `alpaca_command.py` module is designed to run from the Ansible control node and directly communicate with the ALPACA API on remote hosts.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CSV File      │    │  Ansible Role    │    │  Generated      │
│   (Local)       │───▶│  (Local)         │───▶│  Playbooks      │
│                 │    │                  │    │  (Local)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  ALPACA API      │
                       │  (Remote Host)   │
                       └──────────────────┘
```

### Processing Flow
1. **Local CSV Processing**: CSV file is read and processed locally
2. **Local Playbook Generation**: Command playbooks are generated locally
3. **Local Execution**: Generated playbooks are executed locally
4. **Remote API Communication**: Playbooks communicate with ALPACA API on remote hosts

## Features

- **Local CSV Processing**: CSV files are processed locally on the Ansible control node
- **SLA-based Command Configuration**: Different command settings based on SLA levels (SLA1, SLA2, SLA3, SLA4)
- **Multiple Output Formats**: Generates individual command files, consolidated playbooks, inventory, variables, and documentation
- **Flexible Configuration**: Configurable CSV processing, output options, and command parameters
- **Validation**: Comprehensive CSV data validation before processing
- **Documentation**: Auto-generated README with usage instructions

## CSV Data Mapping

The role maps the following CSV columns to ALPACA command parameters:

| CSV Column | ALPACA Parameter | Description |
|------------|------------------|-------------|
| `hdb_nw_sid` | `systemName` | System identifier for ALPACA |
| `system_vdns` | `agentName` | Agent name for command execution |
| `system_sla` | Command Configuration | Determines SLA-based command settings |
| `system_type` | Parameter Substitution | Used in command parameter templates |
| `system_az` | Parameter Substitution | Used in command parameter templates |

## SLA Command Configurations

### SLA1 (High Priority)
- **Schedule**: Every 5 minutes (log sync), Fixed time (data sync)
- **Escalation**: Email and SMS enabled
- **Critical**: Yes
- **History**: Full logging with 200 retention
- **Commands**: DB log sync, DB data sync

### SLA2 (Medium Priority)
- **Schedule**: Every 15 minutes
- **Escalation**: Email only
- **Critical**: No
- **History**: Partial logging with 100 retention
- **Commands**: DB log sync

### SLA3 (Low Priority)
- **Schedule**: Every 30 minutes
- **Escalation**: Disabled
- **Critical**: No
- **History**: Minimal logging with 50 retention
- **Commands**: DB log sync

### SLA4 (Development)
- **Schedule**: Manual execution
- **Escalation**: Disabled
- **Critical**: No
- **History**: Minimal logging with 25 retention
- **Commands**: DB log sync (disabled)

## Requirements

### Required Variables
- `ALPACA_Operator_API_Username`: ALPACA API username
- `ALPACA_Operator_API_Password`: ALPACA API password

### Optional Variables
- `ALPACA_Operator_API_Protocol`: API protocol (default: "https")
- `ALPACA_Operator_API_Port`: API port (default: 8443)
- `ALPACA_Operator_API_Validate_Certs`: TLS certificate validation (default: false)

## Usage

### Basic Usage

```yaml
- name: Generate ALPACA Commands
  hosts: localhost
  gather_facts: true
  
  vars:
    ALPACA_Operator_API_Username: "your_username"
    ALPACA_Operator_API_Password: "your_password"
    
    csv_processor:
      input_file: "path/to/your/csv/file.csv"
      delimiter: ";"
      skip_header: true
    
    output_config:
      output_dir: "{{ playbook_dir }}/generated_commands"

  tasks:
    - name: Generate commands from CSV
      include_role:
        name: dynamic_command_generator
```

### Advanced Configuration

```yaml
- name: Generate ALPACA Commands with Custom Settings
  hosts: localhost
  gather_facts: true
  
  vars:
    ALPACA_Operator_API_Username: "your_username"
    ALPACA_Operator_API_Password: "your_password"
    ALPACA_Operator_API_Protocol: "https"
    ALPACA_Operator_API_Port: 8443
    ALPACA_Operator_API_Validate_Certs: false
    
    csv_processor:
      input_file: "{{ playbook_dir }}/data/systems.csv"
      delimiter: ";"
      encoding: "utf-8"
      skip_header: true
    
    output_config:
      output_dir: "{{ playbook_dir }}/generated_commands"
      command_file_pattern: "command_{{ item.system_name | replace(' ', '_') | lower }}_{{ item.system_type | lower }}_{{ item.command_name | replace(' ', '_') | lower }}.yml"
    
    processing_options:
      generate_individual_files: true
      generate_consolidated_file: true
      generate_inventory: true
      generate_variables: true
      generate_readme: true
      validate_data: true
      log_level: "info"

  tasks:
    - name: Generate commands from CSV
      include_role:
        name: dynamic_command_generator
```

## Generated Files

The role generates the following files in the specified output directory:

### Individual Command Playbooks
- `command_{system_name}_{system_type}.yml` - Individual command playbooks for each system and command combination

### Consolidated Files
- `consolidated_commands.yml` - Single playbook containing all commands
- `inventory.ini` - ALPACA API inventory file
- `variables.yml` - Configuration variables and summary
- `README.md` - Complete documentation and usage instructions

## Running Generated Playbooks

### Individual Commands
```bash
# Run a specific command playbook
ansible-playbook -i inventory.ini command_mhp_hdb.yml
```

### Consolidated Playbook
```bash
# Run all commands at once
ansible-playbook -i inventory.ini consolidated_commands.yml
```

### With Custom Variables
```bash
# Override API credentials
ansible-playbook -i inventory.ini consolidated_commands.yml \
  -e "ALPACA_Operator_API_Username=your_username" \
  -e "ALPACA_Operator_API_Password=your_password"
```

## Configuration Options

### CSV Processor Configuration
```yaml
csv_processor:
  input_file: "path/to/csv/file.csv"  # Required: Local CSV file path
  delimiter: ";"                      # Required: CSV delimiter
  encoding: "utf-8"                   # Optional: File encoding
  skip_header: true                   # Optional: Skip header row
```

### Output Configuration
```yaml
output_config:
  output_dir: "{{ playbook_dir }}/generated_commands"  # Required: Local output directory
  command_file_pattern: "command_{{ item.system_name | replace(' ', '_') | lower }}_{{ item.system_type | lower }}.yml"  # Optional: File naming pattern
  consolidated_file: "consolidated_commands.yml"       # Optional: Consolidated file name
  inventory_file: "inventory.ini"                      # Optional: Inventory file name
  variables_file: "variables.yml"                      # Optional: Variables file name
  readme_file: "README.md"                             # Optional: README file name
```

### Processing Options
```yaml
processing_options:
  generate_individual_files: true      # Generate individual command files
  generate_consolidated_file: true     # Generate consolidated playbook
  generate_inventory: true             # Generate inventory file
  generate_variables: true             # Generate variables file
  generate_readme: true                # Generate README file
  validate_data: true                  # Validate CSV data before processing
  log_level: "info"                    # Logging level
```

## Customizing SLA Command Configurations

You can customize the SLA-based command configurations by overriding the `sla_commands` variable:

```yaml
sla_commands:
  SLA1:
    commands:
      - name: "Custom Command Name"
        processId: 801
        parameters: "Custom parameters with {{ system_type }} and {{ hdb_nw_sid }}"
        schedule:
          period: "every_5min"
          time: "00:00:00"
          cronExpression: ""
          daysOfWeek: ["monday", "tuesday", "wednesday", "thursday", "friday"]
        parametersNeeded: false
        disabled: false
        critical: true
        autoDeploy: false
        history:
          documentAllRuns: true
          retention: 200
        timeout:
          type: "default"
          value: 30
        escalation:
          mailEnabled: true
          smsEnabled: false
          mailAddress: "monitoring@example.com"
          smsAddress: ""
          minFailureCount: 1
          triggers:
            everyChange: true
            toRed: true
            toYellow: false
            toGreen: false
```

## CSV File Format

The CSV file should have the following columns (in order):

1. `primary_system` - Primary system identifier
2. `hdb_nw_sid` - HDB system ID (maps to systemName)
3. `hdb_tenant` - HDB tenant
4. `system_type` - System type (HDB, ASCS, PAI, etc.)
5. `system_staging` - System staging environment
6. `system_sla` - SLA level (SLA1, SLA2, SLA3, SLA4)
7. `system_vm_type` - VM type
8. `system_vm_flavor` - VM flavor
9. `system_vdns` - System DNS name (maps to agentName)
10. `system_az` - System availability zone
11. `hdb_data_min` - HDB data minimum
12. `hdb_data_max` - HDB data maximum
13. `hdb_log_min` - HDB log minimum
14. `hdb_log_max` - HDB log maximum
15. `hdb_shared_min` - HDB shared minimum
16. `hdb_shared_max` - HDB shared maximum
17. `Instance_no` - Instance number

Example CSV line:
```
MUP;MHP;MUP;HDB;rg-sap-010msb-prod;SLA1;Standard_E32ds_v5;hdb-t-e;hdbmhpa;3;1;2;3;4;5;6;05
```

## Local Processing Benefits

- **No Remote File Transfer**: CSV files are processed locally, no need to copy files to remote hosts
- **Direct API Communication**: Generated playbooks communicate directly with ALPACA API on remote hosts
- **Simplified Architecture**: All processing happens on the Ansible control node
- **Better Security**: No sensitive CSV data is transferred to remote hosts
- **Faster Execution**: No file transfer overhead

## Troubleshooting

### Common Issues

1. **CSV file not found**: Ensure the `csv_processor.input_file` path is correct and file exists locally
2. **Invalid SLA values**: Only SLA1, SLA2, SLA3, SLA4 are supported
3. **Missing required columns**: Ensure all required CSV columns are present
4. **API authentication failed**: Verify ALPACA API credentials and network connectivity to remote hosts

### Debug Mode

Enable debug output by setting the log level:

```yaml
processing_options:
  log_level: "debug"
```

### Validation Errors

The role performs comprehensive validation and will fail with descriptive error messages if:
- CSV data is malformed
- Required columns are missing
- SLA values are invalid
- Command configurations are missing

## Dependencies

- Ansible 2.12 or higher
- ALPACA Operator collection (`pcg.alpaca_operator`)
- Python CSV processing capabilities
- Network connectivity to ALPACA API hosts

## License

This role is part of the ALPACA Operator Ansible collection and follows the same licensing terms. 