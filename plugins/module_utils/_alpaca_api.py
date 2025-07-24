# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# Apache License, Version 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)


# This module is for internal use only within the pcg.alpaca_operator collection.
# Python versions supported: 2.7+

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


def api_call(method, url, headers=None, json=None, verify=True, module=None, fail_msg=None):
    """Make API call and handle errors"""
    try:
        import requests
        response = requests.request(method, url, headers=headers, json=json, verify=verify)
        if response.status_code >= 400:
            if module and fail_msg:
                module.fail_json(msg="{0}: {1}".format(fail_msg, response.text))
            response.raise_for_status()
        return response
    except ImportError:
        if module:
            module.fail_json(msg="Python module 'requests' could not be found")
        raise
    except requests.RequestException as e:
        if module:
            module.fail_json(msg="{0}: {1}".format(fail_msg or 'API request failed.', e))
        raise


def get_token(api_url, username, password, verify):
    """Get API token"""
    payload = {"username": username, "password": password}
    response = api_call("POST", "{0}/auth/login".format(api_url), json=payload, verify=verify)
    return response.json()["token"]


def lookup_resource(api_url, headers, resource, key, value, verify):
    """Find resource by the given key and value"""
    response = api_call("GET", "{0}/{1}".format(api_url, resource), headers=headers, verify=verify)
    for resource in response.json():
        if resource.get(key) == value:
            return resource
    return None


def lookup_processId(api_url, headers, key, value, verify):
    """Find processId by the given key and value"""
    response = api_call("GET", "{0}/processes/tree".format(api_url), headers=headers, verify=verify)
    for type in response.json():
        for process in type.get('processes', []):
            if str(process.get(key)) == str(value):
                return process.get('id')
    return None
