#!/usr/bin/env python

from patr import cli
import pytest


def test_parse_args():
    input_data = dict(
        data='data.yml',
        tpl='template.yml',
        out='output.yml',
        validation_rules='rules.yml',
        setup=True,
        version=True,
    )
    expected = input_data.get('data')
    in_args = (
        '-d', expected,
    )
    result = cli.parse_args(in_args)
    actual = result.data
    assert expected == actual

    expected = input_data.get('tpl')
    in_args = (
        '-t', expected,
    )
    result = cli.parse_args(in_args)
    actual = result.tpl
    assert expected == actual

    expected = input_data.get('out')
    in_args = (
        '-o', expected,
    )
    result = cli.parse_args(in_args)
    actual = result.out
    assert expected == actual

    expected = input_data.get('validation_rules')
    in_args = (
        '-r', expected,
    )
    result = cli.parse_args(in_args)
    actual = result.validation_rules
    assert expected == actual

    expected = input_data.get('setup')
    in_args = (
        '-s',
    )
    result = cli.parse_args(in_args)
    actual = result.setup
    assert expected == actual

    expected = input_data.get('version')
    in_args = (
        '-v',
    )
    result = cli.parse_args(in_args)
    actual = result.version
    assert expected == actual
