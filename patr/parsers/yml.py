#!/usr/bin/env python
# pylint: disable=missing-docstring,unused-variable,line-too-long
"""
renders inventory from source format into ansible inventory
"""
from __future__ import print_function
import yaml

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

from patr import utilities

# DEBUG = True
# DEFAULT_DATA_PATH = os.path.join(os.path.abspath(os.getcwd()), 'cluster_map.yml')
# DEFAULT_TPL_PATH = os.path.join(os.path.abspath(os.getcwd()), 'hosts.j2')
# DEFAULT_INVENTORY = os.path.join(os.path.abspath(os.getcwd()), 'default_inventory')
# DEFAULT_RULES_PATH = os.path.join(os.path.dirname(__file__), 'default_rules.yml')


class ParsersYamlError(Exception):
    pass


def parse_yaml_str(data_str):
    data = yaml.safe_load(data_str)
    if not data:
        raise ParsersYamlError("empty data")
    for attr in ('version', 'data',):
        prefix = 'incorrect format of data'
        if attr not in data:
            raise ParsersYamlError("{prefix}: missing attribute '{attr}'".format(prefix=prefix, attr=attr))
        val = data.get(attr, '')
        if not val:
            raise ParsersYamlError("{prefix}: improperly set attribute '{attr}'".format(prefix=prefix, attr=attr))
    return data


def parse_file_yaml(fpath):
    data_str = utilities.load_data_from_path(fpath)
    return parse_yaml_str(data_str)

