# ALPACA Agent Module

## Overview

The `alpaca_agent` module allows you to create, update, or delete ALPACA Operator agents using the REST API. This module provides comprehensive management capabilities for ALPACA Operator agents, including configuration of escalation settings, location settings, and other agent-specific properties.

## Module Information

- **Module Name**: `alpaca_agent`
- **Short Description**: Manage ALPACA Operator agents via REST API
- **Version Added**: 1.0.0
- **Requirements**:
  - Python >= 3.8
  - ansible-core >= 2.12
  - ALPACA Operator >= 5.6.0

## Parameters

### Required Parameters

| Parameter       | Type | Required | Description                                              |
| --------------- | ---- | -------- | -------------------------------------------------------- |
| `name`          | str  | Yes      | Unique name (hostname) of the agent                      |
| `apiConnection` | dict | Yes      | Connection details for accessing the ALPACA Operator API |

### Optional Parameters

| Parameter       | Type | Required | Default | Description                                                                                                                                                                            |
| --------------- | ---- | -------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `new_name`      | str  | No       | -       | Optional new name for the agent. If the agent specified in `name` exists, it will be renamed to this value. If the agent does not exist, a new agent will be created using this value. |
| `description`   | str  | No       | -       | Unique description of the agent                                                                                                                                                        |
| `escalation`    | dict | No       | -       | Escalation configuration                                                                                                                                                               |
| `ipAddress`     | str  | No       | -       | IP address of the agent                                                                                                                                                                |
| `location`      | str  | No       | virtual | Location of the agent (virtual, local1, local2, remote)                                                                                                                                |
| `scriptGroupId` | int  | No       | -1      | Script Group ID                                                                                                                                                                        |
| `state`         | str  | No       | present | Desired state of the agent (present, absent)                                                                                                                                           |

### Escalation Configuration

The `escalation` parameter accepts a dictionary with the following sub-options:

| Parameter              | Type | Required | Default | Description                          |
| ---------------------- | ---- | -------- | ------- | ------------------------------------ |
| `failuresBeforeReport` | int  | No       | 0       | Number of failures before reporting  |
| `mailEnabled`          | bool | No       | false   | Whether mail notification is enabled |
| `mailAddress`          | str  | No       | ""      | Mail address for notifications       |
| `smsEnabled`           | bool | No       | false   | Whether SMS notification is enabled  |
| `smsAddress`           | str  | No       | ""      | SMS address for notifications        |

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

### Create an Agent

```yaml
- name: Ensure agent exists
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
    - name: Create agent
      alpaca_agent:
        name: agent01
        ipAddress: 192.168.1.100
        location: virtual
        description: Test agent
        escalation:
          failuresBeforeReport: 3
          mailEnabled: true
          mailAddress: my.mail@pcg.io
          smsEnabled: true
          smsAddress: 0123456789
        scriptGroupId: 0
        state: present
        apiConnection: "{{ apiConnection }}"
```

### Delete an Agent

```yaml
- name: Ensure agent is absent
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
    - name: Delete agent
      alpaca_agent:
        name: agent01
        state: absent
        apiConnection: "{{ apiConnection }}"
```

### Rename an Agent

```yaml
- name: Rename an existing agent
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
    - name: Rename agent
      alpaca_agent:
        name: agent01
        new_name: agent_renamed
        state: present
        apiConnection: "{{ apiConnection }}"
```

## Return Values

| Parameter      | Type | Returned                                    | Description                                                                  |
| -------------- | ---- | ------------------------------------------- | ---------------------------------------------------------------------------- |
| `msg`          | str  | always                                      | Status message indicating the result of the operation                        |
| `changed`      | bool | always                                      | Indicates whether any change was made                                        |
| `agent_config` | dict | when state is present or absent             | Details of the created, updated, or deleted agent configuration              |
| `changes`      | dict | when state is present and a change occurred | Dictionary showing differences between the current and desired configuration |

### Return Value Examples

#### Successful Agent Creation

```json
{
  "msg": "Agent created",
  "changed": true,
  "agent_config": {
    "id": 7,
    "hostname": "testagent",
    "description": "Test agent",
    "ipAddress": "10.1.1.1",
    "location": "virtual",
    "scriptGroupId": 2,
    "escalation": {
      "failuresBeforeReport": 3,
      "mailEnabled": true,
      "mailAddress": "monitoring@pcg.io",
      "smsEnabled": false,
      "smsAddress": ""
    }
  }
}
```

#### Agent Update with Changes

```json
{
  "msg": "Agent updated",
  "changed": true,
  "changes": {
    "ipAddress": {
      "current": "10.1.1.1",
      "desired": "10.1.1.2"
    },
    "escalation": {
      "mailEnabled": {
        "current": false,
        "desired": true
      }
    }
  }
}
```

## Notes

- The module supports check mode for previewing changes without applying them
- Agent names must be unique within the ALPACA Operator environment
- When renaming an agent, the new name must not conflict with existing agent names
- Escalation settings are optional and can be configured independently
- The `scriptGroupId` parameter defaults to -1 if not specified
- Location options include: virtual, local1, local2, remote
- API connection variables should be stored in the inventory file and referenced via `apiConnection: "{{ apiConnection }}"` in playbooks

## Author

- Jan-Karsten Hansmeyer (@pcg)