#!/usr/bin/env python
# pylint: disable=missing-docstring,unused-variable,line-too-long
"""
renders inventory from source format into ansible inventory
"""
from __future__ import print_function
from jinja2 import Template
from patr import utilities


def render_template(tpl_path, context=None, path=None):
    context = context or {}
    path = path or tpl_path.replace(".j2", "")
    tpl_data = utilities.load_data_from_path(tpl_path)
    tpl = Template(tpl_data)
    result = tpl.render(context)
    utilities.dump_data_to_path(result, path)

