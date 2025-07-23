# ALPACA Operator Collection for Ansible

[![CI](https://github.com/pcg-sap/alpaca-operator-ansible/actions/workflows/test.yml/badge.svg)](https://github.com/pcg-sap/alpaca-operator-ansible/actions/workflows/test.yml)

This Ansible Collection provides modules to manage **ALPACA Operator** via its REST API. It is designed to allow automation of common lifecycle operations related to groups, agents, systems, and commands within ALPACA-managed infrastructures.

## License

<!-- license:start -->

This project is licensed under the GNU General Public License v3.0 or later. See the [LICENSE](LICENSE) file for details.

<!-- license:end -->


## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Included content

This collection includes the following modules:

| Module Name          | Description                                              |
| -------------------- | -------------------------------------------------------- |
| `alpaca_agent`       | Manage ALPACA Operator agents                            |
| `alpaca_command_set` | Manage all ALPACA Operator commands of a specific system |
| `alpaca_command`     | Manage a single ALPACA Operator command                  |
| `alpaca_group`       | Manage ALPACA Operator groups                            |
| `alpaca_system`      | Manage ALPACA Operator systems                           |


All modules require API connection parameters and support both `present` and `absent` states where applicable.

Additionally, a shared utility (`_alpaca_api.py`) is available under `module_utils` for internal use, handling REST API logic and token management.

## Included Roles

This collection also includes the following role:

| Role Name     | Description                                                          |
| ------------- | -------------------------------------------------------------------- |
| `hana_backup` | Automate SAP HANA backup command creation in ALPACA Operator systems |

### HANA Backup Role

The `hana_backup` role automates the creation and management of SAP HANA backup commands in ALPACA Operator systems. It reads system information from a CSV file and creates standardized commands for each system based on their Service Level Agreement (SLA) classification.

#### Basic Usage

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

#### CSV File Requirements

The role expects a CSV file with semicolon (`;`) delimiter containing:

| Column Name      | Description                | Example                        |
| ---------------- | -------------------------- | ------------------------------ |
| `hdb_nw_sid`     | System ID/Name             | `HDB`                          |
| `system_vdns`    | Agent hostname             | `agent01.example.com`          |
| `system_sla`     | Service Level Agreement    | `SLA1`, `SLA2`, `SLA3`, `SLA4` |
| `system_type`    | System type classification | `PROD`, `TEST`, `DEV`          |
| `system_staging` | Staging environment        | `PROD`, `STAGE`, `DEV`         |
| `Instance_no`    | HANA instance number       | `00`, `01`, `02`               |

#### Supported Commands

The role creates standardized backup commands including:
- HANA BACKUP LOG
- HANA RESTORE FILE/SNAP
- HANA BACKUP FILE (Daily/Monthly/Yearly)
- HANA BACKUP SNAP
- FS BACKUP (Incremental/Full)

For detailed configuration options and advanced usage, see the role's [README](roles/hana_backup/README.md).

## Requirements

- Python >= 3.8
- Ansible >= 2.12
- ALPACA Operator >= 5.6.0

### Support Matrix

<!-- support-matrix:start -->

|             | Ansible 2.12.* | Ansible 2.13.* | Ansible 2.14.* | Ansible 2.15.* | Ansible 2.16.* | Ansible 2.17.* |
| ----------- | -------------- | -------------- | -------------- | -------------- | -------------- | -------------- |
| Python 3.8 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| Python 3.9 | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ |
| Python 3.10 | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Python 3.11 | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| Python 3.12 | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ |

<!-- support-matrix:end -->

### Legend

| Symbol | Meaning                                               |
| ------ | ----------------------------------------------------- |
| ✅     | Tested and **supported**                              |
| ❌     | Tested and **unsupported** (failed)                   |
| ⬜     | **Not tested** (e.g. unsupported version combination) |

## Installation

You can install this collection from Ansible Galaxy:

```bash
ansible-galaxy collection install pcg.alpaca_operator
```

Or directly from the Git repository:

```bash
ansible-galaxy collection install git+https://github.com/pcg-sap/alpaca-operator-ansible.git
```

### Quick Start Guide

For a complete setup guide including Ansible installation, collection setup, and first playbook execution, see the [Quick Start Guide](docs/QUICK_START.md).

## Example Usage

### Group Management

```yaml
- name: Ensure group "ansible_testing_group_01" exists
  alpaca_group:
    name: ansible_testing_group_01
    state: present
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

- name: Delete group ansible_testing_group_01
  alpaca_group:
    name: ansible_testing_group_01
    state: absent
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"
```

### Agent Management

```yaml
- name: Ensure agent "ansible_testing_agent_01" exists
  alpaca_agent:
    name: ansible_testing_agent_01
    description: My Test Agent 01
    ipAddress: 10.1.1.1
    location: virtual
    escalation:
      failuresBeforeReport: 1
      mailEnabled: False
      mailAddress: monitoring_1@pcg.io
      smsEnabled: True
      smsAddress: 0123456789
    scriptGroupId: -1
    state: present
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

- name: Delete agent ansible_testing_agent_01
  alpaca_agent:
    name: ansible_testing_agent_01
    state: absent
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"
```

### System Management

```yaml
- name: Ensure system "ansible01" exists
  alpaca_system:
    name: ansible01
    description: Ansible Test System 01
    magicNumber: 59
    checksDisabled: False
    groupName: ansible_testing_group_01
    rfcConnection:
      type: instance
      host: ansible01-host
      instanceNumber: 42
      sid: ABC
      logonGroup: ansible01-lgroup
      username: rfc_myUser
      password: rfc_myPasswd
      client: 123
      sapRouterString: rfc_SAPRouter
      sncEnabled: False
    agents:
      - name: ansible_testing_agent_01
      - name: ansible_testing_agent_02
      - name: ansible_testing_agent_03
    variables:
      - name: <BKP_DATA_CLEANUP_INT>
        value: "400"
      - name: <BKP_DATA_DEST1>
        value: this is a string
      - name: <BKP_DATA_DEST2>
        value: "11"
    state: present
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

- name: Delete system ansible01
  alpaca_system:
    name: ansible01
    state: absent
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"
```

### System Command Management

**Warning**

⚠️ When using the `alpaca_command_set` module, all existing commands on the target system that are not included in your playbook will be deleted. Use this module with care!

```yaml
- name: Ensure that exactly these system commands exist — no more, no fewer
  alpaca_command_set:
    system:
      systemName: ansible01
    commands:
      - name: "BKP: DB log sync 1"
        state: present
        agentName: ansible_testing_agent_01
        parameters: "-p GLTarch -s <BKP_LOG_SRC> -l 4 -d <BKP_LOG_DEST1> -r <BKP_LOG_DEST2> -b <BKP_LOG_CLEANUP_INT> -t <BKP_LOG_CLEANUP_INT2> -h DB_HOST"
        processCentralId: 8990048
        schedule:
          period: manually
          time: "11:11:11"
          cronExpression: ""
          daysOfWeek:
            - monday
            - sunday
        parametersNeeded: false
        disabled: true
        critical: true
        history:
          documentAllRuns: false
          retention: 100
        autoDeploy: false
        timeout:
          type: custom
          value: 10
        escalation:
          mailEnabled: true
          smsEnabled: true
          mailAddress: "monitoring_1@pcg.io"
          smsAddress: "0123456789-1"
          minFailureCount: 1
          triggers:
            everyChange: true
            toRed: false
            toYellow: false
            toGreen: true
      - name: "BKP: DB log sync 2"
        state: present
        agentName: ansible_testing_agent_02
        parameters: "-p GLTarch -s <BKP_LOG_SRC> -l 4 -d <BKP_LOG_DEST1> -r <BKP_LOG_DEST2> -b <BKP_LOG_CLEANUP_INT> -t <BKP_LOG_CLEANUP_INT2> -h DB_HOST"
        processId: 801
        schedule:
          period: manually
          time: "12:12:12"
          cronExpression: ""
          daysOfWeek:
            - monday
            - wednesday
            - friday
            - sunday
        parametersNeeded: false
        disabled: true
        critical: true
        history:
          documentAllRuns: false
          retention: 200
        autoDeploy: false
        timeout:
          type: custom
          value: 20
        escalation:
          mailEnabled: true
          smsEnabled: true
          mailAddress: "monitoring_2@pcg.io"
          smsAddress: "0123456789-2"
          minFailureCount: 2
          triggers:
            everyChange: true
            toRed: false
            toYellow: false
            toGreen: true

- name: Ensure a specific system command exist
  alpaca_command:
    system:
      systemName: ansible01
    command:
      name: "BKP: DB log sync 3"
      state: present
      agentName: ansible_testing_agent_03
      parameters: "-p GLTarch -s <BKP_LOG_SRC> -l 4 -d <BKP_LOG_DEST1> -r <BKP_LOG_DEST2> -b <BKP_LOG_CLEANUP_INT> -t <BKP_LOG_CLEANUP_INT2> -h DB_HOST"
      processId: 801
      processCentralId: 8990048
      schedule:
        period: manually
        time: "13:13:13"
        cronExpression: ""
        daysOfWeek:
          - monday
          - sunday
          - wednesday
      parametersNeeded: false
      disabled: true
      critical: true
      history:
        documentAllRuns: false
        retention: 300
      autoDeploy: false
        timeout:
          type: custom
          value: 30
      escalation:
        mailEnabled: true
        smsEnabled: true
        mailAddress: "monitoring_3@pcg.io"
        smsAddress: "0123456789-3"
        minFailureCount: 3
        triggers:
          everyChange: true
          toRed: false
          toYellow: false
          toGreen: true
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

- name: Delete all commands in system ansible01
  alpaca_command_set:
    system:
      systemName: ansible01
    commands: []
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

- name: Delete a specific command
  pcg.alpaca_operator.alpaca_command:
    system:
      systemName: ansible01
    command:
      name: "BKP: DB log sync 3"
      agentName: "ansible_testing_agent_03"
      state: absent
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"
```