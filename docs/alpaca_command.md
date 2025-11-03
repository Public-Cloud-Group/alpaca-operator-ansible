# ALPACA Command Module

## Overview

The `pcg.alpaca_operator.alpaca_command` module manages a single ALPACA Operator command. It provides fine-grained control over individual command properties. Use this module when you need to configure or modify one specific command, such as changing its timeout, toggling disabled, or setting a new schedule.

Each command is uniquely identified by the combination of its name (description) and the assigned agentHostname. Note that renaming a command or reassigning it to a different agent is not supported by this module, as these properties are used for identification.

## Module Information

- **Module Name**: `pcg.alpaca_operator.alpaca_command`
- **Short Description**: Manage a single ALPACA Operator command via REST API
- **Version Added**: 1.0.0
- **Requirements**:
  - Python >= 3.8
  - ansible-core >= 2.12
  - ALPACA Operator >= 5.6.0

## Update Behavior

If the desired command already exists, only the fields required for unique identification need to be provided (i.e., either systemId or systemName, and either agentId or agentName). Any options not explicitly set in the module call or the playbook will retain their existing values from the current configuration.

## Parameters

### Required Parameters

| Parameter       | Type | Required | Description                                                                                      |
| --------------- | ---- | -------- | ------------------------------------------------------------------------------------------------ |
| `system`        | dict | Yes      | Dictionary containing system identification. Either `systemId` or `systemName` must be provided. |
| `command`       | dict | Yes      | Definition of the desired command                                                                |
| `apiConnection` | dict | Yes      | Connection details for accessing the ALPACA Operator API                                         |

### System Identification

The `system` parameter accepts a dictionary with the following sub-options:

| Parameter    | Type | Required | Description                                                            |
| ------------ | ---- | -------- | ---------------------------------------------------------------------- |
| `systemId`   | int  | No*      | Numeric ID of the target system. Optional if `systemName` is provided. |
| `systemName` | str  | No*      | Name of the target system. Optional if `systemId` is provided.         |

*Either `systemId` or `systemName` must be provided.

### Command Configuration

The `command` parameter accepts a dictionary with the following sub-options:

| Parameter          | Type | Required | Default | Description                                                                                |
| ------------------ | ---- | -------- | ------- | ------------------------------------------------------------------------------------------ |
| `name`             | str  | No       | -       | Name or description of the command                                                         |
| `state`            | str  | No       | present | Desired state of the command (present, absent)                                             |
| `agentId`          | int  | No       | -       | Numeric ID of the agent. Optional if `agentName` is provided.                              |
| `agentName`        | str  | No       | -       | Name of the agent. Optional if `agentId` is provided.                                      |
| `processId`        | int  | No       | -       | ID of the process to be executed. Optional if `processCentralId` is provided.              |
| `processCentralId` | int  | No       | -       | Central ID / Global ID of the process to be executed. Optional if `processId` is provided. |
| `parameters`       | str  | No       | -       | Parameters for the process                                                                 |
| `parametersNeeded` | bool | No       | -       | Whether the execution of the command requires additional parameters                        |
| `disabled`         | bool | No       | -       | Whether the command is currently disabled                                                  |
| `critical`         | bool | No       | -       | Whether the command is marked as critical                                                  |
| `autoDeploy`       | bool | No       | -       | Whether to automatically deploy the command                                                |

### Schedule Configuration

The `schedule` parameter accepts a dictionary with the following sub-options:

| Parameter        | Type | Required | Description                                                                                                             |
| ---------------- | ---- | -------- | ----------------------------------------------------------------------------------------------------------------------- |
| `period`         | str  | No       | Scheduling period                                                                                                       |
| `time`           | str  | No       | Execution time in HH:mm:ss. Required when period is 'fixed_time', 'fixed_time_once' or 'start_fixed_time_and_hourly_mn' |
| `cronExpression` | str  | No       | Quartz-compatible cron expression. Required when period is 'cron_expression'                                            |
| `daysOfWeek`     | list | No       | List of weekdays for execution                                                                                          |

**Period Choices**: every_5min, one_per_day, hourly, manually, fixed_time, hourly_with_mn, every_minute, even_hours_with_mn, odd_hours_with_mn, even_hours, odd_hours, fixed_time_once, fixed_time_immediate, cron_expression, disabled, start_fixed_time_and_hourly_mn

**Days of Week Choices**: monday, tuesday, wednesday, thursday, friday, saturday, sunday

### History Configuration

The `history` parameter accepts a dictionary with the following sub-options:

| Parameter         | Type | Required | Description                        |
| ----------------- | ---- | -------- | ---------------------------------- |
| `documentAllRuns` | bool | No       | Whether to document all executions |
| `retention`       | int  | No       | Retention time in seconds          |

### Timeout Configuration

The `timeout` parameter accepts a dictionary with the following sub-options:

| Parameter | Type | Required | Description                                |
| --------- | ---- | -------- | ------------------------------------------ |
| `type`    | str  | No       | Type of timeout (none, default, or custom) |
| `value`   | int  | No       | Timeout value in seconds (for custom type) |

**Type Choices**: none, default, custom

### Escalation Configuration

The `escalation` parameter accepts a dictionary with the following sub-options:

| Parameter         | Type | Required | Description                                  |
| ----------------- | ---- | -------- | -------------------------------------------- |
| `mailEnabled`     | bool | No       | Whether email alerts are enabled             |
| `smsEnabled`      | bool | No       | Whether SMS alerts are enabled               |
| `mailAddress`     | str  | No       | Email address for alerts                     |
| `smsAddress`      | str  | No       | SMS number for alerts                        |
| `minFailureCount` | int  | No       | Minimum number of failures before escalation |
| `triggers`        | dict | No       | Trigger types for escalation                 |

### Escalation Triggers

The `triggers` parameter accepts a dictionary with the following sub-options:

| Parameter     | Type | Required | Description                        |
| ------------- | ---- | -------- | ---------------------------------- |
| `everyChange` | bool | No       | Currently no description available |
| `toRed`       | bool | No       | Currently no description available |
| `toYellow`    | bool | No       | Currently no description available |
| `toGreen`     | bool | No       | Currently no description available |

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

### Create a Command

```yaml
- name: Ensure a specific system command exist
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
    - name: Create command
      pcg.alpaca_operator.alpaca_command:
        system:
          systemName: system01
        command:
          name: "BKP: DB log sync"
          state: present
          agentName: agent01
          parameters: "-p GLTarch -s <BKP_LOG_SRC> -l 4 -d <BKP_LOG_DEST1> -r <BKP_LOG_DEST2> -b <BKP_LOG_CLEANUP_INT> -t <BKP_LOG_CLEANUP_INT2> -h DB_HOST"
          processCentralId: 8990048
          schedule:
            period: manually
            time: "01:00:00"
            daysOfWeek:
              - monday
              - sunday
          parametersNeeded: false
          disabled: false
          critical: true
          history:
            documentAllRuns: true
            retention: 900
          autoDeploy: false
          timeout:
            type: default
            value: 30
          escalation:
            mailEnabled: true
            smsEnabled: true
            mailAddress: "monitoring@pcg.io"
            smsAddress: "0123456789"
            minFailureCount: 1
            triggers:
              everyChange: true
              toRed: false
              toYellow: false
              toGreen: true
        apiConnection: "{{ apiConnection }}"
```

### Delete a Command

```yaml
- name: Delete a specific command
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
    - name: Delete command
      pcg.alpaca_operator.alpaca_command:
        system:
          systemName: system01
        command:
          name: "BKP: DB log sync"
          agentName: agent01
          state: absent
        apiConnection: "{{ apiConnection }}"
```

## Return Values

| Parameter | Type | Returned                                  | Description                                                                                 |
| --------- | ---- | ----------------------------------------- | ------------------------------------------------------------------------------------------- |
| `msg`     | str  | always                                    | Status message describing what the module did                                               |
| `changed` | bool | always                                    | Whether any changes were made                                                               |
| `changes` | dict | when changes are detected                 | Dictionary containing the differences between the current and desired command configuration |
| `payload` | dict | when state is present and change occurred | Full payload that would be sent to the API (in check_mode) or that was sent (when changed)  |

### Return Value Examples

#### Command Update with Changes

```json
{
  "msg": "Command updated in system 42.",
  "changed": true,
  "changes": {
    "parameters": {
      "current": "-p foo -s A -d B",
      "desired": "-p foo -s A -d B -t X"
    },
    "schedule": {
      "period": {
        "current": "manually",
        "desired": "every_minute"
      }
    },
    "escalation": {
      "minFailureCount": {
        "current": 0,
        "desired": 1
      }
    }
  }
}
```

## Notes

- The module supports check mode for previewing changes without applying them
- Commands are uniquely identified by name and agent assignment
- Renaming commands or reassigning to different agents is not supported
- When updating existing commands, only specified fields are modified
- The agent must be assigned to the corresponding system if managed via Ansible
- Schedule configurations support various periodic execution patterns
- Escalation settings can be configured for both email and SMS notifications
- API connection variables should be stored in the inventory file and referenced via `apiConnection: "{{ apiConnection }}"` in playbooks

## Author

- Jan-Karsten Hansmeyer (@pcg)