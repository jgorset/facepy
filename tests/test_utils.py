"""Tests for the ``utils`` module."""

from datetime import datetime

from facepy import (
    get_application_access_token,
    get_extended_access_token,
    GraphAPI
)
from mock import patch
from nose.tools import (
    assert_equal,
    assert_raises,
    with_setup
)

mock_request = None
patch = patch('requests.session')


def mock():
    global mock_request

    mock_request = patch.start()().request


def unmock():
    patch.stop()


@with_setup(mock, unmock)
def test_get_extended_access_token():
    mock_request.return_value.status_code = 200
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
def test_get_extended_access_token_v23_plus():
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = (
        '{"access_token":"<extended access token>","token_type":"bearer"}'
    )

    access_token, expires_at = get_extended_access_token(
        '<access token>',
        '<application id>',
        '<application secret key>',
        api_version='2.3'
    )

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/v2.3/oauth/access_token',
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
    assert not expires_at


@with_setup(mock, unmock)
def test_get_extended_access_token_no_expiry():
    mock_request.return_value.status_code = 200
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
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = 'access_token=<application access token>'

    access_token = get_application_access_token(
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
            'grant_type': 'client_credentials'
        }
    )

    assert_equal(access_token, '<application access token>')

@with_setup(mock, unmock)
def test_get_application_access_token_v23_plus():
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = (
        '{"access_token":"<application access token>","token_type":"bearer"}'
    )

    access_token, expires_at = get_application_access_token(
        '<application id>',
        '<application secret key>',
        api_version='2.3'
    )

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/v2.3/oauth/access_token',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'client_id': '<application id>',
            'client_secret': '<application secret key>',
            'grant_type': 'client_credentials'
        }
    )

    assert_equal(access_token, '<application access token>')

@with_setup(mock, unmock)
def test_get_application_access_token_raises_error():
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = 'An unknown error occurred'

    assert_raises(
        GraphAPI.FacebookError,
        get_application_access_token,
        '<application id>',
        '<application secret key>'
    )
