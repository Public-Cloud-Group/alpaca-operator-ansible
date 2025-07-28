# ALPACA Command Set Module

## Overview

The `alpaca_command_set` module manages an entire set of ALPACA Operator commands associated with a system using a REST API. It is designed to apply bulk changes, for example, deploying multiple commands at once or cleaning up an existing command set.

Use this module when you need to apply or remove multiple commands at once on a given ALPACA system. It simplifies large-scale system updates and is optimal for automation scenarios.

**Important**: This module takes full control of the command set on the target system. Any commands not defined via Ansible will be removed from the system!

## Module Information

- **Module Name**: `alpaca_command_set`
- **Short Description**: Manage all ALPACA Operator commands of a specific system via REST API
- **Version Added**: 1.0.0
- **Requirements**:
  - Python >= 3.8
  - Ansible >= 2.12
  - ALPACA Operator >= 5.6.0

## Parameters

### Required Parameters

| Parameter       | Type | Required | Description                                                                                      |
| --------------- | ---- | -------- | ------------------------------------------------------------------------------------------------ |
| `system`        | dict | Yes      | Dictionary containing system identification. Either `systemId` or `systemName` must be provided. |
| `apiConnection` | dict | Yes      | Connection details for accessing the ALPACA Operator API                                         |

### Optional Parameters

| Parameter  | Type | Required | Default | Description                        |
| ---------- | ---- | -------- | ------- | ---------------------------------- |
| `commands` | list | No       | []      | List of desired commands to manage |

### System Identification

The `system` parameter accepts a dictionary with the following sub-options:

| Parameter    | Type | Required | Description                                                            |
| ------------ | ---- | -------- | ---------------------------------------------------------------------- |
| `systemId`   | int  | No*      | Numeric ID of the target system. Optional if `systemName` is provided. |
| `systemName` | str  | No*      | Name of the target system. Optional if `systemId` is provided.         |

*Either `systemId` or `systemName` must be provided.

### Command Configuration

The `commands` parameter accepts a list of dictionaries, where each dictionary can include the following fields:

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

### Configure Multiple Commands

```yaml
- name: Ensure that multiple commands are configured correctly on system01
  alpaca_command_set:
    system:
      systemName: system01
    commands:
      - name: "BKP: DB log sync"
        state: present
        agentName: agent01
        parameters: "-p GLTarch -s <BKP_LOG_SRC> -l 4 -d <BKP_LOG_DEST1> -r <BKP_LOG_DEST2> -b <BKP_LOG_CLEANUP_INT> -t <BKP_LOG_CLEANUP_INT2> -h DB_HOST"
        processId: 801
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
      - name: "BKP: DB log sync 2"
        state: present
        agentName: agent02
        parameters: "-p GLTarch -s <BKP_LOG_SRC> -l 4 -d <BKP_LOG_DEST1> -r <BKP_LOG_DEST2> -b <BKP_LOG_CLEANUP_INT> -t <BKP_LOG_CLEANUP_INT2> -h DB_HOST"
        processId: 801
        schedule:
          period: cron_expression
          cronExpression: '0 */5 * * * ?'
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
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: false
```

### Remove All Commands

```yaml
- name: Remove all commands from system system01
  alpaca_command_set:
    system:
      systemName: system01
    commands: []
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: false
```

## Return Values

| Parameter | Type | Returned                  | Description                                                       |
| --------- | ---- | ------------------------- | ----------------------------------------------------------------- |
| `msg`     | str  | always                    | Status message                                                    |
| `changed` | bool | always                    | Whether any change was made                                       |
| `changes` | dict | when changes are detected | A dictionary describing all changes that were or would be applied |

### Changes Dictionary Structure

The `changes` dictionary typically follows the format `commandIndex_XXX`, representing the index in the `commands` list. Each entry includes diffs between the current and desired state. Also includes `removed_commands` if commands were deleted.

#### Example Changes Structure

```json
{
  "commandIndex_000": {
    "parameters": {
      "current": "-p foo -s A -d B",
      "desired": "-p foo -s A -d B -t X"
    },
    "schedule": {
      "period": {
        "current": "manually",
        "desired": "every_minute"
      }
    }
  },
  "commandIndex_001": {
    "escalation": {
      "minFailureCount": {
        "current": 0,
        "desired": 1
      }
    }
  },
  "removed_commands": [
    "Old Command Name 1",
    "Old Command Name 2"
  ]
}
```

## Notes

- **Critical Warning**: This module takes full control of the command set. Any commands not defined in the `commands` list will be removed from the system.
- The module supports check mode for previewing changes without applying them
- Commands are uniquely identified by name and agent assignment
- When updating existing commands, only specified fields are modified
- The agent must be assigned to the corresponding system if managed via Ansible
- Schedule configurations support various periodic execution patterns including cron expressions
- Escalation settings can be configured for both email and SMS notifications
- Use this module for bulk operations rather than individual command management
- Empty commands list will remove all commands from the system

## Author

- Jan-Karsten Hansmeyer (@pcg)