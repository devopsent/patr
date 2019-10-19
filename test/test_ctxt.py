#!/usr/bin/env python
# pylint: disable=missing-docstring

from patr import ctxt
import pytest


def test_gen_host_entry():
    data = dict(
        name="lala",
        variables=dict(
            kuku="kaka",
            susu="sasa",
        )
    )
    # order of dict generated iteration (non orderdict) is unreliable
    # thus we split it into set()s
    expected = set("lala kuku=kaka susu=sasa".split())
    actual = set(ctxt.gen_host_entry(data).split())
    assert expected == actual


    data = dict(
        name="lala",
        variables=dict(
            kuku="kaka",
            susu="sasa",
            dudu=["fee"]
        )
    )
    # order of dict generated iteration (non orderdict) is unreliable
    # thus we split it into set()s
    expected = set('lala kuku=kaka susu=sasa dudu="[\'fee\']"'.split())
    actual = set(ctxt.gen_host_entry(data).split())
    assert expected == actual


@pytest.mark.xfail
def test_build_context():
    assert False
