# ALPACA Operator Ansible Collection Documentation

## Overview

The ALPACA Operator Ansible Collection provides a comprehensive set of modules for managing ALPACA Operator environments through Ansible automation. This collection enables you to manage agents, systems, groups, commands, and command sets using the ALPACA Operator REST API.

## Modules

### Core Management Modules

| Module                                                  | Description                    | Use Case                                                                              |
| ------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------- |
| [`pcg.alpaca_operator.alpaca_agent`](alpaca_agent.md)   | Manage ALPACA Operator agents  | Create, update, delete, and configure agents with escalation settings                 |
| [`pcg.alpaca_operator.alpaca_system`](alpaca_system.md) | Manage ALPACA Operator systems | Create, update, delete systems with RFC connections, agent assignments, and variables |
| [`pcg.alpaca_operator.alpaca_group`](alpaca_group.md)   | Manage ALPACA Operator groups  | Create, rename, and delete groups for organizing systems                              |

### Command Management Modules

| Module                                                            | Description                                | Use Case                                                 |
| ----------------------------------------------------------------- | ------------------------------------------ | -------------------------------------------------------- |
| [`pcg.alpaca_operator.alpaca_command`](alpaca_command.md)         | Manage individual ALPACA Operator commands | Fine-grained control over single command properties      |
| [`pcg.alpaca_operator.alpaca_command_set`](alpaca_command_set.md) | Manage command sets for systems            | Bulk management of all commands associated with a system |

## Quick Start

### Prerequisites

- Python >= 3.8
- ansible-core >= 2.12
- ALPACA Operator >= 5.6.0

### Basic Usage

1. **Install the Collection**
   ```bash
   ansible-galaxy collection install pcg.alpaca_operator
   ```

2. **Configure API Connection in Inventory**
   ```ini
   # inventories/alpaca.ini
   [local]
   localhost ansible_connection=local ansible_python_interpreter=python3

   [local:vars]
   ALPACA_Operator_API_Host='your-alpaca-server'
   ALPACA_Operator_API_Protocol='https'
   ALPACA_Operator_API_Port='8443'
   ALPACA_Operator_API_Username='your-username'
   ALPACA_Operator_API_Password='your-password'
   ALPACA_Operator_API_Validate_Certs=False
   ```

3. **Create a Basic Playbook**
   ```yaml
   - name: Manage ALPACA Operator Environment
     hosts: local
     gather_facts: false

     vars:
       api_connection:
         host: "{{ ALPACA_Operator_API_Host }}"
         protocol: "{{ ALPACA_Operator_API_Protocol }}"
         port: "{{ ALPACA_Operator_API_Port }}"
         username: "{{ ALPACA_Operator_API_Username }}"
         password: "{{ ALPACA_Operator_API_Password }}"
         tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

     tasks:
       - name: Create a group
         pcg.alpaca_operator.alpaca_group:
           name: production
           state: present
           api_connection: "{{ api_connection }}"

## Common Patterns

### 1. Agent Management
```yaml
- name: Create agent with escalation
  pcg.alpaca_operator.alpaca_agent:
    name: backup-agent-01
    description: Backup Agent for Production
    ip_address: 192.168.1.100
    location: virtual
    escalation:
      failures_before_report: 3
      mail_enabled: true
      mail_address: monitoring@company.com
    state: present
    api_connection: "{{ api_connection }}"
```

### 2. System Management with RFC Connection
```yaml
- name: Create SAP system
  pcg.alpaca_operator.alpaca_system:
    name: sap-prod-01
    description: SAP Production System
    group_name: production
    rfc_connection:
      type: instance
      host: sap-prod-server
      instanceNumber: 00
      sid: PRD
      username: rfc_user
      password: rfc_password
      client: 100
    agents:
      - name: backup-agent-01
    variables:
      - name: "BACKUP_PATH"
        value: "/backup/sap"
    state: present
    api_connection: "{{ api_connection }}"
```

### 3. Command Management
```yaml
- name: Configure backup command
  pcg.alpaca_operator.alpaca_command:
    system:
      system_name: sap-prod-01
    command:
      name: "Daily Backup"
      agent_name: backup-agent-01
      process_central_id: 8990048
      parameters: "-p PRD -s /backup/sap"
      schedule:
        period: fixed_time
        time: "02:00:00"
        days_of_week:
          - monday
          - tuesday
          - wednesday
          - thursday
          - friday
      critical: true
      escalation:
        mail_enabled: true
        mail_address: monitoring@company.com
        min_failure_count: 1
    api_connection: "{{ api_connection }}"
```

### 4. Bulk Command Management
```yaml
- name: Configure all commands for system
  pcg.alpaca_operator.alpaca_command_set:
    system:
      system_name: sap-prod-01
    commands:
      - name: "Daily Backup"
        agent_name: backup-agent-01
        process_central_id: 8990048
        schedule:
          period: fixed_time
          time: "02:00:00"
      - name: "Log Cleanup"
        agent_name: backup-agent-01
        process_central_id: 8990048
        schedule:
          period: cron_expression
          cron_expression: '0 3 * * 0'
    api_connection: "{{ api_connection }}"
```

## Best Practices

### 1. Use Variables for API Connection
Store your API connection details in the inventory file:

```ini
# inventories/alpaca.ini
[local]
localhost ansible_connection=local ansible_python_interpreter=python3

[local:vars]
ALPACA_Operator_API_Host='your-alpaca-server'
ALPACA_Operator_API_Protocol='https'
ALPACA_Operator_API_Port='8443'
ALPACA_Operator_API_Username='your-username'
ALPACA_Operator_API_Password='your-password'
ALPACA_Operator_API_Validate_Certs=False
```

Then reference them in your playbook:

```yaml
vars:
  api_connection:
    host: "{{ ALPACA_Operator_API_Host }}"
    protocol: "{{ ALPACA_Operator_API_Protocol }}"
    port: "{{ ALPACA_Operator_API_Port }}"
    username: "{{ ALPACA_Operator_API_Username }}"
    password: "{{ ALPACA_Operator_API_Password }}"
    tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"
```

### 2. Use Check Mode for Testing
Always test your playbooks in check mode first:

```bash
ansible-playbook your-playbook.yml --check
```

### 3. Organize by Environment
Structure your playbooks to separate different environments:

```
playbooks/
├── production/
│   ├── agents.yml
│   ├── systems.yml
│   └── commands.yml
├── staging/
│   ├── agents.yml
│   ├── systems.yml
│   └── commands.yml
└── common/
    └── groups.yml
```

### 4. Use Tags for Selective Execution
```yaml
- name: Create production agents
  pcg.alpaca_operator.alpaca_agent:
    # ... configuration
  tags:
    - agents
    - production
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify API credentials
   - Check if the ALPACA Operator instance is accessible
   - Ensure TLS certificate validation settings are correct

2. **Command Set Module Removes Commands**
   - The `pcg.alpaca_operator.alpaca_command_set` module takes full control of the command set
   - Any commands not defined in your playbook will be removed
   - Use `pcg.alpaca_operator.alpaca_command` for individual command management

3. **RFC Password Not Applied**
   - RFC passwords cannot be retrieved via API
   - Change at least one additional attribute to ensure the password is applied

### Debug Information

Enable verbose output for debugging:

```bash
ansible-playbook your-playbook.yml -vvv
```

## Support

For issues and questions:

- **Author**: Jan-Karsten Hansmeyer (@pcg)

## License

Apache License, Version 2.0