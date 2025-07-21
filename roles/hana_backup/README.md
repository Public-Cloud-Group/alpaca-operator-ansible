# HANA Backup Role

## Overview

The `hana_backup` role automates the creation and management of SAP HANA backup commands using the ALPACA Operator. This role reads system information from a CSV file and generates appropriate backup commands based on Service Level Agreement (SLA) requirements.

## Purpose

This role is designed to:
- Process CSV files containing SAP HANA system information
- Generate ALPACA Operator commands for backup automation
- Apply different backup strategies based on SLA levels (SLA1, SLA2, SLA3, SLA4)
- Configure backup schedules, parameters, and escalation settings
- Integrate with the ALPACA Operator API for command deployment

## Requirements

### Ansible Version
- Python >= 3.8
- Ansible >= 2.12
- ALPACA Operator >= 5.6.0

### Dependencies
- Python 3 (for CSV processing)
- ALPACA Operator API access
- `pcg.alpaca_operator` collection

### Target Platforms
- Enterprise Linux 7, 8, 9

## Role Variables

### Required Variables

| Variable   | Type   | Description                                        | Default             |
| ---------- | ------ | -------------------------------------------------- | ------------------- |
| `csv_file` | string | Path to the CSV file containing system information | `/tmp/swm_prod.csv` |


### CSV File Format

The CSV file should contain the following columns (semicolon-separated):
- `hdb_nw_sid`: HANA system SID
- `system_vdns`: System virtual DNS name
- `system_sla`: Service Level Agreement (SLA1, SLA2, SLA3, SLA4)
- `system_type`: System type
- `system_staging`: Staging information
- `Instance_no`: Instance number

### Command Templates

The role uses predefined command templates for different SLA levels:

#### SLA1 (Premium)
- **BKP: DB log sync** - Every 5 minutes
- **BKP: DB data sync** - Fixed time (12:00:00) on Mon, Tue, Thu, Fri, Sun
- **BKP: DB shared sync** - Once per day
- **BKP: System health check** - Hourly

#### SLA2 (Standard)
- **BKP: DB log sync** - Fixed time (12:00:00) daily
- **BKP: DB data sync** - Fixed time (12:00:00) on Mon, Tue, Wed, Thu, Fri, Sat, Sun
- **BKP: System health check** - Every 4 hours

#### SLA3 (Basic)
- **BKP: DB log sync** - Fixed time (12:00:00) on Mon, Tue, Thu, Fri, Sun
- **BKP: System health check** - Every 4 hours

#### SLA4 (Minimal)
- **BKP: Basic health check** - Fixed time (12:00:00) daily

### Override Variables

You can override command settings using the `override` variable:

```yaml
override:
  global_defaults:
    state: present
    disabled: false
    timeout:
      type: "default"
      value: 15
  SLA1:
    name: "Custom backup name"
    state: present
    disabled: false
```

## Role Structure

```
roles/hana_backup/
├── defaults/
│   └── main.yml          # Default variables and command templates
├── files/
│   └── read_csv.py       # Python script for CSV processing
├── tasks/
│   ├── main.yml          # Main role execution
│   ├── generate_commands.yml  # Command generation logic
│   └── process_csv_row.yml    # CSV row processing
├── meta/
│   └── main.yml          # Role metadata
└── README.md             # This documentation
```

## Tasks

### Main Tasks

1. **Validate CSV file** - Checks if the CSV file exists and is accessible
2. **Read CSV data** - Uses Python script to parse CSV and convert to JSON
3. **Process CSV rows** - Iterates through each row and generates commands
4. **Generate and execute commands** - Creates ALPACA commands based on SLA templates and ensure they exist in ALPACA operator

### Task Flow

```
main.yml
├── Validate csv_file variable
├── Check CSV file exists
├── Read CSV with Python script
├── Parse CSV data to JSON
└── Process each CSV row
    └── process_csv_row.yml
        ├── Set variables for current row
        └── Generate commands for SLA
            └── generate_commands.yml
                ├── Prepare command configuration
                └── Create ALPACA command and ensure it exist
```

## Examples

### Example CSV File

```csv
hdb_nw_sid;system_vdns;system_sla;system_type;system_staging;Instance_no
HDB;hana01.example.com;SLA1;PROD;PROD;00
HDB;hana02.example.com;SLA2;PROD;PROD;00
HDB;hana03.example.com;SLA3;TEST;TEST;00
```

### Example Playbook

```yaml
---
- name: Configure HANA Backup Commands
  hosts: localhost
  gather_facts: false

  vars:
    csv_file: "{{ playbook_dir }}/files/hana_systems.csv"
    ALPACA_Operator_API_Host: "{{ lookup('env', 'ALPACA_API_HOST') }}"
    ALPACA_Operator_API_Protocol: "https"
    ALPACA_Operator_API_Port: 443
    ALPACA_Operator_API_Username: "{{ lookup('env', 'ALPACA_USERNAME') }}"
    ALPACA_Operator_API_Password: "{{ lookup('env', 'ALPACA_PASSWORD') }}"
    ALPACA_Operator_API_Validate_Certs: true

    override:
      global_defaults:
        escalation:
          mailAddress: "monitoring@pcg.io"
          minFailureCount: 2
      SLA1:
        timeout:
          value: 30
        schedule:
          time: "01:00:00"

  tasks:
    - name: Include hana_backup role
      include_role:
        name: hana_backup
```

## Troubleshooting

### Common Issues

1. **CSV file not found**
   - Ensure the `csv_file` path is correct
   - Check file permissions

2. **CSV parsing errors**
   - Verify CSV format (semicolon-separated)
   - Check for encoding issues (UTF-8 recommended)

3. **API connection failures**
   - Validate API credentials
   - Check network connectivity
   - Verify SSL certificate settings

4. **Command generation errors**
   - Ensure SLA values in CSV match defined templates
   - Check override variable syntax

## License

<!-- license:start -->

This project is licensed under the GNU General Public License v3.0 or later. See the [LICENSE](LICENSE) file for details.

<!-- license:end -->