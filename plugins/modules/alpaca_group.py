#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# Apache License, Version 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: alpaca_group

short_description: Manage ALPACA Operator groups via REST API

version_added: '1.0.0'

description: This module allows you to create, rename or delete ALPACA Operator groups using the REST API.

options:
    name:
        description: Name of the group.
        version_added: '1.0.0'
        required: true
        type: str
    new_name:
        description: >
            Optional new name for the group. If the group specified in `name` exists,
            it will be renamed to this value. If the group does not exist, a new group will
            be created using this value.
        version_added: '1.0.0'
        required: false
        type: str
    state:
        description: Desired state of the group.
        version_added: '1.0.0'
        required: false
        default: present
        choices: [present, absent]
        type: str
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
                description: Protocol to use (http or https).
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

requirements:
    - Python >= 3.6
    - Ansible >= 2.11, < 2.17
    - ALPACA Operator >= 5.5.1 instance reachable via API

author:
    - Jan-Karsten Hansmeyer (@pcg)
'''

EXAMPLES = r'''
- name: Ensure group exists
  alpaca_groups:
    name: testgroup01
    state: present
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: false

- name: Ensure group is absent
  alpaca_groups:
    name: testgroup01
    state: absent
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: false

- name: Rename an existing group
  alpaca_groups:
    name: testgroup01
    new_name: testgroup_renamed
    state: present
    apiConnection:
      host: localhost
      port: 8443
      protocol: https
      username: secret
      password: secret
      tls_verify: false
'''

RETURN = r'''
changed:
    description: Indicates whether any change was made to the group.
    version_added: '1.0.0'
    returned: always
    type: bool
    sample: true

msg:
    description: Human-readable message describing the outcome.
    version_added: '1.0.0'
    returned: always
    type: str
    sample: Group created

id:
    description: Numeric ID of the group (if known or newly created).
    version_added: '1.0.0'
    returned: when state is present or absent and group exists
    type: int
    sample: 42

name:
    description: Name of the group (new or existing).
    version_added: '1.0.0'
    returned: always
    type: str
    sample: testgroup01
'''

from ansible_collections.pcg.alpaca_operator.plugins.module_utils._alpaca_api import get_token
from ansible.module_utils.basic import AnsibleModule


def find_group(api_url, headers, name, verify):
    """Find group by name"""
    try:
        import requests
        response = requests.get("{0}/groups".format(api_url), headers=headers, verify=verify)
        response.raise_for_status()
        for group in response.json():
            if group["name"] == name:
                return group
    except ImportError:
        raise
    return None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            new_name=dict(type='str', required=False),
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

    name = module.params['name']
    new_name = module.params.get('new_name')
    state = module.params['state']
    api_host = module.params['apiConnection']['host']
    api_port = module.params['apiConnection']['port']
    api_protocol = module.params['apiConnection']['protocol']
    api_username = module.params['apiConnection']['username']
    api_password = module.params['apiConnection']['password']
    api_tls_verify = module.params['apiConnection']['tls_verify']
    api_url = "{0}://{1}:{2}/api".format(api_protocol, api_host, api_port)
    api_token = get_token(api_url, api_username, api_password, api_tls_verify)

    headers = {"Authorization": "Bearer {0}".format(api_token)}
    group = find_group(api_url, headers, name, api_tls_verify)

    try:
        import requests
    except ImportError:
        module.fail_json(msg="Python module 'requests' could not be found")

    if state == 'present':
        if group:
            # If renaming is requested and name differs, perform update
            if new_name and new_name != name:
                if module.check_mode:
                    module.exit_json(changed=True, msg="Group would be renamed", id=group["id"], name=new_name)

                if not find_group(api_url, headers, new_name, api_tls_verify):
                    response = requests.put("{0}/groups/{1}".format(api_url, group["id"]), headers=headers, verify=api_tls_verify, json={"name": new_name})

                    if response.status_code not in [200]:
                        module.fail_json(msg="Failed to rename group: {0}".format(response.text))

                    module.exit_json(changed=True, msg="Group renamed", id=group["id"], name=new_name)

            # No changes needed
            module.exit_json(changed=False, msg="Group already exists", id=group["id"], name=group["name"])

        # Create the group if it doesn't exist
        if new_name:
            name = new_name

        if not find_group(api_url, headers, name, api_tls_verify):
            if module.check_mode:
                module.exit_json(changed=True, msg="Group would be created", name=name)

            response = requests.post("{0}/groups".format(api_url), headers=headers, verify=api_tls_verify, json={"name": name})
            response.raise_for_status()
            module.exit_json(changed=True, msg="Group created", id=response.json()["id"], name=name)

        module.exit_json(changed=False, msg="Group already exists", name=name)

    if state == 'absent':
        if not group:
            module.exit_json(changed=False, msg="Group does not exist", name=name)
        if module.check_mode:
            module.exit_json(changed=True, msg="Group would be deleted", id=group["id"], name=name)

        group_id = group["id"]
        response = requests.delete("{0}/groups/{1}".format(api_url, group_id), headers=headers, verify=api_tls_verify)

        if response.status_code not in [204]:
            module.fail_json(msg="Failed to delete group: {0}".format(response.text))
        module.exit_json(changed=True, msg="Group deleted", id=group["id"], name=name)


if __name__ == '__main__':
    main()
