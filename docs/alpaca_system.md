# ALPACA System Module

## Overview

The `alpaca_system` module allows you to create, update, or delete ALPACA Operator systems using the REST API. In addition to general system properties, it supports assigning agents and variables. Communication is handled using token-based authentication.

## Module Information

- **Module Name**: `alpaca_system`
- **Short Description**: Manage ALPACA Operator systems via REST API
- **Version Added**: 1.0.0
- **Requirements**:
  - Python >= 3.8
  - Ansible >= 2.12
  - ALPACA Operator >= 5.6.0

## Parameters

### Required Parameters

| Parameter       | Type | Required | Description                                              |
| --------------- | ---- | -------- | -------------------------------------------------------- |
| `name`          | str  | Yes      | Unique name (hostname) of the system                     |
| `apiConnection` | dict | Yes      | Connection details for accessing the ALPACA Operator API |

### Optional Parameters

| Parameter        | Type | Required | Default | Description                                                                                                                                                                                                                                                               |
| ---------------- | ---- | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `new_name`       | str  | No       | -       | Optional new name for the system. If the system specified in `name` exists, it will be renamed to this value. If the system does not exist, a new system will be created using this value.                                                                                |
| `description`    | str  | No       | -       | Description of the system                                                                                                                                                                                                                                                 |
| `magicNumber`    | int  | No       | -       | Custom numeric field between 0 and 59. Can be used for arbitrary logic in your setup                                                                                                                                                                                      |
| `checksDisabled` | bool | No       | -       | Disable automatic system health checks                                                                                                                                                                                                                                    |
| `groupName`      | str  | No       | -       | Name of the group to which the system should belong                                                                                                                                                                                                                       |
| `groupId`        | int  | No       | -       | ID of the group (used if `groupName` is not provided)                                                                                                                                                                                                                     |
| `rfcConnection`  | dict | No       | -       | Connection details for RFC communication                                                                                                                                                                                                                                  |
| `agents`         | list | No       | -       | A list of agents to assign to the system                                                                                                                                                                                                                                  |
| `variables`      | list | No       | -       | A list of variables to assign to the system                                                                                                                                                                                                                               |
| `variables_mode` | str  | No       | update  | Controls how variables are handled when updating the system (update, replace). The value `update` adds missing variables and updates existing ones. The value `replace` adds missing variables, updates existing ones, and removes variables not defined in the playbook. |
| `state`          | str  | No       | present | Desired state of the system (present, absent)                                                                                                                                                                                                                             |

### Magic Number Choices

The `magicNumber` parameter accepts values from 0 to 59.

### RFC Connection Configuration

The `rfcConnection` parameter accepts a dictionary with the following sub-options:

| Parameter         | Type | Required | Description                                            |
| ----------------- | ---- | -------- | ------------------------------------------------------ |
| `type`            | str  | No       | Type of RFC connection (none, instance, messageServer) |
| `host`            | str  | No       | Hostname or IP address of the RFC target system        |
| `instanceNumber`  | int  | No       | Instance number of the RFC connection (0-99)           |
| `sid`             | str  | No       | SAP system ID (SID), consisting of 3 uppercase letters |
| `logonGroup`      | str  | No       | Logon group (used with message server type)            |
| `username`        | str  | No       | Username for RFC connection                            |
| `password`        | str  | No       | Password for the RFC connection                        |
| `client`          | str  | No       | Client for RFC connection                              |
| `sapRouterString` | str  | No       | SAProuter string used to establish the RFC connection  |
| `sncEnabled`      | bool | No       | Enable or disable SNC                                  |

**Type Choices**: none, instance, messageServer

**Instance Number Choices**: 0-99

### Agent Assignment

The `agents` parameter accepts a list of dictionaries, where each dictionary must include:

| Parameter | Type | Required | Description       |
| --------- | ---- | -------- | ----------------- |
| `name`    | str  | Yes      | Name of the agent |

### Variable Assignment

The `variables` parameter accepts a list of dictionaries, where each dictionary must include:

| Parameter | Type | Required | Description                     |
| --------- | ---- | -------- | ------------------------------- |
| `name`    | str  | Yes      | Name of the variable            |
| `value`   | raw  | Yes      | Value to assign to the variable |

### API Connection Configuration

The `apiConnection` parameter requires a dictionary with the following sub-options:

| Parameter    | Type | Required | Default   | Description                                                 |
| ------------ | ---- | -------- | --------- | ----------------------------------------------------------- |
| `username`   | str  | Yes      | -         | Username for authentication against the ALPACA Operator API |
| `password`   | str  | Yes      | -         | Password for authentication against the ALPACA Operator API |
| `protocol`   | str  | No       | https     | Protocol to use (http or https)                             |
| `host`       | str  | No       | localhost | Hostname of the ALPACA Operator server                      |
| `port`       | int  | No       | 8443      | Port of the ALPACA Operator API                             |
| `tls_verify` | bool | No       | true      | Validate SSL certificates                                   |

## Examples

### Create a System with Full Configuration

```yaml
- name: Ensure system exists
  hosts: local
  gather_facts: false

  vars:
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

  tasks:
    - name: Create system
      alpaca_system:
        name: system01
        description: My Test System
        magicNumber: 42
        checksDisabled: false
        groupName: test-group
        rfcConnection:
          type: instance
          host: test-host
          instanceNumber: 30
          sid: ABC
          logonGroup: my-logon-group
          username: rfc_myUser
          password: rfc_myPasswd
          client: 123
          sapRouterString: rfc_SAPRouter
          sncEnabled: false
        agents:
          - name: localhost
          - name: testjan01-agent
        variables:
          - name: "<BKP_DATA_CLEANUP_INT>"
            value: "19"
          - name: "<BKP_DATA_CLEANUP_INT2>"
            value: "this is a string"
          - name: "<BKP_DATA_DEST2>"
            value: "11"
        state: present
        apiConnection: "{{ apiConnection }}"
```

### Delete a System

```yaml
- name: Ensure system is absent
  hosts: local
  gather_facts: false

  vars:
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

  tasks:
    - name: Delete system
      alpaca_system:
        name: system01
        state: absent
        apiConnection: "{{ apiConnection }}"
```

### Rename a System

```yaml
- name: Rename an existing system
  hosts: local
  gather_facts: false

  vars:
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

  tasks:
    - name: Rename system
      alpaca_system:
        name: system01
        new_name: system_renamed
        apiConnection: "{{ apiConnection }}"
```

### Create a System with RFC Connection Only

```yaml
- name: Create system with RFC connection
  hosts: local
  gather_facts: false

  vars:
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

  tasks:
    - name: Create SAP system
      alpaca_system:
        name: sap-system-01
        description: SAP Production System
        rfcConnection:
          type: instance
          host: sap-prod-server
          instanceNumber: 00
          sid: PRD
          username: rfc_user
          password: rfc_password
          client: 100
        state: present
        apiConnection: "{{ apiConnection }}"
```

### Create a System with Variables Only

```yaml
- name: Create system with variables
  hosts: local
  gather_facts: false

  vars:
    apiConnection:
      host: "{{ ALPACA_Operator_API_Host }}"
      protocol: "{{ ALPACA_Operator_API_Protocol }}"
      port: "{{ ALPACA_Operator_API_Port }}"
      username: "{{ ALPACA_Operator_API_Username }}"
      password: "{{ ALPACA_Operator_API_Password }}"
      tls_verify: "{{ ALPACA_Operator_API_Validate_Certs }}"

  tasks:
    - name: Create configuration system
      alpaca_system:
        name: config-system-01
        description: Configuration System
        variables:
          - name: "BACKUP_PATH"
            value: "/backup/data"
          - name: "RETENTION_DAYS"
            value: "30"
          - name: "ENVIRONMENT"
            value: "production"
        state: present
        apiConnection: "{{ apiConnection }}"
```

## Return Values

| Parameter | Type | Returned              | Description                           |
| --------- | ---- | --------------------- | ------------------------------------- |
| `system`  | dict | when state is present | System details                        |
| `msg`     | str  | always                | Status message describing the outcome |
| `changed` | bool | always                | Whether any changes were made         |

### Return Value Examples

#### Successful System Creation

```json
{
  "system": {
    "id": 42,
    "name": "system01",
    "description": "My Test System",
    "magicNumber": 42,
    "checksDisabled": false,
    "groupName": "test-group",
    "rfcConnection": {
      "type": "instance",
      "host": "test-host",
      "instanceNumber": 30,
      "sid": "ABC"
    },
    "agents": [
      {"name": "localhost"},
      {"name": "testjan01-agent"}
    ],
    "variables": [
      {"name": "<BKP_DATA_CLEANUP_INT>", "value": "19"},
      {"name": "<BKP_DATA_CLEANUP_INT2>", "value": "this is a string"}
    ]
  },
  "msg": "System created successfully",
  "changed": true
}
```

## Notes

- The module supports check mode for previewing changes without applying them
- System names must be unique within the ALPACA Operator environment
- When renaming a system, the new name must not conflict with existing system names
- The `magicNumber` field can be used for custom logic in your setup
- RFC connections support both instance and message server types
- Agent assignments and variable assignments are optional
- The currently configured RFC password cannot be retrieved or compared via the API
- To ensure a new RFC password is applied, you must change at least one additional attribute
- Variables can be of any type (string, integer, boolean, etc.)
- The module uses token-based authentication for API communication
- API connection variables should be stored in the inventory file and referenced via `apiConnection: "{{ apiConnection }}"` in playbooks

## Author

- Jan-Karsten Hansmeyer (@pcg)