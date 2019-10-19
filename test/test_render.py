#!/usr/bin/env python
# pylint: disable=missing-docstring

import os
import tempfile
from io import open
from patr import render


def test_render_template():
    tmpfile = tempfile.mktemp()
    tpl_text = '''
    A={{a}}
    '''
    with open(tmpfile, 'wb') as fdw:
        fdw.write(tpl_text.encode('utf-8'))

    context = dict(a="bbb")
    path_out = tmpfile + '.out'
    render.render_template(tmpfile, context=context, path=path_out)

    expected = tpl_text.replace('{{a}}', "bbb")
    with open(path_out, encoding='utf-8') as fdr:
        actual = fdr.read()

    assert expected == actual

    os.remove(path_out)
    os.remove(tmpfile)
