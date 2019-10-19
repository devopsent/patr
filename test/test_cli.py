#!/usr/bin/env python

from patr import cli
import pytest


@pytest.mark.xfail
def test_parse_args():
    assert False
