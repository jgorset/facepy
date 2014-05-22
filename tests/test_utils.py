"""Tests for the ``utils`` module."""

from datetime import datetime
from nose.tools import *
from mock import patch

from facepy import *


patch = patch('requests.session')


def mock():
    global mock_request

    mock_request = patch.start()().request


def unmock():
    patch.stop()


@with_setup(mock, unmock)
def test_get_extended_access_token():
    mock_request.return_value.content = 'access_token=<extended access token>&expires=5183994'

    access_token, expires_at = get_extended_access_token(
        '<access token>',
        '<application id>',
        '<application secret key>'
    )

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/oauth/access_token',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'client_id': '<application id>',
            'client_secret': '<application secret key>',
            'grant_type': 'fb_exchange_token',
            'fb_exchange_token': '<access token>'
        }
    )

    assert_equal(access_token, '<extended access token>')
    assert isinstance(expires_at, datetime)


@with_setup(mock, unmock)
def test_get_extended_access_token_no_expiry():
    mock_request.return_value.content = 'access_token=<extended access token>'

    access_token, expires_at = get_extended_access_token(
        '<access token>',
        '<application id>',
        '<application secret key>'
    )

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/oauth/access_token',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'client_id': '<application id>',
            'client_secret': '<application secret key>',
            'grant_type': 'fb_exchange_token',
            'fb_exchange_token': '<access token>'
        }
    )

    assert_equal(access_token, '<extended access token>')
    assert expires_at is None

@with_setup(mock, unmock)
def test_get_application_access_token():
    mock_request.return_value.content = 'access_token=...'

    access_token = get_application_access_token('<application id>', '<application secret key>')

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/oauth/access_token',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'client_id': '<application id>',
            'client_secret': '<application secret key>',
            'grant_type': 'client_credentials'
        }
    )

    assert_equal(access_token, '...')


@with_setup(mock, unmock)
def test_get_application_access_token_raises_error():
    mock_request.return_value.content = 'An unknown error occurred'

    assert_raises(
        GraphAPI.FacebookError,
        get_application_access_token,
        '<application id>',
        '<application secret key>'
    )
