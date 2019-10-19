#!/usr/bin/env python
# pylint: disable=missing-docstring

import os
import tempfile
from patr import (
    defaults,
    utilities,
)
from io import open
import pytest


def test_msg(capsys):
    defaults.DEBUG = False
    msg = 'lalala'
    utilities.msg(msg)
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''
    defaults.DEBUG = True
    utilities.msg(msg)
    out, err = capsys.readouterr()
    assert out.strip() == msg
    assert err == ''
    defaults.DEBUG = True


def test_load_data_from_path():
    tmpfile = tempfile.mktemp()
    expected = '''
    alalala
    '''
    with open(tmpfile, 'wb') as fdw:
        fdw.write(expected.encode('utf-8'))

    actual = utilities.load_data_from_path(tmpfile)
    assert expected == actual
    os.remove(tmpfile)


@pytest.mark.xfail
def test_update_src_dict():
    assert False
