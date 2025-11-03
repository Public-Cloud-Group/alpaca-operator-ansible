#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# Apache License, Version 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: alpaca_command_set

short_description: Manage all ALPACA Operator commands of a specific system via REST API

version_added: '1.0.0'

description: >
    This Ansible module manages an entire set of ALPACA Operator commands associated with a system using a REST API. It is designed to apply bulk changes, for example, deploying multiple commands at once or cleaning up an existing command set.
    Use this module when you need to apply or remove multiple commands at once on a given ALPACA system. It simplifies large-scale system updates and is optimal for automation scenarios.
    Important: This module takes full control of the command set on the target system. Any commands not defined via Ansible will be removed from the system!

options:
    system:
        description: Dictionary containing system identification. Either `systemId` or `systemName` must be provided.
        version_added: '1.0.0'
        required: true
        type: dict
        suboptions:
            systemId:
                description: Numeric ID of the target system. Optional if O(systemName) is provided.
                version_added: '1.0.0'
                required: false
                type: int
            systemName:
                description: Name of the target system. Optional if O(systemId) is provided.
                version_added: '1.0.0'
                required: false
                type: str
    commands:
        description: >
            List of desired commands to manage. Each command can include fields such as name, agentId or agentName, processId,
            parameters, schedule, history, escalation settings, etc.
        version_added: '1.0.0'
        required: false
        type: list
        elements: dict
        default: []
        suboptions:
            name:
                description: Name or description of the command.
                version_added: '1.0.0'
                required: false
                type: str
            state:
                description: Desired state of the command.
                version_added: '1.0.0'
                required: false
                type: str
                default: present
                choices: [present, absent]
            agentId:
                description: >
                    Numeric ID of the agent. Optional if O(agentName) is provided.
                    Note: This agent must also be assigned to the corresponding system if the system is managed via Ansible.
                version_added: '1.0.0'
                required: false
                type: int
            agentName:
                description: >
                    Name of the agent. Optional if O(agentId) is provided.
                    Note: This agent must also be assigned to the corresponding system if the system is managed via Ansible.
                version_added: '1.0.0'
                required: false
                type: str
            processId:
                description: >
                    ID of the process to be executed. Optional if O(processCentralId) is provided.
                version_added: '1.0.0'
                required: false
                type: int
            processCentralId:
                description: >
                    Central ID / Global ID of the process to be executed. Optional if O(processId) is provided.
                version_added: '1.0.0'
                required: false
                type: int
            parameters:
                description: Parameters for the process.
                version_added: '1.0.0'
                required: false
                type: str
            parametersNeeded:
                description: Whether the execution of the command requires additional parameters.
                version_added: '1.0.0'
                required: false
                type: bool
            disabled:
                description: Whether the command is currently disabled.
                version_added: '1.0.0'
                required: false
                type: bool
            critical:
                description: Whether the command is marked as critical.
                version_added: '1.0.0'
                required: false
                type: bool
            schedule:
                description: Scheduling configuration.
                version_added: '1.0.0'
                required: false
                type: dict
                suboptions:
                    period:
                        description: Scheduling period.
                        version_added: '1.0.0'
                        type: str
                        required: false
                        choices: [every_5min, one_per_day, hourly, manually, fixed_time, hourly_with_mn, every_minute, even_hours_with_mn, odd_hours_with_mn, even_hours, odd_hours, fixed_time_once, fixed_time_immediate, cron_expression, disabled, start_fixed_time_and_hourly_mn]
                    time:
                        description: Execution time in HH:mm:ss. Required when O(period) is V(fixed_time), V(fixed_time_once), or V(start_fixed_time_and_hourly_mn).
                        version_added: '1.0.0'
                        type: str
                        required: false
                    cronExpression:
                        description: Quartz-compatible cron expression. Required when O(period) is V(cron_expression).
                        version_added: '1.0.0'
                        type: str
                        required: false
                    daysOfWeek:
                        description: List of weekdays for execution.
                        version_added: '1.0.0'
                        type: list
                        elements: str
                        required: false
                        choices: [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
            history:
                description: Command history retention settings.
                version_added: '1.0.0'
                required: false
                type: dict
                suboptions:
                    documentAllRuns:
                        description: Whether to document all executions.
                        version_added: '1.0.0'
                        type: bool
                        required: false
                    retention:
                        description: Retention time in seconds.
                        version_added: '1.0.0'
                        type: int
                        required: false
            autoDeploy:
                description: Whether to automatically deploy the command.
                version_added: '1.0.0'
                required: false
                type: bool
            timeout:
                description: Timeout configuration for command execution.
                version_added: '1.0.0'
                required: false
                type: dict
                suboptions:
                    type:
                        description: Type of timeout. Can be V(none), V(default), or V(custom).
                        version_added: '1.0.0'
                        type: str
                        required: false
                        choices: [none, default, custom]
                    value:
                        description: Timeout value in seconds (for V(custom) type).
                        version_added: '1.0.0'
                        type: int
                        required: false
            escalation:
                description: Escalation configuration.
                version_added: '1.0.0'
                required: false
                type: dict
                suboptions:
                    mailEnabled:
                        description: Whether email alerts are enabled.
                        version_added: '1.0.0'
                        type: bool
                        required: false
                    smsEnabled:
                        description: Whether SMS alerts are enabled.
                        version_added: '1.0.0'
                        type: bool
                        required: false
                    mailAddress:
                        description: Email address for alerts.
                        version_added: '1.0.0'
                        type: str
                        required: false
                    smsAddress:
                        description: SMS number for alerts.
                        version_added: '1.0.0'
                        type: str
                        required: false
                    minFailureCount:
                        description: Minimum number of failures before escalation.
                        version_added: '1.0.0'
                        type: int
                        required: false
                    triggers:
                        description: Trigger types for escalation.
                        version_added: '1.0.0'
                        type: dict
                        required: false
                        suboptions:
                            everyChange:
                                description: Currently no description available
                                version_added: '1.0.0'
                                type: bool
                                required: false
                            toRed:
                                description: Currently no description available
                                version_added: '1.0.0'
                                type: bool
                                required: false
                            toYellow:
                                description: Currently no description available
                                version_added: '1.0.0'
                                type: bool
                                required: false
                            toGreen:
                                description: Currently no description available
                                version_added: '1.0.0'
                                type: bool
                                required: false
    apiConnection:
        description: Connection details for accessing the ALPACA Operator API.
        version_added: '1.0.0'
        required: true
        type: dict
        suboptions:
            username:
                description: Username for authentication against the ALPACA Operator API.
                version_added: '1.0.0'
                required: true
                type: str
            password:
                description: Password for authentication against the ALPACA Operator API.
                version_added: '1.0.0'
                required: true
                type: str
            protocol:
                description: Protocol to use. Can be V(http) or V(https).
                version_added: '1.0.0'
                required: false
                default: https
                choices: [http, https]
                type: str
            host:
                description: Hostname of the ALPACA Operator server.
                version_added: '1.0.0'
                required: false
                default: localhost
                type: str
            port:
                description: Port of the ALPACA Operator API.
                version_added: '1.0.0'
                required: false
                default: 8443
                type: int
            tls_verify:
                description: Validate SSL certificates.
                version_added: '1.0.0'
                required: false
                default: true
                type: bool
author:
    - Jan-Karsten Hansmeyer (@pcg)
'''

EXAMPLES = r'''
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
'''

RETURN = r'''
msg:
    description: Status message
    returned: always
    type: str
    version_added: '1.0.0'
    sample: One or multiple commands have been created, updated or deleted in system 42

changed:
    description: Whether any change was made
    returned: always
    type: bool
    version_added: '1.0.0'

changes:
    description: >
        A dictionary describing all changes that were or would be applied. Keys typically follow the format
        `commandIndex_XXX`, representing the index in the `commands` list. Each entry includes diffs between
        the current and desired state. Also includes `removed_commands` if commands were deleted.
    returned: when changes are detected (or would be applied in check_mode)
    type: dict
    version_added: '1.0.0'
    contains:
        commandIndex_000:
            description: >
                Diff of the command at index 0. Contains changed fields with current and desired values.
            type: dict
            sample: {
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
            }

        removed_commands:
            description: >
                List of commands that were removed because they were not included in the desired state.
            type: list
            elements: dict
            sample:
              - id: 123
                name: "Old Command"
                processId: 456
                agentHostname: "my-agent-01"
'''

from ansible_collections.pcg.alpaca_operator.plugins.module_utils._alpaca_api import api_call, get_token, lookup_resource, lookup_processId
from ansible.module_utils.basic import AnsibleModule


def build_payload(desired_command, system_command):
    """
    Constructs a configuration payload by prioritizing values from the desired configuration
    dictionary. If a value is not provided in the desired configuration, the function falls
    back to using the corresponding value from the existing configuration (if available).

    Parameters:
        desired_command (dict): A dictionary containing the desired configuration values.
        system_command (dict): A dictionary with existing configuration values.

    Returns:
        dict: A combined configuration payload dictionary.
    """

    payload = {
        "name":                 desired_command.get('name', None)                                                                                                                               if desired_command.get('name')                                                                                                                                              is not None else system_command.get('name', None),
        "agentId":              desired_command.get('agentId', None)                                                                                                                            if desired_command.get('agentId')                                                                                                                                           is not None else system_command.get('agentId', 0),
        "processId":            desired_command.get('processId', None)                                                                                                                          if desired_command.get('processId')                                                                                                                                         is not None else system_command.get('processId', 0),
        "parameters":           desired_command.get('parameters', None)                                                                                                                         if desired_command.get('parameters')                                                                                                                                        is not None else system_command.get('parameters', None),
        "schedule": {
            "period":           desired_command.get('schedule', {}).get('period', None)                                                                                                         if desired_command.get('schedule', {}).get('period', None)                                                                                                                  is not None else system_command.get('schedule', {}).get('period', 'undefined'),
            "time":             desired_command.get('schedule', {}).get('time', None)                                                                                                           if desired_command.get('schedule', {}).get('time', None)                                                                                                                    is not None else system_command.get('schedule', {}).get('time', None),
            "cronExpression":   desired_command.get('schedule', {}).get('cronExpression', None)                                                                                                 if desired_command.get('schedule', {}).get('cronExpression', None) and desired_command.get('schedule', {}).get('period', None) == 'cron_expression'                                     else system_command.get('schedule', {}).get('cronExpression', ''),
            "daysOfWeek":       sorted(
                                    desired_command.get('schedule', {}).get('daysOfWeek', [])                                                                                                   if desired_command.get('schedule', {}).get('daysOfWeek', None)                                                                                                              is not None else system_command.get('schedule', {}).get('daysOfWeek', []),
                                    key=lambda x: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(x.lower())
                                )
        },
        "parametersNeeded":     desired_command.get('parametersNeeded', None)                                                                                                                   if desired_command.get('parametersNeeded')                                                                                                                                  is not None else system_command.get('parametersNeeded', True),
        "disabled":             desired_command.get('disabled', None)                                                                                                                           if desired_command.get('disabled')                                                                                                                                          is not None else system_command.get('disabled', True),
        "critical":             desired_command.get('critical', None)                                                                                                                           if desired_command.get('critical')                                                                                                                                          is not None else system_command.get('critical', True),
        "history": {
            "documentAllRuns":  desired_command.get('history', {}).get('documentAllRuns', None)                                                                                                 if desired_command.get('history', {}).get('documentAllRuns', None)                                                                                                          is not None else system_command.get('history', {}).get('documentAllRuns', True),
            "retention":        desired_command.get('history', {}).get('retention', None)                                                                                                       if desired_command.get('history', {}).get('retention', None)                                                                                                                is not None else system_command.get('history', {}).get('retention', 0)
        },
        "autoDeploy":           desired_command.get('autoDeploy', None)                                                                                                                         if desired_command.get('autoDeploy')                                                                                                                                        is not None else system_command.get('autoDeploy', True),
        "timeout": {
            "type":             desired_command.get('timeout', {}).get('type', None).upper()                                                                                                    if desired_command.get('timeout', {}).get('type', None)                                                                                                                     is not None else system_command.get('timeout', {}).get('type', 'None').upper(),
            "value":            desired_command.get('timeout', {}).get('value', None)                                                                                                           if desired_command.get('timeout', {}).get('value', None)                                                                                                                    is not None else system_command.get('timeout', {}).get('value', 0)
        },
        "escalation": {
            "mailEnabled":      desired_command.get('escalation', {}).get('mailEnabled', None)                                                                                                  if desired_command.get('escalation', {}).get('mailEnabled', None)                                                                                                           is not None else system_command.get('escalation', {}).get('mailEnabled', False),
            "smsEnabled":       desired_command.get('escalation', {}).get('smsEnabled', None)                                                                                                   if desired_command.get('escalation', {}).get('smsEnabled', None)                                                                                                            is not None else system_command.get('escalation', {}).get('smsEnabled', False),
            "mailAddress":      desired_command.get('escalation', {}).get('mailAddress', None)                                                                                                  if desired_command.get('escalation', {}).get('mailAddress', None)                                                                                                           is not None else system_command.get('escalation', {}).get('mailAddress', None),
            "smsAddress":       desired_command.get('escalation', {}).get('smsAddress', None)                                                                                                   if desired_command.get('escalation', {}).get('smsAddress', None)                                                                                                            is not None else system_command.get('escalation', {}).get('smsAddress', None),
            "minFailureCount":  desired_command.get('escalation', {}).get('minFailureCount', None)                                                                                              if desired_command.get('escalation', {}).get('minFailureCount', None)                                                                                                       is not None else system_command.get('escalation', {}).get('minFailureCount', 0),
            "triggers": {
                "everyChange":  desired_command.get('escalation', {}).get('triggers', {}).get('everyChange', None)                                                                              if desired_command.get('escalation', {}).get('triggers', {}).get('everyChange', None)                                                                                       is not None else system_command.get('escalation', {}).get('triggers', {}).get('everyChange', True),
                "toRed":        desired_command.get('escalation', {}).get('triggers', {}).get('toRed', None)                                                                                    if desired_command.get('escalation', {}).get('triggers', {}).get('toRed', None)                                                                                             is not None else system_command.get('escalation', {}).get('triggers', {}).get('toRed', True),
                "toYellow":     desired_command.get('escalation', {}).get('triggers', {}).get('toYellow', None)                                                                                 if desired_command.get('escalation', {}).get('triggers', {}).get('toYellow', None)                                                                                          is not None else system_command.get('escalation', {}).get('triggers', {}).get('toYellow', True),
                "toGreen":      desired_command.get('escalation', {}).get('triggers', {}).get('toGreen', None)                                                                                  if desired_command.get('escalation', {}).get('triggers', {}).get('toGreen', None)                                                                                           is not None else system_command.get('escalation', {}).get('triggers', {}).get('toGreen', True)
            }
        }
    }

    if payload.get('timeout', {}).get('type') == 'NONE' or payload.get('timeout', {}).get('type') == 'DEFAULT':
        payload['timeout']['value'] = None

    return payload


def main():
    module = AnsibleModule(
        argument_spec=dict(
            system=dict(
                type='dict',
                required=True,
                options=dict(
                    systemId=dict(type='int', required=False),
                    systemName=dict(type='str', required=False)
                )
            ),
            commands=dict(
                type='list',
                required=False,
                default=[],
                elements='dict',
                options=dict(
                    name=dict(type='str', required=False),
                    state=dict(type='str', required=False, default='present', choices=['present', 'absent']),
                    agentId=dict(type='int', required=False),
                    agentName=dict(type='str', required=False),
                    processId=dict(type='int', required=False),
                    processCentralId=dict(type='int', required=False),
                    parameters=dict(type='str', required=False),
                    schedule=dict(
                        type='dict',
                        required=False,
                        options=dict(
                            period=dict(type='str', required=False, choices=[
                                'every_5min', 'one_per_day', 'hourly', 'manually', 'fixed_time',
                                'hourly_with_mn', 'every_minute', 'even_hours_with_mn', 'odd_hours_with_mn',
                                'even_hours', 'odd_hours', 'fixed_time_once', 'fixed_time_immediate',
                                'cron_expression', 'disabled', 'start_fixed_time_and_hourly_mn'
                            ]),
                            time=dict(type='str', required=False),
                            cronExpression=dict(type='str', required=False),
                            daysOfWeek=dict(type='list', required=False, elements='str', choices=[
                                'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
                            ])
                        )
                    ),
                    parametersNeeded=dict(type='bool', required=False),
                    disabled=dict(type='bool', required=False),
                    critical=dict(type='bool', required=False),
                    history=dict(
                        type='dict',
                        required=False,
                        options=dict(
                            documentAllRuns=dict(type='bool', required=False),
                            retention=dict(type='int', required=False)
                        )
                    ),
                    autoDeploy=dict(type='bool', required=False),
                    timeout=dict(
                        type='dict',
                        required=False,
                        options=dict(
                            type=dict(type='str', required=False, choices=[
                                'none', 'default', 'custom'
                            ]),
                            value=dict(type='int', required=False)
                        )
                    ),
                    escalation=dict(
                        type='dict',
                        required=False,
                        options=dict(
                            mailEnabled=dict(type='bool', required=False),
                            smsEnabled=dict(type='bool', required=False),
                            mailAddress=dict(type='str', required=False),
                            smsAddress=dict(type='str', required=False),
                            minFailureCount=dict(type='int', required=False),
                            triggers=dict(
                                type='dict',
                                required=False,
                                options=dict(
                                    everyChange=dict(type='bool', required=False),
                                    toRed=dict(type='bool', required=False),
                                    toYellow=dict(type='bool', required=False),
                                    toGreen=dict(type='bool', required=False)
                                )
                            )
                        )
                    )
                )
            ),
            apiConnection=dict(
                type='dict',
                required=True,
                options=dict(
                    host=dict(type='str', required=False, default='localhost'),
                    port=dict(type='int', required=False, default='8443'),
                    protocol=dict(type='str', required=False, default='https', choices=['http', 'https']),
                    username=dict(type='str', required=True, no_log=True),
                    password=dict(type='str', required=True, no_log=True),
                    tls_verify=dict(type='bool', required=False, default=True)
                )
            )
        ),
        supports_check_mode=True,
    )

    api_url = "{0}://{1}:{2}/api".format(module.params['apiConnection']['protocol'], module.params['apiConnection']['host'], module.params['apiConnection']['port'])
    token = get_token(api_url, module.params['apiConnection']['username'], module.params['apiConnection']['password'], module.params['apiConnection']['tls_verify'])
    headers = {"Authorization": "Bearer {0}".format(token)}
    desired_commands = [command for command in module.params['commands'] if command.get('state') == 'present']
    diffs = {}
    removed = []

    # Check if either a system ID or a system name is provided
    if not module.params['system'].get('systemName', None) and not module.params['system'].get('systemId', None):
        module.fail_json(msg="Either a systemName or systemId must be provided")

    # Resolve system id if needed
    if module.params['system'].get('systemName', None):
        system = lookup_resource(api_url, headers, "systems", "name", module.params['system']['systemName'], module.params['apiConnection']['tls_verify'])
        if not system and desired_commands:
            module.fail_json(msg="System '{0}' not found".format(module.params['system']['systemName']))
        module.params['system']['systemId'] = system['id'] if system else None

    # Check if systemId is valid
    if module.params['system'].get('systemId', None):
        system = lookup_resource(api_url, headers, "systems", "id", module.params['system']['systemId'], module.params['apiConnection']['tls_verify'])
        if not system and desired_commands:
            module.fail_json(msg="System with ID '{0}' not found - Please ensure system is created first".format(module.params['system']['systemId']))

    # Get currently configured system commands
    system_commands = {}
    if module.params['system'].get('systemId', None):
        # system_commands = api_call("GET", "{0}/systems/{1}/commands".format(api_url, module.params['system']['systemId']), headers=headers, verify=module.params['apiConnection']['tls_verify']).json()                                        # unsorted list
        system_commands = sorted(api_call("GET", "{0}/systems/{1}/commands".format(api_url, module.params['system']['systemId']), headers=headers, verify=module.params['apiConnection']['tls_verify']).json(), key=lambda x: x.get("id", 0))    # sorted by id

    # Delete excess commands
    desired_commands_count = len([cmd for cmd in module.params['commands'] if cmd.get('state') == 'present'])
    if len(system_commands) > desired_commands_count:
        start_index = desired_commands_count
        for index in range(start_index, len(system_commands)):
            command = system_commands[index]
            command_id = command.get('id')
            if command_id is not None:
                api_call("DELETE", "{0}/systems/{1}/commands/{2}".format(api_url, module.params['system']['systemId'], command_id), headers=headers, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to delete excess command with id {0}".format(command_id))
                removed.append({"id": command_id, "name": command.get("name"), "processId": command.get("processId"), "agentHostname": command.get("agentHostname")})

    # Add removed commands to diffs for logging
    if removed:
        diffs["removed_commands"] = removed
        # Update list of currently configured system commands
        # system_commands = sorted(api_call("GET", "{0}/systems/{1}/commands".format(api_url, module.params['system']['systemId']), headers=headers, verify=module.params['apiConnection']['tls_verify']).json(), key=lambda x: x.get("id", 0)) # sorted by id

    for desired_command_index, desired_command in enumerate(desired_commands):

        # Check if either an agent ID or a agent name is provided
        if not desired_command.get('agentName', None) and not desired_command.get('agentId', None):
            module.fail_json(msg="Either agentName or agentId must be provided")

        # Resolve agent id if needed
        if desired_command.get('agentName', None):
            agent = lookup_resource(api_url, headers, "agents", "hostname", desired_command['agentName'], module.params['apiConnection']['tls_verify'])
            if not agent:
                module.fail_json(msg="Agent '{0}' defined in system command index {1} not found".format(desired_command['agentName'], desired_command_index))
            desired_command['agentId'] = agent['id']

        # Check if agentId is valid
        if desired_command.get('agentId', None):
            agent = lookup_resource(api_url, headers, "agents", "id", desired_command['agentId'], module.params['apiConnection']['tls_verify'])
            if not agent:
                module.fail_json(msg="Agent with ID '{0}' defined in system command index {1} not found - Please ensure agent is created first".format(desired_command['agentId'], desired_command_index))

        # Check if either a process ID or the processes central ID is provided
        if not desired_command.get('processCentralId', None) and not desired_command.get('processId', None):
            module.fail_json(msg="Either processCentralId or processId must be provided")

        # Resolve processId if needed
        if desired_command.get('processCentralId', None) and not desired_command.get('processId', None):
            processId = lookup_processId(api_url, headers, "globalId", desired_command['processCentralId'], module.params['apiConnection']['tls_verify'])
            if not processId:
                module.fail_json(msg="Process ID lookup for Central ID '{0}' defined in system command index {1} not found".format(desired_command['processCentralId'], desired_command_index))
            desired_command['processId'] = processId

        # Get currently configured system command at the same index as the desired command defined in ansible yaml
        try:
            system_command = api_call("GET", "{0}/systems/{1}/commands/{2}".format(api_url, module.params['system']['systemId'], system_commands[desired_command_index]['id']), headers=headers, verify=module.params['apiConnection']['tls_verify']).json()
        except Exception:
            system_command = {}

        # Create command payload (for comparison and later use)
        command_payload = build_payload(desired_command, system_command)

        if system_command:
            # Compare current command configuration with the desired command configuration if it already exists
            diff = {}
            for key in command_payload:
                if key not in ['schedule', 'history', 'escalation', 'timeout']:
                    if command_payload.get(key, None) != system_command.get(key, None):
                        diff[key] = {
                            'current': system_command.get(key, None),
                            'desired': command_payload.get(key, None)
                        }
                if key in ['schedule', 'history', 'escalation', 'timeout']:
                    for sub_key in command_payload.get(key, {}):
                        if sub_key not in ['triggers']:
                            if command_payload.get(key, {}).get(sub_key, None) != system_command.get(key, {}).get(sub_key, None):
                                if key not in diff:
                                    diff[key] = {}
                                diff[key][sub_key] = {
                                    'current': system_command.get(key, {}).get(sub_key, None),
                                    'desired': command_payload.get(key, {}).get(sub_key, None)
                                }
                        if sub_key in ['triggers']:
                            for sub_sub_key in command_payload.get(key, {}).get(sub_key, {}):
                                if command_payload.get(key, {}).get(sub_key, None).get(sub_sub_key, {}) != system_command.get(key, {}).get(sub_key, {}).get(sub_sub_key, None):
                                    if key not in diff:
                                        diff[key] = {}
                                    if sub_key not in diff.get(key, {}):
                                        diff[key][sub_key] = {}
                                    diff[key][sub_key][sub_sub_key] = {
                                        'current': system_command.get(key, {}).get(sub_key, {}).get(sub_sub_key, None),
                                        'desired': command_payload.get(key, {}).get(sub_key, {}).get(sub_sub_key, None)
                                    }

            if diff:
                diffs['commandIndex_{0:03d}'.format(desired_command_index)] = diff
                if not module.check_mode:
                    # Update command
                    api_call("PUT", "{0}/systems/{1}/commands/{2}".format(api_url, module.params['system']['systemId'], system_command['id']), headers=headers, json=command_payload, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to update command {0}".format(system_command['id']))

        else:
            # Create command if it does not exist already
            diffs['commandIndex_{0:03d}'.format(desired_command_index)] = {'new_command_payload': command_payload}
            if not module.check_mode:
                api_call("POST", "{0}/systems/{1}/commands".format(api_url, module.params['system']['systemId']), headers=headers, json=command_payload, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to create command")

    if diffs:
        if module.check_mode:
            module.exit_json(changed=True, msg="One or multiple commands would be created, updated or deleted in system {0}".format(module.params['system']['systemId']), changes=diffs)

        module.exit_json(changed=True, msg="One or multiple commands have been created, updated or deleted in system {0}".format(module.params['system']['systemId']), changes=diffs)

    module.exit_json(changed=False, msg="Command state processed")


if __name__ == '__main__':
    main()
