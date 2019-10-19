#!/usr/bin/env python
# pylint: disable=missing-docstring,unused-variable,line-too-long
from __future__ import print_function

import argparse
import os
import sys

import patr
from patr import (
    defaults,
    utilities,
    validators,
    parsers,
    ctxt,
    render,

)


def parse_args(args=None):
    component_dir = os.getcwd()
    component = os.path.basename(component_dir)
    parser = argparse.ArgumentParser(
        description="patr - Pretty Awesome Template Renderer"
    )
    parser.add_argument(
        '--data', '-d', dest='data',
        help="path to data file",
        default=defaults.CLUSTER_MAP_PATH
    )
    parser.add_argument(
        '--template', '-t', dest='tpl',
        help="path to template",
        default=defaults.INVENTORY_TPL_PATH
    )
    parser.add_argument(
        '--output', '-o', dest='out',
        help="path to output file",
        default=defaults.INVENTORY_OUT_PATH
    )
    parser.add_argument(
        '--rules', '-r', dest='validation_rules',
        help="path to validation rules YAML file",
        default=os.path.join(component_dir, defaults.RULES_PATH_FMT.format(component=component))
    )
    parser.add_argument(
        '--setup', '-s', dest='setup',
        help="setup initial validation rules YAML file",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--version', '-v', dest='version',
        help="print version and exit",
        default=False,
        action='store_true'
    )
    if args is None:
        args = sys.argv[1:]
    result = parser.parse_args(args=args)
    return result


def copy_missing_files(parsed_args, attr_list):
    for attr in attr_list:
        path = getattr(parsed_args, attr, None)
        if path is None:
            continue
        if not os.path.exists(path):
            print("File: {path} is missing, generating from default".format(**locals()))
            utilities.copy_rules(path)


def main():
    arguments = parse_args(args=sys.argv[1:])

    rules_path = arguments.validation_rules

    if arguments.setup:
        utilities.copy_rules(rules_path)
        return 0

    if arguments.version:
        version = patr.__version__
        print("v{version}".format(**locals()))
        return 0

    if not os.path.exists(rules_path):
        print("Validation rules are missing, generating from default")
        rules_path = utilities.copy_rules(rules_path)

    rules = parsers.parse_file(rules_path)
    data = parsers.parse_file(arguments.data)
    validators.validate_data_consistency(data, validation_rules=rules)
    context = ctxt.build_context(data)
    validators.validate_context(context, rules.get('data'))
    render.render_template(arguments.tpl, context=context, path=arguments.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
