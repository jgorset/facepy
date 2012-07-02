"""Tests for the ``exceptions`` module."""

from nose.tools import *

from facepy import *
from facepy.graph_api import GraphAPI
import cPickle

def test_facepy_error():
    try:
        raise FacepyError('<message>')
    except FacepyError as exception:
        assert exception.message == '<message>'

def test_facebookerror_can_be_pickled():
    try:
        raise GraphAPI.FacebookError('<message>', '<code>')
    except FacepyError as exception:
        cPickle.dumps(exception)

def test_oautherror_can_be_pickled():
    try:
        raise GraphAPI.OAuthError('<message>', '<code>')
    except FacepyError as exception:
        cPickle.dumps(exception)

def test_httperror_can_be_pickled():
    try:
        raise GraphAPI.HTTPError('<message>')
    except FacepyError as exception:
        cPickle.dumps(exception)
