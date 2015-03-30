"""Tests for the ``exceptions`` module."""
try:
    import cPickle as pickle
except ImportError:
    import pickle

from nose.tools import *
from facepy import *

TEST_ERROR_OBJ = {
  'error': {
    'message': '<message>',
    'code': 100,
    'error_data': {
      'blame_field_specs': [
        [
          'account_id'
        ]
      ]
    },
    'error_subcode': 1234567,
    'is_transient': False,
    'error_user_title': '<error_user_title>',
    'error_user_msg': '<error_user_msg>'
  }
}


def test_facepy_error():
    try:
        raise FacepyError(TEST_ERROR_OBJ['error']['message'])
    except FacepyError as exception:
        if hasattr(exception, 'message'):
            assert_equal(exception.message, '<message>')
        assert_equal(exception.__str__(), '<message>')
        assert_equal(exception.__repr__(), 'FacepyError(\'<message>\',)')


def test_facebook_error():
    try:
        raise FacebookError(**TEST_ERROR_OBJ['error'])
    except FacebookError as exception:
        for name, value in TEST_ERROR_OBJ['error'].items():
            assert_equal(getattr(exception, name, None), value)
        assert_equal(exception.__str__(), '[100] <message>')
        assert_equal(exception.__repr__(), 'FacebookError(\'[100] <message>\',)')


def test_facebookerror_can_be_pickled():
    try:
        raise GraphAPI.FacebookError(**TEST_ERROR_OBJ['error'])
    except FacepyError as exception:
        pickle.dumps(exception)


def test_oautherror_can_be_pickled():
    try:
        raise GraphAPI.OAuthError(**TEST_ERROR_OBJ['error'])
    except FacepyError as exception:
        pickle.dumps(exception)


def test_httperror_can_be_pickled():
    try:
        raise GraphAPI.HTTPError(TEST_ERROR_OBJ['error']['message'])
    except FacepyError as exception:
        pickle.dumps(exception)
