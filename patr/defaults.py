#!/usr/bin/env python
# pylint: disable=missing-docstring
import os
DEBUG = True
CLUSTER_MAP_PATH = os.path.join(os.path.abspath(os.getcwd()), 'cluster_map.yml')
INVENTORY_TPL_PATH = os.path.join(os.path.abspath(os.getcwd()), 'hosts.j2')
INVENTORY_OUT_PATH = os.path.join(os.path.abspath(os.getcwd()), 'default_inventory')
RULES_PATH_FMT = '{component}_rules.yml'
# RULES_PATH = 'default_rules.yml'
CUSTOMER_NAME = os.environ.get('CUSTOMER_NAME', 'customer')
RULES_DATA = '''# vim: ts=2 sw=2 expandtab
---
version: '1.0'
customer_name: '{customer}'
data:
  cluster:
    count: 3
    comment: 'should contain ALL the mapr related nodes'
  cldb:
    count: 3
    comment: 'should be exactly 3'
  zookeeper:
    count: 3
    comment: 'should run on half of the nodes for bigger setups'
  metrics:
    count: 1
    comment: 'should run on the other half that zookeper does not run on'
  nfs:
    count: 3
    comment: 'should run on all analytics nodes'
  fileserver:
    count: 3
    comment: 'should run on ALL nodes'
  resourcemanager:
    count: 1
    comment: 'for big clusters more resourcemanagers are required'
  nodemanager:
    count: 3
    comment: 'should run on all analytics nodes'
  oozie:
    count: 1
    comment: 'for big clusters more oozies are needed'
  pig:
    count: 3
    comment: 'should run on all analytics nodes'
  hiveserver:
    count: 3
    comment: 'should run on all analytics nodes'
  hiveserver2:
    count: 1
    comment: 'bigger clusters should have more hs2 nodes, on hiveserver node'
  hue:
    count: 1
    comment: 'should only run on 1 node'
  mysql:
    count: 1
    comment: 'should be strong enough, can be shared accross analytics, mdservice and oltp'
  sqoop:
    count: 3
    comment: 'should run on ALL nodes'
  webserver:
    count: 1
    comment: 'should be powerful enough to serve with REST, can be multiple nodes'
  runtime:
    count: 3
    comment: 'can be as many nodes as needed'
    variables:
    - '{customer}_logical_name'
    extra_keys:
    - 'customer_roles'
  runtime_zk:
    count: 3
    comment: 'should be exactly 3 nodes for quorum to work'
  runtime_mysql:
    count: 1
    comment: 'should be strong enough, can be shared accross analytics, mdservice and oltp'
  mdservice:
    count: 1
    comment: 'should be as many nodes as needed'
  icinga:
    count: 1
    comment: 'should be powerful enough to pull all the checks in the setup'
  tsdb:
    count: 1
  haproxy:
    count: 1
  qlikview:
    count: 1
    variables:
    - 'qv_bi_instance'
    - 'qv_ftp_username'
    - 'qv_ftp_password'
  # cluster_oltp:
  #   count: 3


'''.format(customer=CUSTOMER_NAME)

INVENTORY_TPL_DATA = '''
local ansible_connection=local ansible_python_interpreter=python
localhost ansible_connection=local ansible_python_interpreter=python
{% if customer_roles is mapping %}
{% for role_name in customer_roles.keys() %}
[{{role_name}}]
{% if customer_roles[role_name]|default([])|length -%}
{% for host_entry in customer_roles[role_name] -%}
{{host_entry}}
{% endfor -%}
{% endif -%}
{% endfor -%}
{% endif %}

{% if groups is mapping %}
{% for group_name in groups.keys() %}
[{{group_name}}]
{% if groups[group_name]|default([])|length -%}
{% for host_entry in groups[group_name] -%}
{{host_entry}}
{% endfor -%}
{% endif -%}
{% endfor %}
{% endif %}
'''
