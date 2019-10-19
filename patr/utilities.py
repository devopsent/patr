#!/usr/bin/env python
# pylint: disable=missing-docstring,unused-variable,line-too-long

from __future__ import print_function

import os
from io import open
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
from patr import defaults


def msg(message):
    if not defaults.DEBUG:
        return
    print(message)


def load_data_from_path(path):
    with open(path, encoding='utf-8') as in_fd:
        data = in_fd.read()
        return data


def dump_data_to_path(data, path):
    with open(path, 'w', encoding='utf-8') as wfd:
        wfd.write(data)


def update_src_dict(key, item_dict, src_dict=None):
    """
    updates existing or non existing src dict with key values of item dict

    @param key: search key in item dict
    @type key: str
    @param item_dict: the dictionary to search for key
    @type item_dict: dict
    @param src_dict: "starting" dictionary (if there are items matching key - the list will grow)
    @type src_dict: dict|None

    @return dictionary with updated list
    @rtype: dict
    """
    result = src_dict or OrderedDict()
    items_list = result.get(key, [])
    items_list.append(item_dict)
    result.update({key: items_list})
    return result


def copy_rules(dest_base=None):
    """
    copies validation rules to destination `dest`
    :param dest_base: destination file name
    :type dest_base: str
    :return:
    """
    if dest_base is None:
        dest_base = os.path.join(os.getcwd(), os.path.basename(defaults.RULES_PATH))
    data = defaults.RULES_DATA
    dump_data_to_path(data, dest_base)
    print("Generated initial validation rules file {dest_base}".format(**locals()))
    return dest_base
