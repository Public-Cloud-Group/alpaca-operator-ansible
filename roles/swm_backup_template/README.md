# SWM Backup Template Role

A template-based Ansible role for generating ALPACA Operator commands from CSV data using Jinja2 templates.

## Overview

This role processes CSV files containing system information and generates multiple output files using Jinja2 templates:

- **Individual command playbooks** for each system
- **Consolidated playbook** containing all commands
- **Ansible inventory** with SLA-based groups
- **Variables file** with system-specific data
- **README documentation** with generation details

## Key Differences from Direct API Role

| Aspect | Direct API Role | Template Role |
|--------|----------------|---------------|
| **Output** | Direct API calls | Generated files |
| **Complexity** | Simple, single-purpose | Complex, multi-output |
| **Flexibility** | Limited to API execution | Multiple output formats |
| **Maintenance** | Easy to maintain | More files to manage |
| **Use Case** | Immediate execution | File generation for later use |

## Role Structure

```
roles/swm_backup_template/
├── defaults/
│   └── main.yml              # Default configuration
├── tasks/
│   ├── main.yml              # Main coordination tasks
│   ├── process_csv.yml       # CSV data processing
│   ├── validate_csv.yml      # Data validation
│   ├── generate_individual_commands.yml  # Individual file generation
│   ├── generate_consolidated_file.yml    # Consolidated file generation
│   ├── generate_inventory.yml            # Inventory generation
│   ├── generate_variables.yml            # Variables generation
│   └── generate_readme.yml               # README generation
├── templates/
│   ├── command_template.yml.j2           # Individual command template
│   ├── consolidated_template.yml.j2      # Consolidated playbook template
│   ├── inventory_template.ini.j2         # Inventory template
│   ├── variables_template.yml.j2         # Variables template
│   └── README_template.md.j2             # README template
├── files/
│   └── swm_prod.csv                      # Sample CSV file
├── meta/
│   └── main.yml              # Role metadata
├── example_playbook.yml      # Usage examples
└── README.md                 # This documentation
```

## Requirements

- Ansible 2.12 or higher
- ALPACA Operator collection: `pcg.alpaca_operator`
- CSV file with system data
- ALPACA API credentials

## CSV Format

The role expects a semicolon-delimited CSV file with the following columns:

```csv
primary_system;hdb_nw_sid;hdb_tenant;system_type;system_staging;system_sla;system_vm_type;system_vm_flavor;system_vdns;system_az;hdb_data_min;hdb_data_max;hdb_log_min;hdb_log_max;hdb_shared_min;hdb_shared_max;Instance_no
```

### Column Mapping

| Column | Index | Description | Maps to |
|--------|-------|-------------|---------|
| `primary_system` | 0 | Primary system identifier | - |
| `hdb_nw_sid` | 1 | HDB system ID | SystemName |
| `hdb_tenant` | 2 | HDB tenant | - |
| `system_type` | 3 | System type | Parameter placeholder |
| `system_staging` | 4 | Staging information | - |
| `system_sla` | 5 | SLA level (SLA1-SLA4) | SLA configuration |
| `system_vm_type` | 6 | VM type | - |
| `system_vm_flavor` | 7 | VM flavor | - |
| `system_vdns` | 8 | System DNS | AgentName |
| `system_az` | 9 | Availability zone | Parameter placeholder |

## Configuration

### Default Variables

```yaml
# CSV Processing
csv_processor:
  input_file: "{{ role_path }}/files/swm_prod.csv"
  delimiter: ";"
  encoding: "utf-8"
  skip_header: true

# Output Configuration
output_config:
  output_dir: "{{ playbook_dir }}/generated"
  command_file_pattern: "command_{{ item.system_name | replace(' ', '_') | lower }}.yml"
  consolidated_file: "consolidated_commands.yml"
  inventory_file: "inventory.ini"
  variables_file: "variables.yml"
  readme_file: "README.md"

# Processing Options
processing_options:
  generate_individual_files: true
  generate_consolidated_file: true
  generate_inventory: true
  generate_variables: true
  generate_readme: true
  validate_data: true
  log_level: "info"
```

### Required Variables

```yaml
# ALPACA API Configuration
ALPACA_Operator_API_Username: "your_username"
ALPACA_Operator_API_Password: "your_password"
ALPACA_Operator_API_Protocol: "https"  # Optional, defaults to https
ALPACA_Operator_API_Port: 8443         # Optional, defaults to 8443
ALPACA_Operator_API_Validate_Certs: false  # Optional, defaults to false

# SLA Definitions
sla_definitions:
  "SLA1":
    name: "Production"
    command_defaults:
      processId: 801
      parameters: "-p prod -t __SYSTEM_TYPE__ -s __HDB_NW_SID__ -az __SYSTEM_AZ__"
      # ... additional configuration
```

## Usage

### Basic Usage

```yaml
---
- name: Generate ALPACA Commands from CSV
  hosts: local
  gather_facts: true
  vars:
    ALPACA_Operator_API_Username: "pms*"
    ALPACA_Operator_API_Password: "pms"
    sla_definitions:
      "SLA1":
        name: "Production"
        command_defaults:
          processId: 801
          parameters: "-p prod -t __SYSTEM_TYPE__ -s __HDB_NW_SID__ -az __SYSTEM_AZ__"
          # ... additional configuration

  tasks:
    - name: Execute SWM Backup Template Role
      include_role:
        name: swm_backup_template
```

### Advanced Usage

```yaml
---
- name: Generate ALPACA Commands with Custom Configuration
  hosts: local
  gather_facts: true
  vars:
    ALPACA_Operator_API_Username: "pms*"
    ALPACA_Operator_API_Password: "pms"
    sla_definitions:
      # ... SLA definitions

  tasks:
    - name: Execute SWM Backup Template Role with Custom Settings
      include_role:
        name: swm_backup_template
      vars:
        output_config:
          output_dir: "{{ playbook_dir }}/custom_generated"
          command_file_pattern: "custom_command_{{ item.system_name | replace(' ', '_') | lower }}.yml"
        processing_options:
          generate_individual_files: true
          generate_consolidated_file: false
          generate_inventory: true
          generate_variables: true
          generate_readme: true
          validate_data: true
          log_level: "debug"
```

## Generated Output

### Individual Command Files

For each system in the CSV, a separate playbook is generated:

```yaml
# command_prd01.yml
---
- name: Create ALPACA Command for PRD01
  hosts: alpaca-server
  gather_facts: false
  
  vars:
    ALPACA_Operator_API_Protocol: "https"
    ALPACA_Operator_API_Port: 8443
    ALPACA_Operator_API_Username: "pms*"
    ALPACA_Operator_API_Password: "pms"
    ALPACA_Operator_API_Validate_Certs: false

  tasks:
    - name: Create Production Backup Command - PRD01
      pcg.alpaca_operator.alpaca_command:
        system:
          systemName: "PRD01"
        command:
          name: "Production Backup Command - PRD01"
          state: present
          agentName: "prd01.example.com"
          processId: 801
          parameters: "-p prod -t HANA -s PRD01 -az eu-west-1a"
          # ... additional configuration
```

### Consolidated Playbook

A single playbook containing all commands:

```yaml
# consolidated_commands.yml
---
- name: Create ALPACA Commands for All Systems
  hosts: alpaca-server
  gather_facts: false
  
  tasks:
    - name: Create Production Backup Command - PRD01
      pcg.alpaca_operator.alpaca_command:
        # ... command configuration
    
    - name: Create Staging Backup Command - STG01
      pcg.alpaca_operator.alpaca_command:
        # ... command configuration
```

### Inventory File

```ini
# inventory.ini
[alpaca_operator]
alpaca-server

[alpaca_operator:vars]
ALPACA_Operator_API_Protocol=https
ALPACA_Operator_API_Port=8443
ALPACA_Operator_API_Username=pms*
ALPACA_Operator_API_Password=pms
ALPACA_Operator_API_Validate_Certs=false

[sla1_production]
alpaca-server  # PRD01 - HANA

[sla2_staging]
alpaca-server  # STG01 - HANA
```

### Variables File

```yaml
# variables.yml
---
# ALPACA API Configuration
ALPACA_Operator_API_Protocol: https
ALPACA_Operator_API_Port: 8443
ALPACA_Operator_API_Username: pms*
ALPACA_Operator_API_Password: pms
ALPACA_Operator_API_Validate_Certs: false

# System-specific variables
prd01_system_name: PRD01
prd01_agent_name: prd01.example.com
prd01_system_type: HANA
prd01_hdb_nw_sid: PRD01
prd01_system_az: eu-west-1a
prd01_system_sla: SLA1

# SLA Group Variables
sla1_systems:
  - PRD01

sla2_systems:
  - STG01

# Summary Statistics
total_systems: 2
sla1_count: 1
sla2_count: 1
```

## Template Features

### Jinja2 Template Capabilities

The role leverages Jinja2 templates for:

- **Dynamic content generation** based on CSV data
- **Conditional logic** for different SLA levels
- **Loop processing** for multiple systems
- **Variable substitution** with placeholders
- **Formatting and structure** control

### Template Variables

Available variables in templates:

- `csv_data`: List of all CSV rows
- `sla_definitions`: SLA configuration
- `alpaca_api`: API connection details
- `csv_row`: Current row data (in individual templates)
- `generation_timestamp`: Generation timestamp

### Placeholder Replacement

Templates support the same placeholder system as the direct API role:

- `__SYSTEM_TYPE__` → Replaced with `system_type` from CSV
- `__HDB_NW_SID__` → Replaced with `hdb_nw_sid` from CSV
- `__SYSTEM_AZ__` → Replaced with `system_az` from CSV

## Execution

### Generate Files

```bash
# Generate all files
ansible-playbook -i localhost, example_playbook.yml

# Generate with custom inventory
ansible-playbook -i custom_inventory.ini example_playbook.yml
```

### Execute Generated Commands

```bash
# Execute individual command
ansible-playbook -i generated/inventory.ini generated/command_prd01.yml

# Execute all commands
ansible-playbook -i generated/inventory.ini generated/consolidated_commands.yml

# Execute by SLA group
ansible-playbook -i generated/inventory.ini generated/consolidated_commands.yml --limit sla1_production
```

## Comparison with Direct API Role

### Template Role Advantages

✅ **Multiple output formats**: Generates various file types
✅ **Flexible execution**: Files can be executed independently
✅ **Documentation**: Auto-generates README and documentation
✅ **Inventory management**: Creates SLA-based inventory groups
✅ **Variable extraction**: Generates variables file for reference
✅ **Template customization**: Jinja2 templates can be modified

### Template Role Disadvantages

❌ **Higher complexity**: More files and configuration
❌ **Two-step process**: Generate files, then execute
❌ **File management**: Need to manage generated files
❌ **Template maintenance**: Templates require maintenance
❌ **Learning curve**: Jinja2 template syntax required

### When to Use Template Role

- **Complex deployments** requiring multiple file formats
- **Documentation needs** with auto-generated README
- **Selective execution** by SLA groups
- **Audit requirements** with generated files
- **Template customization** needs
- **Team collaboration** with shared generated files

### When to Use Direct API Role

- **Simple execution** with immediate API calls
- **Minimal complexity** requirements
- **Direct control** over API execution
- **Real-time processing** without file generation
- **Resource constraints** (less disk space needed)

## Troubleshooting

### Common Issues

1. **Template syntax errors**: Check Jinja2 syntax in templates
2. **File permissions**: Ensure write permissions for output directory
3. **CSV format issues**: Verify CSV delimiter and column mapping
4. **API connection**: Check ALPACA API credentials and connectivity

### Debug Mode

Enable debug logging:

```yaml
processing_options:
  log_level: "debug"
```

### Validation

The role includes comprehensive validation:

- CSV data structure validation
- Required field validation
- SLA value validation
- Duplicate system detection

## Contributing

When modifying templates:

1. Test with sample CSV data
2. Verify generated file syntax
3. Check template variable availability
4. Update documentation for new features

## License

MIT License - see LICENSE file for details. 