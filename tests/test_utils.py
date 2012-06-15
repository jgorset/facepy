"""Tests for the ``utils`` module."""

from mock import patch, Mock as mock
from nose.tools import *

from facepy import *

patch = patch('requests.session')

def mock():
    global mock_request

    mock_request = patch.start()().request

def unmock():
    patch.stop()

@with_setup(mock, unmock)
def test_get_application_access_token():
    mock_request.return_value.content = 'access_token=...'

    access_token = get_application_access_token('<application id>', '<application secret key>')

    mock_request.assert_called_with('GET', 'https://graph.facebook.com/oauth/access_token',
        allow_redirects = True,
        params = {
            'client_id': '<application id>',
            'client_secret': '<application secret key>',
            'grant_type': 'client_credentials'
        }
    )

    assert access_token == '...'

@with_setup(mock, unmock)
def test_get_application_access_token_raises_error():
    mock_request.return_value.content = 'An unknown error occurred'

    assert_raises(
        GraphAPI.FacebookError, get_application_access_token,
        '<application id>', '<application secret key>'
    )
