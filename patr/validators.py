#!/usr/bin/env python
# pylint: disable=missing-docstring,unused-variable,line-too-long
from __future__ import print_function
import sys
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


def cool_validator(hdata, field, cls, extra_line=""):
    name = hdata['name']
    try:
        data = hdata.get(field, None)
        assert data is not None
        assert isinstance(data, cls)
    except AssertionError:
        err_arr = [
            "FATAL: YAML parsing problem:",
            "'" + field + "' of host '" + name + "' should be a " + str(type(cls)) + ", but it is: " + str(type(data)),
        ]
        if extra_line != "":
            err_arr.append(extra_line)
        print(" ".join(err_arr))
        print("SUGGESTION: Please fix your cluster map file")
        sys.exit(1)


def less_cool_validator(condition, err_message, extra_line=""):
    try:
        assert condition
    except AssertionError:
        print(err_message)
        if extra_line != "":
            print(extra_line)
        sys.exit(1)


def validate_context_groups(context, validation_rules):
    """
    Validates context groups using validation rules
    :param context:  context dictionary
    :type context: OrderedDict
    :param validation_rules: validation rules dictionary
    :type validation_rules: OrderedDict
    :return:
    """
    groups = context.get("groups", OrderedDict())
    for key in validation_rules:
        curr_count = len(groups.get(key, []))
        val = validation_rules[key]
        comment = ''
        extra_line = [
            "       Please refer to `README.ENV.md` file"
        ]
        if isinstance(val, (dict, OrderedDict,)):
            comment = val.get('comment', '')
            val = val.get('count', 0)

        less_cool_validator(
            curr_count >= val,
            "FATAL: hostgroup '{key}' must have at least {val} hosts. (now: {curr_count})".format(**locals()),
            extra_line="\n".join(extra_line)
        )
        if comment:
            print("        " + " ".join(["SUGGESTION for '{key}':".format(**locals()), comment]))


def validate_host_variables(host_data, group_variables):
    variables_dict = host_data.get('variables', OrderedDict())
    print("type of variables_dict: " + str(type(variables_dict)))
    cool_validator(host_data, 'variables', (dict, OrderedDict(),), extra_line="")
    name = host_data['name']
    utilities.msg("validating variables of '" + name + "'")
    for var_name in group_variables:
        less_cool_validator(
            var_name in variables_dict.keys(),
            "host '{name}' must have variable '{var_name}' defined in 'variables' section.".format(**locals()),
            extra_line="       Please refer to `README.ENV.md` file"
        )


def validate_host_extra_keys(host_data, group_name, extra_keys):
    name = host_data['name']
    utilities.msg("host: {name}, group extra_keys: {extra_keys}".format(**locals()))
    for var_name in extra_keys:
        less_cool_validator(
            var_name in host_data.keys(),
            ' '.join([
                "host '" + name +"'",
                "in host group '" + group_name +"',",
                "so it must have",
                var_name,
                "defined in its section.",
            ]),
            extra_line="       Please refer to `README.ENV.md` file and update your cluster map file"
        )
        less_cool_validator(
            len(host_data.get(var_name, [])) > 0,
            ' '.join([
                "host '" + name + "'",
                "must have variable",
                var_name,
                "defined and not empty.",
            ]),
            extra_line="       Please refer to `README.ENV.md` file and update your cluster map file"
        )


def validate_data_consistency(data, validation_rules={}):
    """
    Validate data consistency by running validation rules callbacks on it

    NOTE: 1 validation rule per hostgroup is supported
          for a more advanced validation - more advanced
          validation rules data needs to be designed,
          thus re-implementing the whole validation

    :param data: the data we're validating
    :type data: dict or OrderedDict
    :param validation_rules: validation rules dict:
    :type validation_rules: dict or OrderedDict
    :return:
    """
    assert len(validation_rules.keys()) > 0, "FATAL: empty `validation_rules` passed. Refer VALIDATION RULES chapter in the documentation"
    hosts = data.get("data", OrderedDict())
    for host_data in hosts:
        variables_dict = host_data.get('variables', OrderedDict())
        variables_dict = OrderedDict(variables_dict)
        groups = host_data.get('groups')
        for group_name, validation_rule in validation_rules.items():
            if group_name not in groups:
                continue

            if not isinstance(validation_rule, (dict, OrderedDict,)):
                continue

            group_variables = validation_rule.get('variables', [])
            utilities.msg("group: {group_name}, group variables: {group_variables}".format(**locals()))
            validate_host_variables(host_data, group_variables)

            extra_keys = validation_rule.get('extra_keys', [])
            validate_host_extra_keys(host_data, group_name, extra_keys)


def validate_context(context, validation_rules):
    validate_context_groups(context, validation_rules)
