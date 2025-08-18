#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# Apache License, Version 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: alpaca_system

short_description: Manage ALPACA Operator systems via REST API

version_added: "1.0.0"

description: >
    This module allows you to create, update or delete ALPACA Operator systems using the REST API.
    In addition to general system properties, it supports assigning agents and variables.
    Communication is handled using token-based authentication.

options:
    name:
        description: Unique name (hostname) of the system
        version_added: '1.0.0'
        required: true
        type: str
    new_name:
        description: >
            Optional new name for the system. If the system specified in `name` exists,
            it will be renamed to this value. If the system does not exist, a new system will
            be created using this value.
        version_added: '1.0.0'
        required: false
        type: str
    description:
        description: Description of the system.
        version_added: '1.0.0'
        required: false
        type: str
    magicNumber:
        description: >
            Custom numeric field between 0 and 59. Can be used for arbitrary logic in your setup.
        version_added: '1.0.0'
        required: false
        type: int
        choices: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
            40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
    checksDisabled:
        description: Disable automatic system health checks.
        version_added: '1.0.0'
        required: false
        type: bool
    groupName:
        description: Name of the group to which the system should belong.
        version_added: '1.0.0'
        required: false
        type: str
    groupId:
        description: ID of the group (used if `groupName` is not provided).
        version_added: '1.0.0'
        required: false
        type: int
    rfcConnection:
        description: Connection details for accessing the ALPACA Operator API
        version_added: '1.0.0'
        required: false
        type: dict
        suboptions:
            type:
                description: Type of RFC connection.
                version_added: '1.0.0'
                required: false
                choices: [none, instance, messageServer]
                type: str
            host:
                description: Hostname or IP address of the RFC target system.
                version_added: '1.0.0'
                required: false
                type: str
            instanceNumber:
                description: Instance number of the RFC connection.
                version_added: '1.0.0'
                required: false
                type: int
                choices: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                    40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                    60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                    80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
            sid:
                description: SAP system ID (SID), consisting of 3 uppercase letters.
                version_added: '1.0.0'
                required: false
                type: str
            logonGroup:
                description: Logon group (used with message server type).
                version_added: '1.0.0'
                required: false
                type: str
            username:
                description: Username for RFC connection.
                version_added: '1.0.0'
                required: false
                type: str
            password:
                description: >
                    Password for the RFC connection. Note that the currently configured password cannot be retrieved or compared via the API.
                    To ensure the new password is actually applied, you must change at least one additional attribute (e.g., the system description),
                    otherwise Ansible will assume no changes are needed and skip the update.
                version_added: '1.0.0'
                required: false
                type: str
            client:
                description: Client for RFC connection.
                version_added: '1.0.0'
                required: false
                type: str
            sapRouterString:
                description: SAProuter string used to establish the RFC connection.
                version_added: '1.0.0'
                required: false
                type: str
            sncEnabled:
                description: Enable or disable SNC.
                version_added: '1.0.0'
                required: false
                type: bool
    agents:
        description: |
            A list of agents to assign to the system.

            Each entry must include:
            - `name` (string): The agent's name.

        version_added: '1.0.0'
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the agent
                version_added: '1.0.0'
                required: true
                type: str
    variables:
        description: |
            A list of variables to assign to the system.

            Each entry must include:
            - `name` (string):  The name of the variable.
            - `value` (string): The value to assign to the variable.

        version_added: '1.0.0'
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of variable
                version_added: '1.0.0'
                required: true
                type: str
            value:
                description: Value of variable
                version_added: '1.0.0'
                required: true
                type: raw
    variables_mode:
        description: |
            Controls how variables are handled when updating the system.

            update: Add missing variables and update existing ones.
            replace: Add missing variables, update existing ones, and remove variables not defined in the playbook.

        version_added: '1.0.0'
        required: false
        default: update
        choices: [update, replace]
        type: str
    state:
        description: Desired state of the system
        version_added: '1.0.0'
        required: false
        default: present
        choices: [present, absent]
        type: str
    apiConnection:
        description: Connection details for accessing the ALPACA Operator API
        version_added: '1.0.0'
        required: true
        type: dict
        suboptions:
            username:
                description: Username for authentication against the ALPACA Operator API
                version_added: '1.0.0'
                required: true
                type: str
            password:
                description: Password for authentication against the ALPACA Operator API
                version_added: '1.0.0'
                required: true
                type: str
            protocol:
                description: Protocol to use (http or https)
                version_added: '1.0.0'
                required: false
                default: https
                choices: [http, https]
                type: str
            host:
                description: Hostname of the ALPACA Operator server
                version_added: '1.0.0'
                required: false
                default: localhost
                type: str
            port:
                description: Port of the ALPACA Operator API
                version_added: '1.0.0'
                required: false
                default: 8443
                type: int
            tls_verify:
                description: Validate SSL certificates
                version_added: '1.0.0'
                required: false
                default: true
                type: bool

requirements:
    - Python >= 3.6
    - Ansible >= 2.11, < 2.17
    - ALPACA Operator >= 5.5.1 instance reachable via API

author:
    - Jan-Karsten Hansmeyer (@pcg)
'''

EXAMPLES = r'''
- name: Ensure system exists
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
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: false

- name: Ensure system is absent
  alpaca_system:
    name: system01
    state: absent
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: false

- name: Rename an existing system
  alpaca_system:
    name: system01
    new_name: system_renamed
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: false
'''

RETURN = r'''
system:
    description: System details
    version_added: '1.0.0'
    type: dict
    returned: when state is present
msg:
    description: Status message
    version_added: '1.0.0'
    type: str
    returned: always
changed:
    description: Whether any change was made
    version_added: '1.0.0'
    type: bool
    returned: always
'''

from ansible_collections.pcg.alpaca_operator.plugins.module_utils._alpaca_api import get_token, api_call, lookup_resource
from ansible.module_utils.basic import AnsibleModule
import re


def get_system_details(api_url, headers, system_id, verify):
    """Get system details by ID"""
    general = api_call("GET", "{0}/systems/{1}".format(api_url, system_id), headers=headers, verify=verify).json()
    agents = api_call("GET", "{0}/systems/{1}/agents".format(api_url, system_id), headers=headers, verify=verify).json()
    variables = api_call("GET", "{0}/systems/{1}/variables".format(api_url, system_id), headers=headers, verify=verify).json()

    # Clean up description: Current workaround for trailing whitespace returned by API --- #0001
    if "description" in general:
        general["description"] = re.sub(r'\s+', ' ', general["description"]).strip()
    # ------------------------------------------------------------------------------------------

    return {"general": general, "agents": agents, "variables": variables}


def build_system_payload(params, current_system_details):
    """
    Constructs a configuration payload by prioritizing values from the desired configuration
    dictionary. If a value is not provided in the desired configuration, the function falls
    back to using the corresponding value from the existing configuration (if available).

    Returns:
        dict: A combined configuration payload dictionary.
    """

    payload = {
        "name":                 params.get('new_name', None) or params.get('name', None),
        "description":          params.get('description', '').strip()                           if params.get('description', None)                              is not None else current_system_details.get('general', {}).get('description', '').strip()                           if current_system_details else None, #0001
        "magicNumber":          params.get('magicNumber', None)                                 if params.get('magicNumber', None)                              is not None else current_system_details.get('general', {}).get('magicNumber', None)                                 if current_system_details else None,
        "schedulingDisabled":   params.get('schedulingDisabled', None)                          if params.get('schedulingDisabled', None)                       is not None else current_system_details.get('general', {}).get('schedulingDisabled', None)                          if current_system_details else None,
        "groupId":              params.get('groupId', None)                                     if params.get('groupId', None)                                  is not None else current_system_details.get('general', {}).get('groupId', None)                                     if current_system_details else None,
        "rfcConnection": {
            "type":             params.get('rfcConnection', {}).get('type', None)               if params.get('rfcConnection', {}).get('type', None)            is not None else current_system_details.get('general', {}).get('rfcConnection', {}).get('type', None)               if current_system_details else None,
            "host":             params.get('rfcConnection', {}).get('host', None)               if params.get('rfcConnection', {}).get('host', None)            is not None else current_system_details.get('general', {}).get('rfcConnection', {}).get('host', None)               if current_system_details else None,
            "instanceNumber":   params.get('rfcConnection', {}).get('instanceNumber', None)     if params.get('rfcConnection', {}).get('instanceNumber', None)  is not None else current_system_details.get('general', {}).get('rfcConnection', {}).get('instanceNumber', None)     if current_system_details else None,
            "sid":              params.get('rfcConnection', {}).get('sid', None)                if params.get('rfcConnection', {}).get('sid', None)             is not None else current_system_details.get('general', {}).get('rfcConnection', {}).get('sid', None)                if current_system_details else None,
            "logonGroup":       params.get('rfcConnection', {}).get('logonGroup', None)         if params.get('rfcConnection', {}).get('logonGroup', None)      is not None else current_system_details.get('general', {}).get('rfcConnection', {}).get('logonGroup', None)         if current_system_details else None,
            "username":         params.get('rfcConnection', {}).get('username', None)           if params.get('rfcConnection', {}).get('username', None)        is not None else current_system_details.get('general', {}).get('rfcConnection', {}).get('username', None)           if current_system_details else None,
            "client":           params.get('rfcConnection', {}).get('client', None)             if params.get('rfcConnection', {}).get('client', None)          is not None else current_system_details.get('general', {}).get('rfcConnection', {}).get('client', None)             if current_system_details else None,
            "sapRouterString":  params.get('rfcConnection', {}).get('sapRouterString', None)    if params.get('rfcConnection', {}).get('sapRouterString', None) is not None else current_system_details.get('general', {}).get('rfcConnection', {}).get('sapRouterString', None)    if current_system_details else None,
            "sncEnabled":       params.get('rfcConnection', {}).get('sncEnabled', None)         if params.get('rfcConnection', {}).get('sncEnabled', None)      is not None else current_system_details.get('general', {}).get('rfcConnection', {}).get('sncEnabled', None)         if current_system_details else None
        }
    }

    # Only include 'password' if its present in params to avoid unwanted emptying #0002
    if params.get('rfcConnection', {}).get('password', None) is not None:
        if 'rfcConnection' not in payload:
            payload['rfcConnection'] = {}
        payload['rfcConnection']['password'] = params['rfcConnection']['password']

    return payload


def build_variable_payload(api_url, headers, module, desired_vars):
    payload = []
    for variable in desired_vars or []:
        api_variable = lookup_resource(api_url, headers, "variables", "name", variable['name'], module.params['apiConnection']['tls_verify'])
        if not api_variable:
            module.fail_json(msg="Variable '{0}' not found. Please ensure variable exists first.".format(variable['name']))

        payload.append({"id": api_variable.get('id'), "value": variable.get('value')})

    return payload


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            new_name=dict(type='str', required=False),
            description=dict(type='str', required=False),
            magicNumber=dict(type='int', required=False, choices=list(range(0, 60))),
            checksDisabled=dict(type='bool', required=False),
            groupId=dict(type='int', required=False),
            groupName=dict(type='str', required=False),
            rfcConnection=dict(
                type='dict',
                required=False,
                options=dict(
                    type=dict(type='str', required=False, choices=["none", "instance", "messageServer"]),
                    host=dict(type='str', required=False),
                    instanceNumber=dict(type='int', required=False, choices=list(range(0, 100))),
                    sid=dict(type='str', required=False),
                    logonGroup=dict(type='str', required=False),
                    username=dict(type='str', required=False, no_log=True),
                    password=dict(type='str', required=False, no_log=True),
                    client=dict(type='str', required=False),
                    sapRouterString=dict(type='str', required=False),
                    sncEnabled=dict(type='bool', required=False),
                )
            ),
            agents=dict(
                type='list',
                elements='dict',
                required=False,
                options=dict(
                    name=dict(type='str', required=True)
                )
            ),
            variables=dict(
                type='list',
                elements='dict',
                required=False,
                options=dict(
                    name=dict(type='str', required=True),
                    value=dict(type='raw', required=True)
                )
            ),
            variables_mode=dict(type='str', required=False, default='update', choices=['update', 'replace']),
            state=dict(type='str', required=False, default='present', choices=['present', 'absent']),
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

    # Validate rfc SID against pattern
    if 'rfcConnection' not in module.params or module.params['rfcConnection'] is None:
        module.params['rfcConnection'] = {}

    try:
        import re
        rfc_sid = module.params.get('rfcConnection', {}).get('sid') if module.params.get('rfcConnection') else None
        if rfc_sid and not re.fullmatch(r'^[A-Z]{3}$', rfc_sid):
            module.fail_json(msg="Invalid value for 'sid'. Must be exactly 3 uppercase letters (A-Z).")
    except ImportError:
        if module:
            module.fail_json(msg="Python module 're' could not be found")
        raise

    current_system = lookup_resource(api_url, headers, "systems", "name", module.params['name'], module.params['apiConnection']['tls_verify'])
    if not current_system and module.params.get('new_name', None):
        current_system = lookup_resource(api_url, headers, "systems", "name", module.params['new_name'], module.params['apiConnection']['tls_verify'])

    system_details = get_system_details(api_url, headers, current_system['id'], module.params['apiConnection']['tls_verify']) if current_system else None

    if module.params['state'] == 'present':
        # Lookup group id if needed
        if module.params.get('groupName'):
            group = lookup_resource(api_url, headers, "groups", "name", module.params['groupName'], module.params['apiConnection']['tls_verify'])
            if not group:
                module.fail_json(msg="Group '{0}' not found.".format(module.params['groupName']))
            module.params['groupId'] = group['id']

        # Check if groupId is valid
        if module.params.get('groupId'):
            group = lookup_resource(api_url, headers, "groups", "id", module.params['groupId'], module.params['apiConnection']['tls_verify'])
            if not group:
                module.fail_json(msg="Group with ID '{0}' not found. Please ensure group is created first.".format(module.params['groupId']))

        # Build payload for general system configuration
        system_payload = build_system_payload(module.params, system_details)

        # Check if system already exists
        if current_system:
            # Compare current system configuration with the desired system configuration if it already exists)
            diff = {}
            for key in system_payload:
                if key not in ['rfcConnection']:
                    if system_payload.get(key, None) != system_details.get('general', {}).get(key, None):
                        if 'general' not in diff:
                            diff['general'] = {}
                        diff['general'][key] = {
                            'current': system_details.get('general', {}).get(key, None),
                            'desired': system_payload.get(key, None)
                        }
                if key in ['rfcConnection']:
                    for sub_key in system_payload.get(key, {}):
                        if sub_key not in ['password']: #0002
                            if system_payload.get(key, {}).get(sub_key, None) != system_details.get('general', {}).get(key, {}).get(sub_key, None):
                                if 'general' not in diff:
                                    diff['general'] = {}
                                if key not in diff['general']:
                                    diff['general'][key] = {}
                                diff['general'][key][sub_key] = {
                                    'current': system_details.get('general', {}).get(key, {}).get(sub_key, None),
                                    'desired': system_payload.get(key, {}).get(sub_key, None)
                                }

            # Check if agent assignments need to be updated
            if 'agents' in module.params and module.params['agents'] is not None:
                desired_agents = sorted([agent['name'] for agent in module.params['agents'] if 'name' in agent]) if module.params.get('agents') else []
                current_agents = sorted([agent['name'] for agent in system_details.get('agents', []) if 'name' in agent])

                if desired_agents != current_agents:
                    diff['agents'] = {
                        'current': current_agents,
                        'desired': desired_agents
                    }

            # Check if variable assignments need to be updated
            if 'variables' in module.params and module.params['variables'] is not None:
                current_vars = sorted(
                    [{"name": v['name'], "value": str(v['value'])} for v in system_details.get('variables', [])],
                    key=lambda x: x['name']
                )

                if module.params['variables_mode'] == 'replace':
                    # Replace mode: use only the variables from module.params
                    desired_vars = sorted(
                        [{"name": v['name'], "value": str(v['value'])} for v in module.params['variables']],
                        key=lambda x: x['name']
                    ) if module.params.get('variables') else []
                else:
                    # Update mode: merge current_vars with module.params['variables'], giving priority to module.params
                    merged_vars = {var['name']: var['value'] for var in current_vars}

                    if module.params.get('variables'):
                        for var in module.params['variables']:
                            merged_vars[var['name']] = str(var['value'])

                    desired_vars = sorted(
                        [{"name": name, "value": value} for name, value in merged_vars.items()],
                        key=lambda x: x['name']
                    )

                if desired_vars != current_vars:
                    diff['variables'] = {
                        'current': current_vars,
                        'desired': desired_vars
                    }

            if diff:
                if module.check_mode:
                    module.exit_json(changed=True, msg="System would be updated.", changes=diff)

                # Update system
                if 'general' in diff:
                    current_system = api_call(method="PUT", url="{0}/systems/{1}".format(api_url, system_details['general']['id']), headers=headers, json=system_payload, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to update system.").json()

                # Update agents
                if 'agents' in diff:
                    # for system_agent in system_details['agents']: (When #0004 is resolved, this part can used again)
                    #     if system_agent['name'] not in desired_agents:
                    #         # Unassign agent if it's not in the desired list
                    #         agent = lookup_resource(api_url, headers, "agents", "hostname", system_agent['name'], module.params['apiConnection']['tls_verify'])
                    #         if not agent:
                    #             module.fail_json(msg="Agent '{0}' not found. Please ensure agent exists.".format(param_agent['name']))
                    #         api_call(method="DELETE", url="{0}/systems/{1}/agents/{2}".format(api_url, current_system['id'], agent['id']), headers=headers, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to unassign agent from system.")

                    # Try to unassign agents as long as needed. Workaround for #0004 ----
                    while True:
                        # Get currently assigned agents
                        current_agents = api_call("GET", "{0}/systems/{1}/agents".format(api_url, current_system['id']), headers=headers, verify=module.params['apiConnection']['tls_verify']).json()

                        # Filter agents that should be unassigned
                        agents_to_remove = [agent for agent in current_agents if agent['name'] not in desired_agents]

                        # Break if there's nothing to remove
                        if not agents_to_remove:
                            break

                        # Unassign agents
                        for agent in agents_to_remove:
                            api_agent = lookup_resource(api_url, headers, "agents", "hostname", agent['name'], module.params['apiConnection']['tls_verify'])
                            if not api_agent:
                                module.fail_json(msg="Agent '{0}' not found. Please ensure agent exists.".format(agent['name']))
                            api_call(method="DELETE", url="{0}/systems/{1}/agents/{2}".format(api_url, current_system['id'], api_agent['id']), headers=headers, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to unassign agent from system.")
                    # End of workaround for #0004 ---------------------------------------

                    # Assign agents
                    if module.params.get('agents'):
                        for agent in module.params.get('agents', []) or []:
                            if agent not in current_agents:
                                # Assign desired agent
                                api_agent = lookup_resource(api_url, headers, "agents", "hostname", agent['name'], module.params['apiConnection']['tls_verify'])
                                if not api_agent:
                                    module.fail_json(msg="Agent '{0}' not found. Please ensure agent exists first.".format(agent['name']))
                                api_call(method="POST", url="{0}/systems/{1}/agents".format(api_url, current_system['id']), headers=headers, json={'id': api_agent['id']}, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to assign agent to system.")

                # Update variables
                if 'variables' in diff:
                    variable_payload = build_variable_payload(api_url, headers, module, desired_vars)
                    api_call(method="POST", url="{0}/systems/{1}/variables".format(api_url, current_system['id']), headers=headers, json=variable_payload, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to assign variables to system.")

                module.exit_json(changed=True, msg="System updated.", api_response=current_system, changes=diff)

            module.exit_json(changed=False, msg="System already exists with the desired configuration", system_details=system_details)

        else:
            if module.check_mode:
                module.exit_json(changed=True, msg="System would be created.")

            # Create system
            current_system = api_call(method="POST", url="{0}/systems".format(api_url), headers=headers, json=system_payload, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to create system.").json()

            # Assign agents
            if module.params.get('agents'):
                for agent in module.params.get('agents', []) or []:
                    # Assign desired agent
                    api_agent = lookup_resource(api_url, headers, "agents", "hostname", agent['name'], module.params['apiConnection']['tls_verify'])
                    if not api_agent:
                        module.fail_json(msg="Agent '{0}' not found. Please ensure agent exists first.".format(agent['name']))
                    api_call(method="POST", url="{0}/systems/{1}/agents".format(api_url, current_system['id']), headers=headers, json={'id': api_agent['id']}, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to assign agent to system.")

            # Assign variables
            variable_payload = build_variable_payload(api_url, headers, module)
            api_call(method="POST", url="{0}/systems/{1}/variables".format(api_url, current_system['id']), headers=headers, json=variable_payload, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to assign variables to system.")

            module.exit_json(changed=True, msg="System created.", api_response=current_system)

    elif module.params['state'] == 'absent':
        if not current_system:
            module.exit_json(changed=False, msg="System already absent.")

        if module.check_mode:
            module.exit_json(changed=True, msg="System would be deleted.", id=current_system['config']["id"])

        # Unassign all agents (When #0004 is resolved, this part can used again)
        # for system_agent in system_details['agents']:
        #     agent = lookup_resource(api_url, headers, "agents", "hostname", system_agent['name'], module.params['apiConnection']['tls_verify'])
        #     if not agent:
        #         module.fail_json(msg="Agent '{0}' not found. Please ensure agent exists.".format(param_agent['name']))
        #     api_call(method="DELETE", url="{0}/systems/{1}/agents/{2}".format(api_url, current_system['id'], agent['id']), headers=headers, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to unassign agent from system")

        # Try to unassign agents as long as needed. Workaround for #0004 ----
        while True:
            agents = api_call("GET", "{0}/systems/{1}/agents".format(api_url, current_system['id']), headers=headers, verify=module.params['apiConnection']['tls_verify']).json()

            if not agents:
                break

            for system_agent in agents:
                agent = lookup_resource(api_url, headers, "agents", "hostname", system_agent['name'], module.params['apiConnection']['tls_verify'])
                if not agent:
                    module.fail_json(msg="Agent '{0}' not found. Please ensure agent exists.".format(system_agent['name']))
                api_call(method="DELETE", url="{0}/systems/{1}/agents/{2}".format(api_url, current_system['id'], agent['id']), headers=headers, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to unassign agent from system")
        # End of workaround for #0004 ---------------------------------------

        # Unassign all variables
        api_call(method="POST", url="{0}/systems/{1}/variables".format(api_url, current_system['id']), headers=headers, json=[], verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to unassign variables from system.")

        # Delete system
        api_call(method="DELETE", url="{0}/systems/{1}".format(api_url, current_system['id']), headers=headers, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to delete system")

        module.exit_json(changed=True, msg="System deleted.", system_details=system_details)

    module.exit_json(changed=True, msg="System state processed.")


if __name__ == '__main__':
    main()
