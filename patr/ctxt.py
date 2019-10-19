#!/usr/bin/env python
# pylint: disable=missing-docstring,unused-variable,line-too-long
"""
renders inventory from source format into ansible inventory
"""
from __future__ import print_function

import argparse
import csv
import distutils
import os
import sys
import yaml
from jinja2 import Template
PY3 = False
try:
    from collections import OrderedDict
    PY3 = True
except ImportError:
    pass

if not PY3:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        raise

from patr import (
    utilities,
)


def gen_host_entry(hdata):
    if "variables" not in hdata:
        return hdata['name']
    he_list = [hdata['name']]
    variables = hdata['variables']
    for key in variables:
        val = variables[key]
        if isinstance(val, (list, tuple,)):
            val = '"' + str(val) + '"'
        he_list.append('='.join([key, val]))
    result = ' '.join(he_list)
    return result


def build_context(data):
    groups = None
    customer_roles = None
    customer_name = data.get('customer_name', 'customer')
    for host in data['data']:
        hentry = gen_host_entry(host)
        for hgroup in host.get('groups', []):
            key = hgroup
            groups = utilities.update_src_dict(key, hentry, src_dict=groups)
        for role in host.get('customer_roles', []):
            key = '_'.join([
                customer_name,
                'role',
                role
            ])
            customer_roles = utilities.update_src_dict(key, hentry, src_dict=customer_roles)
    result = {}
    result.update(
        groups=groups,
        customer_roles=customer_roles
    )
    return result
