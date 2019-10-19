#!/usr/bin/env python
# pylint: disable=missing-docstring,unused-variable,line-too-long
"""
renders inventory from source format into ansible inventory
"""
from __future__ import print_function
import csv
import distutils
import os

CUSTOMER_NAME = os.environ.get('CUSTOMER_NAME', 'client')

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from patr import utilities

def load_data_from_csv(fpath):
    # print("in load_data_from_csv({fpath})".format(**locals()))
    with open(fpath, 'rb') as fdr:
        csv_dict_reader = csv.DictReader(fdr)
        for row in csv_dict_reader:
            yield row


def parse_csv_data(rows):
    result = []
    for row in rows:
        item = OrderedDict()
        item.update(name=row['name'])
        col_name = '_'.join([CUSTOMER_NAME, 'role'])
        if col_name in row and row[col_name]:
            item.update(customer_roles=[row[col_name]])
        variables = OrderedDict()
        variables_list = [
            '{customer_name}_logical_name'.format(customer_name=CUSTOMER_NAME),
            'qv_ftp_username',
            'qv_ftp_password',
            'qv_bi_instance',
        ]
        for varname in variables_list:
            if varname in row and row[varname]:
                variables.update({varname: row[varname]})
        item.update(variables=variables)
        host_groups = [
            'runtime',
            'runtime_zk',
            'runtime_mysql',
            'cluster',
            'cldb',
            'webserver',
            'tsdb',
            'hiveserver',
            'nfs',
            'haproxy',
            'icinga',
            'qlikview',
        ]
        groups = []
        for host_group in host_groups:
            if host_group not in row:
                continue
            if not bool(distutils.util.strtobool(row[host_group])):
                continue
            groups.append(host_group)
        item.update(groups=groups)
        result.append(item)
    return result


def parse_file_csv(fpath):
    # print("in parse_file_csv({fpath})".format(**locals()))
    data_raw = list(load_data_from_csv(fpath))
    # print("data:")
    # print(data)
    data = parse_csv_data(data_raw)
    # print("result: {result}".format(**locals()))
    result = OrderedDict(version='1.5', data=data)
    return result

