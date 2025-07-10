# CSV Processor Role

An Ansible role for processing CSV files and generating ALPACA Operator commands based on defined SLA levels and variable mappings.

## Features

- **CSV Processing**: Automatic processing of CSV files with configurable columns
- **SLA Definitions**: Three predefined SLA levels (SLA1-3) with different retention, timeout, and escalation settings
- **Variable Mapping**: SLA-dependent values for command parameters (e.g., `<BKP_LOG_SRC>`)
- **Schedule Templates**: Predefined schedule templates (hourly, daily, every_5min, etc.)
- **Playbook Generation**: Automatic generation of various playbook types
- **Validation**: Comprehensive validation of CSV data and configurations

## SLA Definitions

### SLA 1 - Basic SLA
- Retention: 7 days local files, 30 days blob logs
- Timeout: 300 seconds (standard)
- Escalation: Email on errors, 2 failures until escalation
- Schedule: Hourly, Monday-Friday

### SLA 2 - Enhanced SLA
- Retention: 14 days local files, 90 days blob logs
- Timeout: 600 seconds (custom)
- Escalation: Email + SMS, 1 failure until escalation
- Schedule: Every 5 minutes, 7 days/week

### SLA 3 - Premium SLA
- Retention: 30 days local files, 365 days blob logs
- Timeout: 1800 seconds (custom)
- Escalation: Email + SMS, 1 failure until escalation
- Schedule: Every minute, 7 days/week

## Variable Mappings

The role supports the following variable mappings:

- `<BKP_LOG_SRC>` - Backup Log Source
- `<BKP_LOG_DEST1>` - Primary Backup Destination
- `<BKP_LOG_DEST2>` - Secondary Backup Destination
- `<BKP_LOG_CLEANUP_INT>` - Cleanup Interval 1
- `<BKP_LOG_CLEANUP_INT2>` - Cleanup Interval 2
- `<DB_HOST>` - Database Host

Variable values are determined by the SLA level assigned to each command.

## Schedule Templates

- `manual` - Manual execution
- `hourly` - Hourly
- `daily` - Daily at 02:00
- `business_hours` - Hourly, Monday-Friday
- `weekend` - Daily at 06:00, weekends
- `every_5min` - Every 5 minutes
- `every_minute` - Every minute

## Usage

### 1. Include Role

```yaml
- name: Process CSV and generate ALPACA Commands
  hosts: local
  gather_facts: false

  tasks:
    - name: Include CSV processor role
      include_role:
        name: csv_processor
```

### 2. Adjust Configuration

```yaml
vars:
  csv_processor:
    input_file: "swm_prod.csv"
    output_dir: "{{ playbook_dir }}/output"

  processing_options:
    create_commands: false  # Generate playbooks
    environment: "prod"
```

### 3. Create CSV File

```csv
SystemName,AgentName,CommandName,SLA,Parameters,Schedule,Enabled,Critical
"Production Server","backup_agent_01","BKP: DB log sync","2","-p GLTarch -s <BKP_LOG_SRC>","hourly","true","false"
```

## Generated Files

The role generates the following files in the output directory:

- **Individual Command Playbooks**: One playbook per command
- **Consolidated Playbook**: All commands in one playbook
- **SLA-specific Playbooks**: Separate playbooks for each SLA level
- **System-specific Playbooks**: Separate playbooks for each system
- **Inventory Template**: Ansible inventory with API configuration
- **Variables File**: All configurations and mappings
- **README**: Documentation of generated files

## Example

See `example_playbook.yml` and `files/swm_prod.csv` for a complete example.

## Requirements

- Ansible 2.12+
- ALPACA Operator Collection (`pcg.alpaca_operator`)
- CSV file with required columns

## License

GPL-3.0-or-later