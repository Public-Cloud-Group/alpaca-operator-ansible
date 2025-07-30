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

### Filtering Example

```yaml
---
- name: Configure HANA Backup Commands for HDB Systems Only
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

    # Filter to process only HDB systems using wildcard
    override:
      csv_filter:
        enabled: true
        column_name: "hdb_nw_sid"
        expected_value: "HDB*"

  roles:
    - hana_backup
```

### Multiple Filtering Examples

```yaml
# Exact match examples
# Filter by system type (HDB systems only)
override:
  csv_filter:
    enabled: true
    column_name: "system_type"
    expected_value: "HDB"

# Filter by specific system ID
override:
  csv_filter:
    enabled: true
    column_name: "hdb_nw_sid"
    expected_value: "MHP"

# Wildcard filtering examples
# Filter all SLA levels starting with "SLA" (SLA1, SLA2, SLA3, SLA4)
override:
  csv_filter:
    enabled: true
    column_name: "system_sla"
    expected_value: "SLA*"

# Filter system IDs starting with "M" (MHP, MUP, etc.)
override:
  csv_filter:
    enabled: true
    column_name: "hdb_nw_sid"
    expected_value: "M*"

# Filter system IDs containing "HP" anywhere
override:
  csv_filter:
    enabled: true
    column_name: "hdb_nw_sid"
    expected_value: "*HP*"

# Filter system IDs starting with "MH"
override:
  csv_filter:
    enabled: true
    column_name: "hdb_nw_sid"
    expected_value: "MH*"

# Filter system types with exactly 3 characters starting with "H"
override:
  csv_filter:
    enabled: true
    column_name: "system_type"
    expected_value: "H??"
```

## Requirements

- Python >= 3.8
- Ansible >= 2.12
- ALPACA Operator >= 5.6.0
- CSV file containing system information

## How It Works

### Basic Concept

1. **CSV Input**: The role reads system information from a CSV file
2. **CSV Filtering**: Optional filtering of CSV rows based on column name and expected value
3. **SLA Classification**: Each system is assigned a Service Level Agreement (SLA)
4. **Command Generation**: Based on the SLA, appropriate backup commands are created
5. **ALPACA Integration**: Commands are created/updated in ALPACA Operator

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

The role expects a CSV file with semicolon (`;`) as the delimiter.

#### Available CSV Variables

The role automatically maps CSV columns to variables that can be used in command parameters. These variables must be enclosed in curly braces `{ variableName }`:

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

#### Using CSV Variables in Command Parameters

You can use these variables in your command definitions within the `override` section:

```yaml
---
- name: HANA Backup with CSV Variables
  hosts: localhost
  gather_facts: false

  vars:
    csv_file: "/path/to/your/systems.csv"
    override:
      commands:
        - name: "HANA BACKUP SNAP"
          processCentralId: 8990048
          parameters: "-s { systemName } -i { instanceNo } -m pms_onl_cons -c localhost -t 3 -p $LOCAL_SNAP_RET -u BACKUP"
        - name: "HANA BACKUP FILE DAILY"
          processCentralId: 8990048
          parameters: "-s { systemName } -d <BKP_DATA_DEST1> -r - -b { local_file_ret } -t ALL -m file -p full -u BACKUP -A blob -B <BKP_LB_DATA_01> -C $SKEY -D { blob_file_ret }"

  roles:
    - hana_backup
```

#### Variable Substitution in Command Parameters

The role automatically substitutes variables in command parameters using the `{ variable_name }` syntax:

```yaml
# In your command definition
parameters: "-s { systemName } -i { instanceNo } -t { systemType }"

# Gets automatically replaced with actual values from CSV
parameters: "-s MHP -i 05 -t HDB"
```

## Comprehensive Example

Here's a complete example showing all available parameters and variables:

```yaml
---
- name: Comprehensive HANA Backup Configuration Example
  hosts: localhost
  gather_facts: false

  vars:
    # Path to the CSV file containing system information
    csv_file: "/path/to/your/systems.csv"

    # ALPACA Operator API connection details
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

    # Default command configuration unless overwritten
    override:
      # CSV filtering configuration
      csv_defaults:
        filter:
          enabled: true                    # Enable CSV row filtering
          column_name: "system_type"       # Filter by system_type column
          expected_value: "HDB*"           # Process only HDB systems (supports wildcards)

      # Global command defaults applied to all commands unless overridden
      command_defaults:
        state: present                     # Command state: present (create/update) or absent (delete)
        # agentName: "localhost"           # Optional: Override agent name for all commands. If not specified, the role will automatically use the value from the "system_vdns" column in the CSV file.
        schedule:
          period: fixed_time               # Scheduling period: fixed_time, manually, hourly, etc.
          time: "02:00:00"                 # Execution time in HH:mm:ss format
          daysOfWeek:                      # Days of the week for execution
            - monday
            - tuesday
            - wednesday
            - thursday
            - friday
            - saturday
            - sunday
        parametersNeeded: true             # Whether command requires additional parameters
        disabled: false                    # Whether command is disabled
        critical: true                     # Whether command is marked as critical
        history:
          documentAllRuns: true            # Document all command executions
          retention: 200                   # Retention time in seconds
        autoDeploy: false                  # Auto-deploy command after creation
        timeout:
          type: custom                     # Timeout type: none, default, or custom
          value: 6000                      # Timeout value in seconds
        escalation:
          mailEnabled: true                # Enable email alerts
          smsEnabled: true                 # Enable SMS alerts
          mailAddress: "monitoring@pcg.io" # Email address for alerts
          smsAddress: "0123456789"         # SMS number for alerts
          minFailureCount: 1               # Minimum failures before escalation
          triggers:
            everyChange: true              # Escalate on every status change
            toRed: true                    # Escalate when status changes to red
            toYellow: true                 # Escalate when status changes to yellow
            toGreen: true                  # Escalate when status changes to green

      # Default commands for each SLA unless overwritten
      commands:
        # HANA Log Backup Command
        - name: "HANA BACKUP LOG"
          processCentralId: 8990048
          parameters: "-s { systemName } -n 4 -e blob -o <BKP_LB_LOG_01> -z $SKEY -r { blob_log_ret } -k { local_log_ret } -y -"
          schedule:
            period: fixed_time
            time: "01:00:00"               # Override global schedule for this command
            daysOfWeek:
              - monday
              - wednesday
              - friday
          critical: true                   # Override global critical setting
          timeout:
            type: custom
            value: 8000                    # Override global timeout for this command

        # HANA Snapshot Backup Command
        - name: "HANA BACKUP SNAP"
          processCentralId: 8990048
          parameters: "-s { systemName } -i { instanceNo } -m pms_onl_cons -c localhost -t 3 -p $LOCAL_SNAP_RET -u BACKUP"
          schedule:
            period: fixed_time
            time: "03:00:00"
          disabled: false
          escalation:
            mailEnabled: false             # Override global escalation for this command
            smsEnabled: true

        # HANA Daily File Backup Command
        - name: "HANA BACKUP FILE DAILY"
          processCentralId: 8990048
          parameters: "-s { systemName } -d <BKP_DATA_DEST1> -r - -b { local_file_ret } -t ALL -m file -p full -u BACKUP -A blob -B <BKP_LB_DATA_01> -C $SKEY -D { blob_file_ret }"
          schedule:
            period: fixed_time
            time: "04:00:00"
          critical: true

        # HANA Monthly File Backup Command
        - name: "HANA BACKUP FILE MONTHLY"
          processCentralId: 8990048
          parameters: "-s { systemName } -d <BKP_DATA_DEST1_MONTHLY> -r - -b { local_file_ret } -t ALL -m file -p full -u BACKUP -A blob -B <BKP_LB_DATA_01> -C $SKEY -D { blob_file_ret_monthly }"
          schedule:
            period: fixed_time
            time: "05:00:00"
            daysOfWeek:
              - sunday                     # Run only on Sundays

        # HANA Yearly File Backup Command
        - name: "HANA BACKUP FILE YEARLY"
          processCentralId: 8990048
          parameters: "-s { systemName } -d <BKP_DATA_DEST1_YEARLY> -r - -b { local_file_ret } -t ALL -m file -p full -u BACKUP -A blob -B <BKP_LB_DATA_01> -C $SKEY -D { blob_file_ret_yearly }"
          schedule:
            period: fixed_time
            time: "06:00:00"
            daysOfWeek:
              - sunday
          disabled: true                   # Disabled by default, enable manually when needed

        # Filesystem Incremental Backup Command
        - name: "FS BACKUP INCR"
          processCentralId: 8990048
          parameters: "-a { systemName } -b <BKP_LB_FS_01> -c 1 -d $FSBKPBASE -e /backup -f localhost -g $SKEY -h <CZ_LOCAL_FILE_RET_CLASS_3> -i <CZ_BLOB_FILE_RET_CLASS_3>"
          schedule:
            period: fixed_time
            time: "07:00:00"

      # SLA-specific configurations with custom variables and command overrides
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
          command_defaults:
            critical: true                 # All SLA1 commands are critical
            timeout:
              type: custom
              value: 8000                  # Longer timeout for production systems
            escalation:
              minFailureCount: 1           # Escalate immediately on failure
          commands:
            # SLA1-specific command override
            # Remember: When overriding lists (e.g. `commands`, `variables`, `daysOfWeek`), your definition replaces the entire default list; defaults are merged recursively for dictionaries, but lists are not merged—define the full list if you want to extend rather than replace.
            - name: "SLA1 ENHANCED BACKUP"
              processCentralId: 8990048
              parameters: "-s { systemName } -i { instanceNo } -t { systemType } -e enhanced -r { blob_file_ret }"
              schedule:
                period: fixed_time
                time: "01:30:00"
              critical: true

        SLA2:
          variables:
            local_file_ret: "<CZ_LOCAL_FILE_RET_CLASS_2>"
            local_snap_ret: "<CZ_LOCAL_SNAP_RET_CLASS_2>"
            local_log_ret: "<CZ_LOCAL_LOG_RET_CLASS_2>"
            blob_log_ret: "<CZ_BLOB_LOG_RET_CLASS_2>"
            blob_file_ret: "<CZ_BLOB_FILE_RET_CLASS_2>"
            blob_file_ret_monthly: "<CZ_BLOB_FILE_RET_MONTHLY_CLASS_2>"
            blob_file_ret_yearly: "<CZ_BLOB_FILE_RET_YEARLY_CLASS_2>"
          command_defaults:
            critical: false                # SLA2 commands are not critical
            timeout:
              type: custom
              value: 6000
            escalation:
              minFailureCount: 2           # Escalate after 2 failures

        SLA3:
          variables:
            local_file_ret: "<CZ_LOCAL_FILE_RET_CLASS_3>"
            local_snap_ret: "<CZ_LOCAL_SNAP_RET_CLASS_3>"
            local_log_ret: "<CZ_LOCAL_LOG_RET_CLASS_3>"
            blob_log_ret: "<CZ_BLOB_LOG_RET_CLASS_3>"
            blob_file_ret: "<CZ_BLOB_FILE_RET_CLASS_3>"
            blob_file_ret_monthly: "<CZ_BLOB_FILE_RET_MONTHLY_CLASS_3>"
            blob_file_ret_yearly: "<CZ_BLOB_FILE_RET_YEARLY_CLASS_3>"
          command_defaults:
            critical: false
            disabled: true                 # Disable all SLA3 commands by default
            timeout:
              type: default                # Use default timeout
            escalation:
              mailEnabled: false           # No email alerts for dev systems
              smsEnabled: false            # No SMS alerts for dev systems

        SLA4:
          variables:
            local_file_ret: "<CZ_LOCAL_FILE_RET_CLASS_4>"
            local_snap_ret: "<CZ_LOCAL_SNAP_RET_CLASS_4>"
            local_log_ret: "<CZ_LOCAL_LOG_RET_CLASS_4>"
            blob_log_ret: "<CZ_BLOB_LOG_RET_CLASS_4>"
            blob_file_ret: "<CZ_BLOB_FILE_RET_CLASS_4>"
            blob_file_ret_monthly: "<CZ_BLOB_FILE_RET_MONTHLY_CLASS_4>"
            blob_file_ret_yearly: "<CZ_BLOB_FILE_RET_YEARLY_CLASS_4>"
          command_defaults:
            critical: false
            disabled: true                 # Disable all SLA4 commands by default
            autoDeploy: false              # Don't auto-deploy test commands

  roles:
    - hana_backup
```

### Variable Types and Usage

This example demonstrates three types of variables:

1. **CSV Variables** (from CSV file): `{ systemName }`, `{ instanceNo }`, `{ systemType }`, etc.
2. **SLA Variables** (from service_levels): `{ local_file_ret }`, `{ blob_file_ret }`, etc.
3. **System Variables** (from ALPACA system config): `$SKEY`, `<BKP_DATA_DEST1>`, etc.

### Agent Name Configuration

The role supports flexible agent name configuration through multiple levels:

#### Default Behavior
By default, the role automatically uses the value from the `system_vdns` column in the CSV file as the agent name for all commands.

#### Global Override
You can override the agent name for all commands by setting it in the global `command_defaults`:

```yaml
override:
  command_defaults:
    agentName: "localhost"  # All commands will use "localhost" as agent
```

#### SLA-Level Override
You can set different agent names for specific SLA levels:

```yaml
override:
  service_levels:
    SLA1:
      command_defaults:
        agentName: "prod-agent"  # All SLA1 commands use "prod-agent"
    SLA2:
      command_defaults:
        agentName: "test-agent"  # All SLA2 commands use "test-agent"
```

#### Command-Level Override
You can override the agent name for specific commands:

```yaml
override:
  commands:
    - name: "HANA BACKUP LOG"
      agentName: "backup-agent"  # This specific command uses "backup-agent"
      processCentralId: 8990048
      parameters: "-s { systemName } -n 4 -e blob -o <BKP_LB_LOG_01>"
```

#### Priority Order
Agent name resolution follows this priority order (highest to lowest):
1. **Command-specific** `agentName` setting
2. **SLA-level** `command_defaults.agentName` setting
3. **Global** `command_defaults.agentName` setting
4. **CSV column** `system_vdns` value (default behavior)

#### Example Configuration
```yaml
override:
  command_defaults:
    agentName: "default-agent"  # Global fallback
  service_levels:
    SLA1:
      command_defaults:
        agentName: "prod-agent"  # Override for SLA1
    SLA2:
      command_defaults:
        agentName: "test-agent"  # Override for SLA2
  commands:
    - name: "HANA BACKUP LOG"
      agentName: "backup-agent"  # Override for this specific command
      processCentralId: 8990048
```

**Result**: 
- "HANA BACKUP LOG" command uses `backup-agent`
- Other SLA1 commands use `prod-agent`
- SLA2 commands use `test-agent`
- All other commands use `default-agent`

### Priority Order

Variables are resolved in this priority order:
1. **Command-specific** settings (highest priority)
2. **SLA-specific** settings
3. **Global command defaults** (lowest priority)

This allows fine-grained control over each command while maintaining consistency across similar systems.

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

### CSV Filtering Variables

| Variable   | Type | Default | Description                                                          |
| ---------- | ---- | ------- | -------------------------------------------------------------------- |
| `csv_filter.enabled` | boolean | `false` | Enable CSV row filtering |
| `csv_filter.column_name` | string | `null` | Name of the CSV column to filter on (e.g., "system_sla", "system_type") |
| `csv_filter.expected_value` | string | `null` | Expected value in the column for the row to be processed (supports wildcards) |

**Note**: Filtering is applied after CSV parsing but before command generation. Only rows where the specified column matches the expected value will be processed. If filtering is disabled or not properly configured, all CSV rows will be processed.

**Wildcard Support**: Wildcards are automatically detected in `expected_value`. The following wildcards are supported:
- `*` - Matches any sequence of characters (zero or more)
- `?` - Matches any single character

**Important**: When using `*` at the end of a pattern (e.g., `"HDB*"`), it will match both the exact value (e.g., `"HDB"`) and values that start with the pattern (e.g., `"HDB1"`, `"HDB2"`, etc.).

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
3. **CSV Filtering** - Optionally filters CSV rows based on column name and expected value
4. **Configuration Merging** - Merges role defaults with playbook overrides
5. **Command Generation** - Iterates through CSV rows and generates commands
6. **ALPACA Integration** - Creates/updates commands using the `alpaca_command` module

## Dependencies

This role depends on the `pcg.alpaca_operator` collection, specifically the `alpaca_command` module.

## Return Values

The role does not return specific values but creates/updates ALPACA Operator commands for each system defined in the CSV file.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](../../LICENSE) file for details.

## Testing

### Testing CSV Filtering

You can test the CSV filtering functionality using the included test playbook:

```bash
# Test wildcard filtering for all SLA levels (SLA1, SLA2, SLA3, SLA4)
ansible-playbook test_filtering.yml

# Test with different filter values by modifying the override section
```

The test playbook creates a sample CSV file with different SLA levels and demonstrates how wildcard filtering works. The current configuration filters for all SLA levels using the pattern `SLA*`.

## Support

For issues and questions related to this role, please refer to the ALPACA Operator documentation or create an issue in the project repository.
