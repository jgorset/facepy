"""Tests for the ``exceptions`` module."""

from nose.tools import *

from facepy import *

def test_facepy_error():
    try:
        raise FacepyError('<message>')
    except FacepyError as exception:
        assert exception.message == '<message>'
