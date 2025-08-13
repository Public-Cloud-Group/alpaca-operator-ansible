# HANA Backup Role

## Overview

The `hana_backup` role automates the creation and management of SAP HANA backup commands in ALPACA Operator systems. This role reads system information from a CSV file and creates standardized commands for each system based on their Service Level Agreement (SLA) classification.

The role leverages the `pcg.alpaca_operator.alpaca_system` and `pcg.alpaca_operator.alpaca_command` modules to create and manage systems and commands in ALPACA Operator, ensuring consistent backup configurations across multiple systems.

## Requirements

- Python >= 3.8
- Ansible >= 2.12
- ALPACA Operator >= 5.6.0
- CSV file containing system information

## How It Works

### Basic Concept

1. **CSV Input**: The role reads system information from a CSV file with semicolon (`;`) delimiter
2. **CSV Filtering**: Optional filtering of CSV rows based on column name and expected value
3. **SLA Classification**: Each system is assigned a Service Level Agreement (SLA)
4. **Command Generation**: Based on the SLA, appropriate backup commands are created
5. **ALPACA Integration**: Systems and commands are created/updated using the `alpaca_system` and `alpaca_command` modules

### Parameter Mapping

The role uses the same parameter structure as the `pcg.alpaca_operator.alpaca_command` module. All parameters under the `command` key in the role defaults correspond directly to the module's `command` parameter.

## Input Data

### CSV File Format

The role expects a CSV file with semicolon (`;`) as the delimiter.

#### Available CSV Variables

The role automatically maps CSV columns to variables that can be used in command parameters. These variables must be enclosed in **single** curly braces `{ variableName }`:

| CSV Column            | Variable Name          | Description                        | Example Value          |
| --------------------- | ---------------------- | ---------------------------------- | ---------------------- |
| `primary_system`      | `{ primarySystem }`    | Primary system identifier          | `"MUP"`                |
| `hdb_nw_sid`          | `{ systemName }`       | HANA system SID                    | `"MHP"`                |
| `hdb_tenant`          | `{ hdbTenant }`        | HANA tenant                        | `"MUP"`                |
| `system_vdns`         | `{ agentName }`        | Agent name (used as default agent) | `"hdbmhpa"`            |
| `system_sla`          | `{ systemSla }`        | Service Level Agreement            | `"SLA2"`               |
| `system_type`         | `{ systemType }`       | System type                        | `"HDB"`                |
| `system_staging`      | `{ systemStaging }`    | System staging environment         | `"rg-sap-010msb-prod"` |
| `system_vm_type`      | `{ systemVmType }`     | VM type                            | `"Standard_E32ds_v5"`  |
| `system_vm_flavor`    | `{ systemVmFlavor }`   | VM flavor                          | `"hdb-t-e"`            |
| `system_az`           | `{ systemAz }`         | Availability zone                  | `"3"`                  |
| `hdb_data_min`        | `{ hdbDataMin }`       | HANA data minimum                  | `"1"`                  |
| `hdb_data_max`        | `{ hdbDataMax }`       | HANA data maximum                  | `"2"`                  |
| `hdb_log_min`         | `{ hdbLogMin }`        | HANA log minimum                   | `"3"`                  |
| `hdb_log_max`         | `{ hdbLogMax }`        | HANA log maximum                   | `"4"`                  |
| `hdb_shared_min`      | `{ hdbSharedMin }`     | HANA shared minimum                | `"5"`                  |
| `hdb_shared_max`      | `{ hdbSharedMax }`     | HANA shared maximum                | `"6"`                  |
| `Instance_no`         | `{ instanceNo }`       | Instance number                    | `"05"`                 |
| `alpaca_ext_pool_old` | `{ alpacaExtPoolOld }` | N/A                                | `"ag10_bkp001"`        |
| `alpaca_ext_pool_new` | `{ alpacaExtPoolNew }` | N/A                                | `"ag10_bkp101"`        |
| `backupshare`         | `{ backupShare }`      | N/A                                | `"bkp004"`             |
| `MagicNumber2`        | `{ magicNumber2 }`     | N/A                                | `"6"`                  |

**⚠️ IMPORTANT**: CSV variables must be enclosed in **single** curly braces `{ variableName }` when used in command parameters.

### CSV Filtering

The role supports filtering CSV rows based on column name and expected value. This is useful for processing only specific systems or SLA levels.

#### Filter Configuration

```yaml
override:
  csv_defaults:
    filter:
      enabled: true               # Enable or disable CSV filtering
      column_name: "system_type"  # Name of the column to filter on
      expected_value: "HDB*"      # Expected value (supports wildcards)
```

#### Wildcard Support

The filtering supports wildcards for flexible matching:

- `*` - Matches any sequence of characters (zero or more)
- `?` - Matches any single character

#### Filtering Examples

```yaml
# Exact match examples
override:
  csv_defaults:
    filter:
      enabled: true
      column_name: "system_type"
      expected_value: "HDB"       # Exact match for HDB systems

override:
  csv_defaults:
    filter:
      enabled: true
      column_name: "hdb_nw_sid"
      expected_value: "MHP"       # Exact match for specific system

# Wildcard filtering examples
override:
  csv_defaults:
    filter:
      enabled: true
      column_name: "system_sla"
      expected_value: "SLA*"      # All SLA levels (SLA1, SLA2, SLA3, SLA4)

override:
  csv_defaults:
    filter:
      enabled: true
      column_name: "hdb_nw_sid"
      expected_value: "M*"        # All systems starting with M (MHP, MUP, etc.)

override:
  csv_defaults:
    filter:
      enabled: true
      column_name: "hdb_nw_sid"
      expected_value: "*HP*"      # Systems containing "HP" anywhere

override:
  csv_defaults:
    filter:
      enabled: true
      column_name: "hdb_nw_sid"
      expected_value: "MH*"       # Systems starting with "MH"

override:
  csv_defaults:
    filter:
      enabled: true
      column_name: "system_type"
      expected_value: "H??"       # System types with exactly 3 characters starting with "H"
```

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

### System Variables Example

```yaml
---
- name: HANA Backup with System Variables
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

    # Define system-specific variables
    system_variables:
      MHP:
        - name: "<BKP_DATA_DEST1>"
          value: "1"
        - name: "<BKP_DATA_DEST2>"
          value: "2"
        - name: "<BKP_LB_DATA_01>"
          value: "backup-container-mhp"
        - name: "<BKP_LB_LOG_01>"
          value: "log-container-mhp"
        - name: "<HANA_SYS_NR>"
          value: "05"
        - name: "<HANA_DB_SID>"
          value: "MHP"
        - name: "<HANA_VHOST>"
          value: "hdbmhpa"

  roles:
    - hana_backup
```

## Comprehensive Configuration

### Complete Example with Override

```yaml
---
- name: HANA Backup with Full Configuration
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

    # Define system variables
    system_variables:
      MHP:
        - name: "<BKP_DATA_DEST1>"
          value: "1"
        - name: "<BKP_DATA_DEST2>"
          value: "2"
        - name: "<BKP_LB_DATA_01>"
          value: "backup-container-mhp"
        - name: "<BKP_LB_LOG_01>"
          value: "log-container-mhp"
        - name: "<HANA_SYS_NR>"
          value: "05"
        - name: "<HANA_DB_SID>"
          value: "MHP"
        - name: "<HANA_VHOST>"
          value: "hdbmhpa"
        - name: "<BKP_DATA_DEST1_MONTHLY>"
          value: "monthly-backup-mhp"
        - name: "<BKP_DATA_DEST1_YEARLY>"
          value: "yearly-backup-mhp"
        - name: "<BKP_LB_FS_01>"
          value: "fs-backup-mhp"

    # Override configuration
    override:
      csv_defaults:
        filter:
          enabled: true
          column_name: "system_type"
          expected_value: "HDB*"

      command_defaults:
        state: present
        schedule:
          period: fixed_time
          time: "02:00:00"
          daysOfWeek:
            - monday
            - tuesday
            - wednesday
            - thursday
            - friday
            - saturday
            - sunday
        parametersNeeded: true
        disabled: false
        critical: false
        history:
          documentAllRuns: true
          retention: 200
        autoDeploy: false
        timeout:
          type: custom
          value: 4000
        escalation:
          mailEnabled: true
          smsEnabled: true
          mailAddress: "monitoring@pcg.io"
          smsAddress: "0123456789"
          minFailureCount: 1
          triggers:
            everyChange: true
            toRed: true
            toYellow: true
            toGreen: true

      commands:
        - name: "HANA BACKUP LOG"
          processCentralId: 8990048
          parameters: "-s <HANA_DB_SID> -n 4 -e blob -o <BKP_LB_LOG_01> -z $SKEY -r { blob_log_ret } -k { local_log_ret } -y -"
        - name: "HANA RESTORE FILE"
          processCentralId: 8990048
          parameters: "-q <HANA_DB_SID> -w <HANA_VHOST> -e <HANA_DB_SID> -j 1 -t AUTO -k 2021-06-16.10:00:00 -l <BKP_DATA_DEST1>/restore -g SYSTEMDB,<HANA_DB_SID>!<HANA_DB_SID> -A xxxx -Q 1 -T 0 -J BACKUP -W <HANA_VHOST> -X { systemName } -E 2 -B <BKP_LB_DATA_01> -P $SKEY -U -"
        - name: "HANA RESTORE SNAP"
          processCentralId: 8990048
          parameters: "-q <HANA_DB_SID> -w <HANA_VHOST> -e <HANA_DB_SID> -j 0 -t AUTO -k 2021-06-16.10:00:00 -l <BKP_DATA_DEST1>/restore -g SYSTEMDB,<HANA_DB_SID>!<HANA_DB_SID> -A xxxx -Q 1 -T 0 -J BACKUP -W <HANA_VHOST> -X { systemName } -E 2 -B <BKP_LB_DATA_01> -P $SKEY"
        - name: "HANA BACKUP SNAP"
          processCentralId: 8990048
          parameters: "-s { systemName } -i <HANA_SYS_NR> -m pms_onl_cons -c localhost -t 3 -p $LOCAL_SNAP_RET -u BACKUP"
        - name: "HANA BACKUP FILE DAILY"
          processCentralId: 8990048
          parameters: "-s { systemName } -d <BKP_DATA_DEST1> -r - -b { local_file_ret } -t ALL -m file -p full -u BACKUP -A blob -B <BKP_LB_DATA_01> -C $SKEY -D { blob_file_ret }"
        - name: "HANA BACKUP FILE MONTHLY"
          processCentralId: 8990048
          parameters: "-s { systemName } -d <BKP_DATA_DEST1_MONTHLY> -r - -b { local_file_ret } -t ALL -m file -p full -u BACKUP -A blob -B <BKP_LB_DATA_01> -C $SKEY -D { blob_file_ret_monthly }"
        - name: "HANA BACKUP FILE YEARLY"
          processCentralId: 8990048
          parameters: "-s { systemName } -d <BKP_DATA_DEST1_YEARLY> -r - -b { local_file_ret } -t ALL -m file -p full -u BACKUP -A blob -B <BKP_LB_DATA_01> -C $SKEY -D { blob_file_ret_yearly }"
        - name: "FS BACKUP INCR"
          processCentralId: 8990048
          parameters: "-a { systemName } -b <BKP_LB_FS_01> -c 1 -d $FSBKPBASE -e /backup -f localhost -g $SKEY -h <CZ_LOCAL_FILE_RET_CLASS_3> -i <CZ_BLOB_FILE_RET_CLASS_3>"

      service_levels:
        SLA1:
          variables:
            local_file_ret: "<CZ_LOCAL_FILE_RET_CLASS_1>"
            local_snap_ret: "<CZ_LOCAL_SNAP_RET_CLASS_1>"
            local_log_ret: "<CZ_LOCAL_LOG_RET_CLASS_1>"
            blob_log_ret: "<CZ_BLOB_LOG_RET_CLASS_1>"
            blob_file_ret: "<CZ_BLOB_FILE_RET_CLASS_1>"
            blob_file_ret_monthly: "<CZ_BLOB_FILE_RET_MONTHLY_CLASS_1>"
            blob_file_ret_yearly: "<CZ_BLOB_FILE_RET_YEARLY_CLASS_1>"
        SLA2:
          variables:
            local_file_ret: "<CZ_LOCAL_FILE_RET_CLASS_2>"
            local_snap_ret: "<CZ_LOCAL_SNAP_RET_CLASS_2>"
            local_log_ret: "<CZ_LOCAL_LOG_RET_CLASS_2>"
            blob_log_ret: "<CZ_BLOB_LOG_RET_CLASS_2>"
            blob_file_ret: "<CZ_BLOB_FILE_RET_CLASS_2>"
            blob_file_ret_monthly: "<CZ_BLOB_FILE_RET_MONTHLY_CLASS_2>"
            blob_file_ret_yearly: "<CZ_BLOB_FILE_RET_YEARLY_CLASS_2>"
        SLA3:
          variables:
            local_file_ret: "<CZ_LOCAL_FILE_RET_CLASS_3>"
            local_snap_ret: "<CZ_LOCAL_SNAP_RET_CLASS_3>"
            local_log_ret: "<CZ_LOCAL_LOG_RET_CLASS_3>"
            blob_log_ret: "<CZ_BLOB_LOG_RET_CLASS_3>"
            blob_file_ret: "<CZ_BLOB_FILE_RET_CLASS_3>"
            blob_file_ret_monthly: "<CZ_BLOB_FILE_RET_MONTHLY_CLASS_3>"
            blob_file_ret_yearly: "<CZ_BLOB_FILE_RET_YEARLY_CLASS_3>"
        SLA4:
          variables:
            local_file_ret: "<CZ_LOCAL_FILE_RET_CLASS_4>"
            local_snap_ret: "<CZ_LOCAL_SNAP_RET_CLASS_4>"
            local_log_ret: "<CZ_LOCAL_LOG_RET_CLASS_4>"
            blob_log_ret: "<CZ_BLOB_LOG_RET_CLASS_4>"
            blob_file_ret: "<CZ_BLOB_FILE_RET_CLASS_4>"
            blob_file_ret_monthly: "<CZ_BLOB_FILE_RET_MONTHLY_CLASS_4>"
            blob_file_ret_yearly: "<CZ_BLOB_FILE_RET_YEARLY_CLASS_4>"

  roles:
    - hana_backup
```

## Variable Types and Usage

The role supports three types of variables:

1. **CSV Variables** (from CSV file): `{ systemName }`, `{ instanceNo }`, `{ systemType }`, etc.
2. **SLA Variables** (from service_levels): `{ local_file_ret }`, `{ blob_file_ret }`, etc.

### Variable Substitution Examples

```yaml
# CSV variables (single curly braces)
parameters: "-s { systemName } -i { instanceNo }"
# Result: "-s MHP -i 05"
```

### Agent Name Configuration

The role supports flexible agent name configuration through multiple levels:

#### Default Behavior
By default, the role automatically uses the value from the `system_vdns` column in the CSV file as the agent name for all commands.

#### Override Options

```yaml
# Global override
override:
  command_defaults:
    agentName: "localhost"  # All commands use "localhost"

# SLA-level override
override:
  service_levels:
    SLA1:
      command_defaults:
        agentName: "someagent01"  # All SLA1 commands use "someagent01"

# Command-level override
override:
  commands:
    - name: "HANA BACKUP LOG"
      agentName: "someagent02"  # This specific command uses "someagent02" (in all SLAs)
```

#### Priority Order
Agent name resolution follows this priority order (highest to lowest):
1. **Command-specific** `agentName` setting
2. **SLA-level** `command_defaults.agentName` setting
3. **Global** `command_defaults.agentName` setting
4. **CSV column** `system_vdns` value (default behavior)

## Default Configuration

### Standard Commands

The role includes a predefined set of commands in `defaults/main.yml`:

**Note**: The listed commands in defaults/main.yml are part of an initial draft and have not yet been validated for correctness or applicability.
The entire Ansible role is currently under active development and subject to significant changes.

1. **HANA BACKUP LOG** - Log backup operations
2. **HANA RESTORE FILE** - File-based restore operations
3. **HANA RESTORE SNAP** - Snapshot-based restore operations
4. **HANA BACKUP SNAP** - Snapshot backup operations
5. **HANA BACKUP FILE DAILY** - Daily file backup operations
6. **HANA BACKUP FILE MONTHLY** - Monthly file backup operations
7. **HANA BACKUP FILE YEARLY** - Yearly file backup operations
8. **FS BACKUP INCR** - Incremental filesystem backup


## Role Variables

### Required Variables

| Variable                             | Type    | Description                                        |
| ------------------------------------ | ------- | -------------------------------------------------- |
| `csv_file`                           | string  | Path to the CSV file containing system information |
| `ALPACA_Operator_API_Host`           | string  | ALPACA Operator server hostname                    |
| `ALPACA_Operator_API_Protocol`       | string  | API protocol (http/https)                          |
| `ALPACA_Operator_API_Port`           | integer | API port number                                    |
| `ALPACA_Operator_API_Username`       | string  | API username                                       |
| `ALPACA_Operator_API_Password`       | string  | API password                                       |
| `ALPACA_Operator_API_Validate_Certs` | boolean | Whether to validate SSL certificates               |

### Optional Variables

| Variable           | Type | Default | Description                          |
| ------------------ | ---- | ------- | ------------------------------------ |
| `system_variables` | dict | `{}`    | System-specific variables            |
| `override`         | dict | `{}`    | Dictionary to override role defaults |

## Advanced Configuration

### Override Behavior

The role supports overriding defaults through the `override` variable in your playbook. The override uses Ansible's `combine` filter with `recursive=True` for merging.

#### Parameter Value Prioritization

The role follows a specific priority order when merging parameter values:

1. **Role Defaults** (`defaults/main.yml`) - Base configuration
2. **Playbook Override** (`override`) - Global overrides from playbook
3. **SLA Command Defaults** (`service_levels[SLA].command_defaults`) - SLA-specific defaults
4. **Individual Command Definition** (`commands[]` or `service_levels[SLA].commands[]`) - Command-specific settings

#### Dictionary and List Behavior

**Important**: When overriding dictionaries that contain lists (such as `commands` or `daysOfWeek`), the entire list is replaced, not merged. This means:

- If you define `commands` in your override, it will completely replace the default command set
- If you define `daysOfWeek` in a schedule override, it will replace the default days
- To extend rather than replace, you must include all desired items in your override

### SLA Level Customization

The role supports dynamic SLA level management through the `override` variable. You can add new SLA levels, modify existing ones, or completely replace the default SLA structure.

#### Adding New SLA Levels

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

## Role Tasks

1. **CSV Validation** - Checks if the CSV file exists and is accessible
2. **CSV Processing** - Reads and parses the CSV file using Python
3. **CSV Filtering** - Optionally filters CSV rows based on column name and expected value
4. **Configuration Merging** - Merges role defaults with playbook overrides
5. **System Generation** - Iterates through CSV rows and creates/updates systems using `alpaca_system` module
6. **Command Generation** - Iterates through CSV rows and generates commands
7. **ALPACA Integration** - Creates/updates commands using the `alpaca_command` module

## Dependencies

This role depends on the `pcg.alpaca_operator` collection, specifically the `alpaca_system` and `alpaca_command` modules. For detailed information about the collection and its modules, see the [Collection README](../../README.md).

## Return Values

The role does not return specific values but creates/updates ALPACA Operator commands for each system defined in the CSV file.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](../../LICENSE) file for details.
