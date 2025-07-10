#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# <!-- License --!>

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: alpaca_agent

short_description: Manage ALPACA Operator agents via REST API

version_added: '1.0.0'

description: This module allows you to create, update or delete ALPACA Operator agents using the REST API.

options:
    name:
        description: Unique name (hostname) of the agent
        version_added: '1.0.0'
        required: true
        type: str
    new_name:
        description: >
            Optional new name for the agent. If the agent specified in `name` exists,
            it will be renamed to this value. If the agent does not exist, a new agent will
            be created using this value.
        version_added: '1.0.0'
        required: false
        type: str
    description:
        description: Unique description of the agent
        version_added: '1.0.0'
        required: false
        type: str
    escalation:
        description: Escalation configuration
        version_added: '1.0.0'
        required: false
        type: dict
        suboptions:
            failuresBeforeReport:
                description: Number of failures before reporting
                version_added: '1.0.0'
                required: false
                type: int
                default: 0
            mailEnabled:
                description: Whether mail notification is enabled
                version_added: '1.0.0'
                required: false
                type: bool
                default: false
            mailAddress:
                description: Mail address for notifications
                version_added: '1.0.0'
                required: false
                type: str
                default: ""
            smsEnabled:
                description: Whether SMS notification is enabled
                version_added: '1.0.0'
                required: false
                type: bool
                default: false
            smsAddress:
                description: SMS address for notifications
                version_added: '1.0.0'
                required: false
                type: str
                default: ""
    ipAddress:
        description: IP address of the agent
        version_added: '1.0.0'
        required: false
        type: str
    location:
        description: Location of the agent (virtual, local1, local2, remote)
        version_added: '1.0.0'
        required: false
        type: str
        choices: [virtual, local1, local2, remote]
        default: virtual
    scriptGroupId:
        description: Script Group ID
        version_added: '1.0.0'
        required: false
        type: int
        default: -1
    state:
        description: Desired state of the agent
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
- name: Ensure agent exists
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
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: False

- name: Ensure agent is absent
  alpaca_agent:
    name: agent01
    state: absent
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: False

- name: Rename an existing agent
  alpaca_agent:
    name: agent01
    new_name: agent_renamed
    state: present
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: False
'''

RETURN = r'''
msg:
    description: Status message indicating the result of the operation.
    returned: always
    type: str
    version_added: '1.0.0'
    sample: Agent created

changed:
    description: Indicates whether any change was made.
    returned: always
    type: bool
    version_added: '1.0.0'
    sample: true

agent_config:
    description: Details of the created, updated, or deleted agent configuration.
    returned: when state is present or absent
    type: dict
    version_added: '1.0.0'
    sample:
        id: 7
        hostname: "testagent"
        description: "Test agent"
        ipAddress: "10.1.1.1"
        location: "virtual"
        scriptGroupId: 2
        escalation:
            failuresBeforeReport: 3
            mailEnabled: true
            mailAddress: "monitoring@pcg.io"
            smsEnabled: false
            smsAddress: ""

changes:
    description: Dictionary showing differences between the current and desired configuration.
    returned: when state is present and a change occurred
    type: dict
    version_added: '1.0.0'
    sample:
        ipAddress:
            current: "10.1.1.1"
            desired: "10.1.1.2"
        escalation:
            mailEnabled:
                current: false
                desired: true
'''

from ansible_collections.pcg.alpaca_operator.plugins.module_utils._alpaca_api import api_call, get_token, lookup_resource
from ansible.module_utils.basic import AnsibleModule


def build_payload(desired_agent_config, current_agent_config):
    """
    Constructs a configuration payload by prioritizing values from the desired configuration
    dictionary. If a value is not provided in the desired configuration, the function falls
    back to using the corresponding value from the existing configuration (if available).

    Parameters:
        desired_agent_config (dict): A dictionary containing the desired configuration values.
        current_agent_config (dict): A dictionary with existing configuration values.

    Returns:
        dict: A combined configuration payload dictionary.
    """

    payload = {
        "description":              desired_agent_config.get('description', None)                                           if desired_agent_config.get('description', None)                                            is not None else current_agent_config.get('description', ''),
        "escalation": {
            "failuresBeforeReport": desired_agent_config.get('escalation', {}).get('failuresBeforeReport', None)            if desired_agent_config.get('escalation', {}).get('failuresBeforeReport', None)             is not None else current_agent_config.get('escalation', {}).get('failuresBeforeReport', 0),
            "mailAddress":          desired_agent_config.get('escalation', {}).get('mailAddress', None)                     if desired_agent_config.get('escalation', {}).get('mailAddress', None)                      is not None else current_agent_config.get('escalation', {}).get('mailAddress', ''),
            "mailEnabled":          desired_agent_config.get('escalation', {}).get('mailEnabled', None)                     if desired_agent_config.get('escalation', {}).get('mailEnabled', None)                      is not None else current_agent_config.get('escalation', {}).get('mailEnabled', False),
            "smsAddress":           desired_agent_config.get('escalation', {}).get('smsAddress', None)                      if desired_agent_config.get('escalation', {}).get('smsAddress', None)                       is not None else current_agent_config.get('escalation', {}).get('smsAddress', ''),
            "smsEnabled":           desired_agent_config.get('escalation', {}).get('smsEnabled', None)                      if desired_agent_config.get('escalation', {}).get('smsEnabled', None)                       is not None else current_agent_config.get('escalation', {}).get('smsEnabled', False),
        },
        "hostname":                 desired_agent_config.get('new_name', None) or desired_agent_config.get('name', None)    if desired_agent_config.get('new_name', None) or desired_agent_config.get('name', None)     is not None else current_agent_config.get('hostname', ''),
        "ipAddress":                desired_agent_config.get('ipAddress', None)                                             if desired_agent_config.get('ipAddress', None)                                              is not None else current_agent_config.get('ipAddress', ''),
        "location":                 desired_agent_config.get('location', None)                                              if desired_agent_config.get('location', None)                                               is not None else current_agent_config.get('location', 'virtual'),
        "scriptGroupId":            desired_agent_config.get('scriptGroupId', None)                                         if desired_agent_config.get('scriptGroupId', None)                                          is not None else current_agent_config.get('scriptGroupId', -1),
    }

    return payload


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),       # = hostname
            new_name=dict(type='str', required=False),  # = hostname
            description=dict(type='str', required=False),
            escalation=dict(type='dict', required=False, default={}),
            ipAddress=dict(type='str', required=False),
            location=dict(type='str', required=False, choices=['virtual', 'local1', 'local2', 'remote']),
            scriptGroupId=dict(type='int', required=False),
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
    current_agent = lookup_resource(api_url, headers, "agents", "hostname", module.params['name'], module.params['apiConnection']['tls_verify']) or lookup_resource(api_url, headers, "agents", "hostname", module.params['new_name'], module.params['apiConnection']['tls_verify'])
    current_agent_config = api_call(method="GET", url="{0}/agents/{1}".format(api_url, current_agent.get('id', None)), headers=headers, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to get current agent configuration").json() if current_agent else {}
    agent_payload = build_payload(module.params, current_agent_config)
    diff = {}

    if module.params['state'] == 'present':
        if current_agent:
            # Compare current agent configuration with the desired agent configuration if it already exists
            for key in agent_payload:
                if key not in ['escalation']:
                    if agent_payload.get(key, None) != current_agent_config.get(key, None):
                        diff[key] = {
                            'current': current_agent_config.get(key, None),
                            'desired': agent_payload.get(key, None)
                        }
                if key in ['escalation']:
                    for sub_key in agent_payload.get(key, {}):
                        if agent_payload.get(key, {}).get(sub_key, None) != current_agent_config.get(key, {}).get(sub_key, None):
                            if key not in diff:
                                diff[key] = {}
                            diff[key][sub_key] = {
                                'current': current_agent_config.get(key, {}).get(sub_key, None),
                                'desired': agent_payload.get(key, {}).get(sub_key, None)
                            }

            if diff:
                if module.check_mode:
                    module.exit_json(changed=True, msg="Agent would be updated", changes=diff)

                # Update agent
                current_agent_config = api_call("PUT", "{0}/agents/{1}".format(api_url, current_agent['id']), headers=headers, json=agent_payload, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to update agent").json()
                module.exit_json(changed=True, msg="Agent updated", agent_config=current_agent_config, changes=diff)

        elif not current_agent:
            if module.check_mode:
                module.exit_json(changed=True, msg="Agent would be created", agent_config=agent_payload)

            # Create the agent if it doesn't exist
            current_agent_config = api_call("POST", "{0}/agents".format(api_url), headers=headers, json=agent_payload, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to create agent").json()
            module.exit_json(changed=True, msg="Agent created", agent_config=current_agent_config)

        module.exit_json(changed=False, msg="Agent already exists with the desired configuration", agent_config=current_agent_config)

    elif module.params['state'] == 'absent':
        if not current_agent:
            module.exit_json(changed=False, msg="Agent already absent")

        if module.check_mode:
            module.exit_json(changed=True, msg="Agent would be deleted", agent_config=current_agent_config)

        api_call("DELETE", "{0}/agents/{1}".format(api_url, current_agent['id']), headers=headers, verify=module.params['apiConnection']['tls_verify'], module=module, fail_msg="Failed to delete agent")
        module.exit_json(changed=True, msg="Agent deleted", agent_config=current_agent_config)

    module.exit_json(changed=True, msg="Agent state processed")


if __name__ == '__main__':
    main()
