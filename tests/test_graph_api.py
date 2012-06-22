"""Tests for the ``graph_api`` module."""

import random
import json
from mock import patch, call, Mock as mock
from nose.tools import *

from facepy import GraphAPI

TEST_USER_ACCESS_TOKEN = '...'

patch = patch('requests.session')

def mock():
    global mock_request

    mock_request = patch.start()().request

def unmock():
    patch.stop()

@with_setup(mock, unmock)
def test_get():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    # Test a simple get
    mock_request.return_value.content = json.dumps({
        'id': 1,
        'name': 'Thomas \'Herc\' Hauk',
        'first_name': 'Thomas',
        'last_name': 'Hauk',
        'link': 'http://facebook.com/herc',
        'username': 'herc',
    })

    graph.get('me')

    mock_request.assert_called_with('GET', 'https://graph.facebook.com/me',
        allow_redirects = True,
        params = {
          'access_token': TEST_USER_ACCESS_TOKEN
        }
    )

    # Test a get that specifies fields
    mock_request.return_value.content = json.dumps({
        'id': 1,
        'first_name': 'Thomas',
        'last_name': 'Hauk'
    })

    graph.get('me', fields=['id', 'first_name', 'last_name'])

    mock_request.assert_called_with('GET', 'https://graph.facebook.com/me',
        allow_redirects = True,
        params = {
            'access_token': TEST_USER_ACCESS_TOKEN,
            'fields': 'id,first_name,last_name'
        }
    )

    # Test a paged get
    mock_request.return_value.content = json.dumps({
        'data': [
            {
                'message': 'He\'s a complicated man. And the only one that understands him is his woman'
            }
        ] * 100,
        'paging': {
            'next': '...'
        }
    })

    pages = graph.get('herc/posts', page=True)

    for index, page in enumerate(pages):
        break

    mock_request.assert_called_with('GET', 'https://graph.facebook.com/herc/posts',
        allow_redirects = True,
        params = {
            'access_token': TEST_USER_ACCESS_TOKEN
        }
    )

    # Test rasing errors
    mock_request.return_value.content = json.dumps({
        'error_code': 1,
        'error_msg': 'An unknown error occurred',
    })

    try:
        graph.get('me')
    except GraphAPI.FacebookError as e:
        assert e.code == 1
    else:
        assert False, "Error shoud have been raised."

    mock_request.assert_called_with('GET', 'https://graph.facebook.com/me',
        allow_redirects = True,
        params = {
          'access_token': TEST_USER_ACCESS_TOKEN
        }
    )

    # Test raising errors without an error code
    mock_request.return_value.content = json.dumps({
        'error_msg': 'The action you\'re trying to publish is invalid'
    })

    try:
        graph.get('me')
    except GraphAPI.FacebookError as e:
        assert e.message == 'The action you\'re trying to publish is invalid'
        assert e.code == None
    else:
        assert False, "Error without error code should have been raised"

    mock_request.assert_called_with('GET', 'https://graph.facebook.com/me',
        allow_redirects = True,
        params = {
          'access_token': TEST_USER_ACCESS_TOKEN
        }
    )

@with_setup(mock, unmock)
def test_paged_get_avoid_extra_request():
    graph = GraphAPI('<access token>')
    limit = 2

    mock_request.return_value.content = json.dumps({
        'data': [
            {
                'message': 'He\'s a complicated man. And the only one that understands him is his woman',
            },
        ],
        'paging': {
            'next': 'https://graph.facebook.com/herc/posts?limit=%(limit)s&offset=%(limit)s&value=1&access_token=<access token>' % {
                'limit': limit
            }
        }
    })

    pages = graph.get('herc/posts', page=True, limit=limit)

    for index, page in enumerate(pages):
        pass

    assert_equal(index, 0)

@with_setup(mock, unmock)
def test_get_with_retries():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    mock_request.return_value.content = json.dumps({
        'error': {
            'message': 'An unknown error occurred.',
            'code': 500
        }
    })

    try:
        graph.get('me', retry=3)
    except GraphAPI.FacebookError:
        pass

    assert mock_request.call_args_list == [
        call('GET', 'https://graph.facebook.com/me',
            allow_redirects = True, params = {
                'access_token': TEST_USER_ACCESS_TOKEN
            }
        )
    ] * 3


@with_setup(mock, unmock)
def test_post():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    mock_request.return_value.content = json.dumps({
        'id': 1
    })

    graph.post(
        path = 'me/feed',
        message = 'He\'s a complicated man. And the only one that understands him is his woman'
    )

    mock_request.assert_called_with('POST', 'https://graph.facebook.com/me/feed',
        files = {},
        data = {
            'message': 'He\'s a complicated man. And the only one that understands him is his woman',
            'access_token': TEST_USER_ACCESS_TOKEN
        }
    )

@with_setup(mock, unmock)
def test_delete():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    # Yes; this is, in fact, what the Graph API returns upon successfully
    # deleting an item.
    mock_request.return_value.content = 'true'

    graph.delete(1)

    mock_request.assert_called_with('DELETE', 'https://graph.facebook.com/1',
        allow_redirects = True,
        params = {
            'access_token': TEST_USER_ACCESS_TOKEN
        }
    )

@with_setup(mock, unmock)
def test_search():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    mock_request.return_value.content = json.dumps({
        'data': [
            {
                'message': 'I don\'t like your chair.'
            },
            {
                'message': 'Don\'t let your mouth get your ass in trouble.'
            }
        ]
    })

    # Test a simple search
    graph.search(
        term = 'shaft quotes',
        type = 'post'
    )

    mock_request.assert_called_with('GET', 'https://graph.facebook.com/search',
        allow_redirects = True,
        params = {
            'q': 'shaft quotes',
            'type': 'post',
            'access_token': TEST_USER_ACCESS_TOKEN
        }
    )

@with_setup(mock, unmock)
def test_batch():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    mock_request.return_value.content = json.dumps([
        {
            'code': 200,
            'headers': [
                { 'name': 'Content-Type', 'value': 'text/javascript; charset=UTF-8' }
            ],
            'body': '{"foo": "bar"}'
        }
    ])

    requests = [
        { 'method': 'GET', 'relative_url': 'me/friends' },
        { 'method': 'GET', 'relative_url': 'me/photos' }
    ]

    batch = graph.batch(
        requests = requests
    )

    for item in batch:
        pass

    mock_request.assert_called_with('POST', 'https://graph.facebook.com/',
        files = {},
        data = {
            'batch': json.dumps(requests),
            'access_token': TEST_USER_ACCESS_TOKEN
        }
    )

@with_setup(mock, unmock)
def test_batch_with_errors():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    mock_request.return_value.content = json.dumps([
        {
            'code': 500,
            'headers': [
                { 'name': 'Content-Type', 'value': 'text/javascript; charset=UTF-8' }
            ],
            'body': '{"error_code": 1, "error_msg": "An unknown error occurred"}'
        }
    ])

    requests = [{ 'method': 'GET', 'relative_url': 'me' }]

    batch = graph.batch(requests)

    for item in batch:
        assert isinstance(item, Exception)
        assert_equal(requests[0], item.request)
