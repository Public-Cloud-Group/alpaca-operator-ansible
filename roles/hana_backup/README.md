# HANA Backup Role

## Overview

The `hana_backup` role is designed to automate the creation and management of SAP HANA backup commands in ALPACA Operator systems. This role reads system information from a CSV file and creates standardized commands for each system based on their Service Level Agreement (SLA) classification.

The role leverages the `pcg.alpaca_operator.alpaca_command` module to create and manage commands in ALPACA Operator, ensuring consistent backup configurations across multiple systems.

## Quick Start

### Basic Example

```yaml
---
- name: Configure HANA Backup Commands
  hosts: localhost
  gather_facts: false

  vars:
    csv_file: "/path/to/your/systems.csv"
    ALPACA_Operator_API_Host: "alpaca.example.com"
    ALPACA_Operator_API_Protocol: "https"
    ALPACA_Operator_API_Port: 8443
    ALPACA_Operator_API_Username: "admin"
    ALPACA_Operator_API_Password: "{{ vault_alpaca_password }}"
    ALPACA_Operator_API_Validate_Certs: true

  roles:
    - hana_backup
```

## Requirements

- Python >= 3.8
- Ansible >= 2.12
- ALPACA Operator >= 5.6.0
- CSV file containing system information

## How It Works

### Basic Concept

1. **CSV Input**: The role reads system information from a CSV file
2. **SLA Classification**: Each system is assigned a Service Level Agreement (SLA)
3. **Command Generation**: Based on the SLA, appropriate backup commands are created
4. **ALPACA Integration**: Commands are created/updated in ALPACA Operator

### Parameter Mapping

The role uses the same parameter structure as the `pcg.alpaca_operator.alpaca_command` module. All parameters under the `command` key in the role defaults correspond directly to the module's `command` parameter:

```yaml
# Role defaults structure
command_defaults:
  state: present
  schedule:
    period: fixed_time
    time: "12:12:12"
  parametersNeeded: true
  disabled: false
  # ... other parameters

# Maps to alpaca_command module
pcg.alpaca_operator.alpaca_command:
  system:
    systemName: "{{ system.systemName }}"
  command:
    state: present  # From command_defaults
    schedule:       # From command_defaults
      period: fixed_time
      time: "12:12:12"
    parametersNeeded: true  # From command_defaults
    disabled: false         # From command_defaults
    # ... other parameters
```

## Input Data

### CSV File Format

The role expects a CSV file with semicolon (`;`) as the delimiter. The following columns are required:

#### Required Columns

| Column Name      | Description                | Example                        |
| ---------------- | -------------------------- | ------------------------------ |
| `hdb_nw_sid`     | System ID/Name             | `HDB`                          |
| `system_vdns`    | Agent hostname             | `agent01.example.com`          |
| `system_sla`     | Service Level Agreement    | `SLA1`, `SLA2`, `SLA3`, `SLA4` |
| `system_type`    | System type classification | `PROD`, `TEST`, `DEV`          |
| `system_staging` | Staging environment        | `PROD`, `STAGE`, `DEV`         |
| `Instance_no`    | HANA instance number       | `00`, `01`, `02`               |

#### Example CSV Content

```csv
hdb_nw_sid;system_vdns;system_sla;system_type;system_staging;Instance_no
MHP;SLA1;hdbmhpa;rg-sap-010msb-prod;05
MHP;SLA1;hdbmhpb;rg-sap-010msb-prod;05
```

## Default Configuration

### Standard Commands

The role includes a predefined set of commands in `defaults/main.yml`:

1. **HANA BACKUP LOG** - Log backup operations
2. **HANA RESTORE FILE** - File-based restore operations
3. **HANA RESTORE SNAP** - Snapshot-based restore operations
4. **HANA BACKUP SNAP** - Snapshot backup operations
5. **HANA BACKUP FILE DAILY** - Daily file backup operations
6. **HANA BACKUP FILE MONTHLY** - Monthly file backup operations
7. **HANA BACKUP FILE YEARLY** - Yearly file backup operations
8. **FS BACKUP INCR** - Incremental filesystem backup
9. **FS BACKUP FULL 2** - Full filesystem backup

### Service Level Agreements

The role supports four predefined SLA levels (SLA1-SLA4), each with different retention variables:

- `local_file_ret` - Local file retention
- `local_snap_ret` - Local snapshot retention
- `local_log_ret` - Local log retention
- `blob_log_ret` - Blob log retention
- `blob_file_ret` - Blob file retention
- `blob_file_ret_monthly` - Monthly blob file retention
- `blob_file_ret_yearly` - Yearly blob file retention

## Role Variables

### Required Variables

| Variable   | Type   | Description                                        |
| ---------- | ------ | -------------------------------------------------- |
| `csv_file` | string | Path to the CSV file containing system information |

### Optional Variables

| Variable   | Type | Default | Description                                                          |
| ---------- | ---- | ------- | -------------------------------------------------------------------- |
| `override` | dict | `{}`    | Dictionary to override role defaults (see Advanced Configuration section) |

### ALPACA Operator API Variables

The following variables must be defined in your inventory or playbook for API connectivity:

| Variable                             | Type    | Description                          |
| ------------------------------------ | ------- | ------------------------------------ |
| `ALPACA_Operator_API_Host`           | string  | ALPACA Operator server hostname      |
| `ALPACA_Operator_API_Protocol`       | string  | API protocol (http/https)            |
| `ALPACA_Operator_API_Port`           | integer | API port number                      |
| `ALPACA_Operator_API_Username`       | string  | API username                         |
| `ALPACA_Operator_API_Password`       | string  | API password                         |
| `ALPACA_Operator_API_Validate_Certs` | boolean | Whether to validate SSL certificates |

## Advanced Configuration

### Override Behavior

The role supports overriding defaults through the `override` variable in your playbook. The override uses Ansible's `combine` filter with `recursive=True` for merging.

#### Parameter Value Prioritization

The role follows a specific priority order when merging parameter values. Values are merged in the following order (later values override earlier ones):

1. **Role Defaults** (`defaults/main.yml`) - Base configuration
2. **Playbook Override** (`override`) - Global overrides from playbook
3. **SLA Command Defaults** (`service_levels[SLA].command_defaults`) - SLA-specific defaults
4. **Individual Command Definition** (`commands[]` or `service_levels[SLA].commands[]`) - Command-specific settings

**Example of Priority Order**:
```yaml
# Role defaults (lowest priority)
role_defaults:
  command_defaults:
    critical: false
    timeout:
      type: custom
      value: 4000

# Playbook override (overrides role defaults)
override:
  command_defaults:
    critical: true  # This overrides the role default
  service_levels:
    SLA1:
      command_defaults:
        critical: false  # This overrides the playbook override for SLA1
        timeout:
          value: 6000    # This overrides the role default timeout
      commands:
        - name: "HANA BACKUP LOG"
          critical: true  # This overrides SLA defaults for this specific command
```

**Result**: The "HANA BACKUP LOG" command will have `critical: true` (highest priority), while other SLA1 commands will have `critical: false`.

#### Override Structure

```yaml
override:
  command_defaults:
    # Override global command defaults
    critical: true
    timeout:
      type: custom
      value: 6000
  commands:
    # Override or add commands
    - name: "CUSTOM BACKUP"
      processCentralId: 8990048
      parameters: "-s { systemName } -d /backup"
  service_levels:
    SLA1:
      variables:
        # Override SLA variables
        local_file_ret: "30"
      command_defaults:
        # Override SLA-specific command defaults
        critical: true
      commands:
        # Override SLA-specific commands
        - name: "SLA1 CUSTOM COMMAND"
          processCentralId: 8990048
```

#### Dictionary and List Behavior

**Important**: When overriding dictionaries that contain lists (such as `commands` or `daysOfWeek`), the entire list is replaced, not merged. This means:

- If you define `commands` in your override, it will completely replace the default command set
- If you define `daysOfWeek` in a schedule override, it will replace the default days
- To extend rather than replace, you must include all desired items in your override

**Example of List Replacement**:
```yaml
# This will REPLACE the default commands, not add to them
override:
  commands:
    - name: "CUSTOM COMMAND"
      processCentralId: 8990048

# This will REPLACE the default days, not add to them
override:
  command_defaults:
    schedule:
      daysOfWeek:
        - monday
        - friday
```

### SLA Level Customization

The role supports dynamic SLA level management through the `override` variable. You can add new SLA levels, modify existing ones, or completely replace the default SLA structure.

#### Adding New SLA Levels

You can add custom SLA levels beyond the default SLA1-SLA4:

```yaml
override:
  service_levels:
    SLA5:  # New SLA level
      variables:
        local_file_ret: "<CZ_LOCAL_FILE_RET_CLASS_5>"
        local_snap_ret: "<CZ_LOCAL_SNAP_RET_CLASS_5>"
        local_log_ret: "<CZ_LOCAL_LOG_RET_CLASS_5>"
        blob_log_ret: "<CZ_BLOB_LOG_RET_CLASS_5>"
        blob_file_ret: "<CZ_BLOB_FILE_RET_CLASS_5>"
        blob_file_ret_monthly: "<CZ_BLOB_FILE_RET_MONTHLY_CLASS_5>"
        blob_file_ret_yearly: "<CZ_BLOB_FILE_RET_YEARLY_CLASS_5>"
      command_defaults:
        critical: true
        timeout:
          type: custom
          value: 8000
      commands:
        - name: "SLA5 CUSTOM BACKUP"
          processCentralId: 8990048
          parameters: "-s { systemName } -d /backup/sla5 -r 30"
```

#### Modifying Existing SLA Levels

You can override specific settings for existing default SLA levels:

```yaml
override:
  service_levels:
    SLA1:
      variables:
        local_file_ret: "60"  # Override default value
        blob_file_ret: "365"  # Override default value
      command_defaults:
        critical: true
        schedule:
          period: fixed_time
          time: "01:00:00"
      commands:
        - name: "SLA1 ENHANCED BACKUP"
          processCentralId: 8990048
          parameters: "-s { systemName } -d /backup/enhanced"
```

#### Custom SLA Structure

You can create completely custom SLA structures with meaningful names:

```yaml
override:
  service_levels:
    PROD_CRITICAL:
      variables:
        local_file_ret: "90"
        local_snap_ret: "30"
        blob_file_ret: "1095"
      command_defaults:
        critical: true
        disabled: false
    DEV_TEST:
      variables:
        local_file_ret: "7"
        local_snap_ret: "3"
        blob_file_ret: "30"
      command_defaults:
        critical: false
        disabled: true
```

#### CSV Requirements for Custom SLA Levels

When using custom SLA levels, ensure your CSV file includes the new SLA values in the `system_sla` column:

```csv
hdb_nw_sid;system_vdns;system_sla;system_type;system_staging;Instance_no
MHP;SLA5;hdbmhpa;rg-sap-010msb-prod;05
MHP;PROD_CRITICAL;hdbmhpb;rg-sap-010msb-prod;05
MHP;DEV_TEST;hdbmhpc;rg-sap-010msb-prod;05
```

**Important Notes**:
- The role dynamically accesses SLA definitions using `merged_definitions.service_levels[csv.systemSla]`
- If an SLA level is not found in the configuration, the role will use empty defaults
- Variable substitution (`{ variable_name }`) works automatically for all SLA variables
- You can completely replace the default SLA structure by defining all desired SLA levels in your override

## Advanced Example Playbook

```yaml
---
- name: Configure HANA Backup Commands with Custom Configuration
  hosts: localhost
  gather_facts: false

  vars:
    csv_file: "/path/to/your/systems.csv"
    ALPACA_Operator_API_Host: "alpaca.example.com"
    ALPACA_Operator_API_Protocol: "https"
    ALPACA_Operator_API_Port: 8443
    ALPACA_Operator_API_Username: "admin"
    ALPACA_Operator_API_Password: "{{ vault_alpaca_password }}"
    ALPACA_Operator_API_Validate_Certs: true

    # Advanced configuration
    override:
      command_defaults:
        critical: true
        timeout:
          type: custom
          value: 6000
      service_levels:
        SLA1:
          command_defaults:
            schedule:
              period: fixed_time
              time: "02:00:00"
        SLA5:  # Custom SLA level
          variables:
            local_file_ret: "90"
            blob_file_ret: "1095"
          command_defaults:
            critical: true
            timeout:
              type: custom
              value: 8000

  roles:
    - hana_backup
```

## Role Tasks

1. **CSV Validation** - Checks if the CSV file exists and is accessible
2. **CSV Processing** - Reads and parses the CSV file using Python
3. **Configuration Merging** - Merges role defaults with playbook overrides
4. **Command Generation** - Iterates through CSV rows and generates commands
5. **ALPACA Integration** - Creates/updates commands using the `alpaca_command` module

## Dependencies

This role depends on the `pcg.alpaca_operator` collection, specifically the `alpaca_command` module.

## Return Values

The role does not return specific values but creates/updates ALPACA Operator commands for each system defined in the CSV file.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

## Support

For issues and questions related to this role, please refer to the ALPACA Operator documentation or create an issue in the project repository.
