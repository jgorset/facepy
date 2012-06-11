"""Tests for the ``graph_api`` module."""

import random
import json
from mock import patch, Mock as mock
from nose.tools import *

from facepy import GraphAPI

TEST_USER_ACCESS_TOKEN = '...'

patch = patch('requests.session')

def setup_module():
    global mock_request
    global response

    mock_request = patch.start()
    mock_request = mock_request()
    mock_request = mock_request.request
    mock_request.return_value = response = mock()

def teardown_module():
    patch.stop()

def test_get():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    # Test a simple get
    response.content = json.dumps({
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
    response.content = json.dumps({
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
    response.content = json.dumps({
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
    response.content = json.dumps({
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
    response.content = json.dumps({
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

def test_post():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    response.content = json.dumps({
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

def test_delete():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    # Yes; this is, in fact, what the Graph API returns upon successfully
    # deleting an item.
    response.content = 'true'

    graph.delete(1)

    mock_request.assert_called_with('DELETE', 'https://graph.facebook.com/1',
        allow_redirects = True,
        params = {
            'access_token': TEST_USER_ACCESS_TOKEN
        }
    )

def test_search():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    response.content = json.dumps({
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

def test_batch():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    response.content = json.dumps([
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

@raises(GraphAPI.FacebookError)
def test_batch_with_errors():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    response.content = json.dumps([
        {
            'code': 500,
            'headers': [
                { 'name': 'Content-Type', 'value': 'text/javascript; charset=UTF-8' }
            ],
            'body': '{"error_code": 1, "error_msg": "An unknown error occurred"}'
        }
    ])

    batch = graph.batch(
        requests = [{ 'method': 'GET', 'relative_url': 'me' }]
    )

    for item in batch:
        pass
