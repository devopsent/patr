#!/usr/bin/env python
from __future__ import print_function
import os
from patr.parsers import (
    csv as csv_parser,
    yml as yaml_parser,
)

parse_map = dict(
    yaml=yaml_parser.parse_file_yaml,
    csv=csv_parser.parse_file_csv,
)


def unsupported_extension(fpath):
    print("INFO: supported extensions: {keys}".format(keys=parse_map.keys()))
    raise RuntimeError("FATAL: cluster map file: {fpath} has unsupported extension.".format(**locals()))


def parse_file(fpath):
    """
    Parses a file

    :param fpath:
    :return:
    """
    extension = os.path.splitext(fpath)[1].split('.', 1)[1].lower()
    if extension in ('yml', 'yaml'):
        key = 'yaml'
    elif extension in ('csv', 'tsv'):
        key = 'csv'
    else:
        key = 'unsupported'

    parse_method = parse_map.get(key, unsupported_extension)

    return parse_method(fpath)
