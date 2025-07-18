# HANA Backup Role

This Ansible role generates and executes ALPACA Operator Commands based on CSV data and SLA levels.

## Description

The `hana_backup` role reads a CSV file with system data and automatically generates ALPACA Operator Commands based on SLA levels:
- SLA1: 4 Commands
- SLA2: 3 Commands  
- SLA3: 2 Commands
- SLA4: 1 Command

## Prerequisites

- Python 3
- ALPACA Ansible Collection installed
- CSV file with the required columns

## CSV Format

The CSV file must contain the following columns:
- `hdb_nw_sid`: Mapped to `systemName`
- `system_vdns`: Mapped to `agentName`  
- `system_sla`: Determines the number of commands (SLA1-SLA4)

## Usage

### Simple Execution

```bash
ansible-playbook hana_backup.yml
```

### With Custom Variables

```bash
ansible-playbook hana_backup.yml -e "csv_file=/path/to/your/csv output_dir=/path/to/output"
```

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `csv_file` | `{{ playbook_dir }}/roles/hana_backup/files/swm_prod.csv` | Path to CSV file |
| `output_dir` | `{{ playbook_dir }}/generated_commands` | Output directory for generated playbooks |

## Output

The role creates:
1. A Python script to read the CSV file
2. Individual playbooks for each command based on SLA level
3. A consolidated playbook for all commands

## Structure

```
roles/hana_backup/
├── defaults/main.yml          # Default variables
├── files/swm_prod.csv         # Example CSV file
├── tasks/
│   ├── main.yml              # Main tasks
│   ├── process_csv.yml       # CSV processing
│   ├── validate_csv.yml      # CSV validation
│   └── create_commands.yml   # Command generation
└── README.md                 # This file
```

## Example CSV

```csv
hdb_nw_sid,system_vdns,system_sla
HDB,server1.example.com,SLA1
HDB,server2.example.com,SLA2
HDB,server3.example.com,SLA3
HDB,server4.example.com,SLA4
```

## Troubleshooting

- **CSV not found**: Check the path in the `csv_file` variable
- **Template errors**: Ensure CSV columns are correctly named
- **Permission errors**: Check write permissions in `output_dir` 