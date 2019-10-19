#!/usr/bin/env python
import pytest
from patr.parsers import yml


def test_yml_parse_yaml_str():
    yaml_str = '''
    '''
    try:
        yml.parse_yaml_str(yaml_str)
        assert False, "Failed to produce exception"
    except yml.ParsersYamlError as val_err:
        assert val_err.args[0] == "empty data"
        assert True
    else:
        assert False, "Failed to produce correct exception."

    yaml_str = '''---
    kuku: 'llala'
    '''
    try:
        yml.parse_yaml_str(yaml_str)
        assert False, "Failed to produce exception"
    except yml.ParsersYamlError as val_err:
        assert val_err.args[0] == "incorrect format of data: missing attribute 'version'"
        assert True
    else:
        assert False, "Failed to produce correct exception."

    yaml_str = '''
    version:
    '''
    try:
        yml.parse_yaml_str(yaml_str)
        assert False, "Failed to produce exception"
    except yml.ParsersYamlError as val_err:
        assert val_err.args[0] == "incorrect format of data: improperly set attribute 'version'"
        assert True
    else:
        assert False, "Failed to produce correct exception."

    yaml_str = '''
    version: '1.0'
    '''
    try:
        yml.parse_yaml_str(yaml_str)
        assert False, "Failed to produce exception"
    except yml.ParsersYamlError as val_err:
        assert val_err.args[0] == "incorrect format of data: missing attribute 'data'"
        assert True
    else:
        assert False, "Failed to produce correct exception."

    yaml_str = '''
    version: '1.0'
    data:
    '''
    try:
        yml.parse_yaml_str(yaml_str)
        assert False, "Failed to produce exception"
    except yml.ParsersYamlError as val_err:
        assert val_err.args[0] == "incorrect format of data: improperly set attribute 'data'"
        assert True
    else:
        assert False, "Failed to produce correct exception."


