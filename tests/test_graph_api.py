# -*- coding:utf-8 -*-

"""Tests for the ``graph_api`` module."""
import json
import decimal

from nose.tools import *
from mock import patch, MagicMock
from requests.exceptions import ConnectionError

from facepy import GraphAPI


patch = patch('requests.session')


def mock():
    global mock_request

    mock_request = patch.start()().request


def unmock():
    patch.stop()


@with_setup(mock, unmock)
def test_get():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps({
        'id': 1,
        'name': 'Thomas \'Herc\' Hauk',
        'first_name': 'Thomas',
        'last_name': 'Hauk',
        'link': 'http://facebook.com/herc',
        'username': 'herc',
    })
    mock_request.return_value.status_code = 200

    graph.get('me')

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/me',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'access_token': '<access token>'
        }
    )


@with_setup(mock, unmock)
def test_get_with_nested_parameters():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps({
        'id': 1,
        'name': 'Thomas \'Herc\' Hauk',
        'first_name': 'Thomas',
        'last_name': 'Hauk',
        'link': 'http://facebook.com/herc',
        'username': 'herc',
    })
    mock_request.return_value.status_code = 200

    graph.get('me', foo={'bar': 'baz'})

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/me',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'access_token': '<access token>',
            'foo': '{"bar": "baz"}'
        }
    )


@with_setup(mock, unmock)
def test_get_with_appsecret():
    graph = GraphAPI('<access token>', appsecret='<appsecret>')

    mock_request.return_value.content = json.dumps({
        'id': 1,
        'name': 'Thomas \'Herc\' Hauk',
        'first_name': 'Thomas',
        'last_name': 'Hauk',
        'link': 'http://facebook.com/herc',
        'username': 'herc',
    })
    mock_request.return_value.status_code = 200

    graph.get('me')

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/me',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'access_token': '<access token>',
            'appsecret_proof': graph._generate_appsecret_proof()
        }
    )


@with_setup(mock, unmock)
def test_get_with_new_version():
    graph = GraphAPI('<access token>', version='2.0')

    mock_request.return_value.content = json.dumps({
        'id': 1,
        'name': 'Thomas \'Herc\' Hauk',
        'first_name': 'Thomas',
        'last_name': 'Hauk',
        'link': 'http://facebook.com/herc',
        'username': 'herc',
        })
    mock_request.return_value.status_code = 200

    graph.get('me')

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/v2.0/me',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'access_token': '<access token>',
        }
    )


@with_setup(mock, unmock)
def test_get_with_fields():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps({
        'id': 1,
        'first_name': 'Thomas',
        'last_name': 'Hauk'
    })
    mock_request.return_value.status_code = 200

    graph.get('me', fields=['id', 'first_name', 'last_name'])

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/me',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'access_token': '<access token>',
            'fields': 'id,first_name,last_name'
        }
    )

    graph.get('me', fields=('id', 'first_name', 'last_name'))

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/me',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'access_token': '<access token>',
            'fields': 'id,first_name,last_name'
        }
    )


@with_setup(mock, unmock)
def test_get_with_fpnum():
    graph = GraphAPI('<access token>')
    mock_request.return_value.content = '{"payout": 0.94}'
    mock_request.return_value.status_code = 200

    resp = graph.get('<paymend_id>')

    assert_equal(resp, {'payout': decimal.Decimal('0.94')})


@with_setup(mock, unmock)
def test_forbidden_get():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = 'false'
    mock_request.return_value.status_code = 200

    assert_raises(GraphAPI.FacebookError, graph.get, 'me')


@with_setup(mock, unmock)
def test_paged_get():
    graph = GraphAPI('<access token>')
    limit = 2

    responses = [
        {
            'data': [
                {
                    'message': 'He\'s a complicated man. And the only one that understands him is his woman'
                }
            ] * 2,
            'paging': {
                'next': 'https://graph.facebook.com/herc/posts?limit=%(limit)s&offset=%(limit)s&access_token=<access token>' % {
                    'limit': limit
                }
            }
        },
        {
            'data': [
                {
                    'message': 'He\'s a complicated man. And the only one that understands him is his woman'
                }
            ],
            'paging': {
                'next': 'https://graph.facebook.com/herc/posts?limit=%(limit)s&offset=%(limit)s&access_token=<access token>' % {
                    'limit': limit
                }
            }
        },
        {
            'data': [],
            'paging': {
                'previous': 'https://graph.facebook.com/herc/posts?limit=%(limit)s&offset=%(limit)s&access_token=<access token>' % {
                    'limit': limit
                }
            }
        }
    ]

    def side_effect(*args, **kwargs):
        response = responses.pop(0)

        return MagicMock(content=json.dumps(response), status_code=200)

    mock_request.side_effect = side_effect

    pages = graph.get('herc/posts', page=True)

    for index, page in enumerate(pages):
        pass

    assert_equal(index, 2)


@with_setup(mock, unmock)
def test_pagination_without_paging_next():
    graph = GraphAPI('<access token>')
    limit = 2

    mock_request.return_value.content = json.dumps({
        'data': [
            {
                'message': 'He\'s a complicated man. And the only one that understands him is his woman',
            },
        ],
        'paging': {
        }
    })
    mock_request.return_value.status_code = 200

    pages = graph.get('herc/posts', page=True, limit=limit)

    for index, page in enumerate(pages):
        pass

    assert_equal(index, 0)


@with_setup(mock, unmock)
def test_get_with_errors():
    graph = GraphAPI('<access token>')

    # Test errors
    mock_request.return_value.content = json.dumps({
        'error': {
            'code': 1,
            'message': 'An unknown error occurred'
        }
    })
    mock_request.return_value.status_code = 200

    assert_raises(GraphAPI.FacebookError, graph.get, 'me')

    # Test legacy errors
    mock_request.return_value.content = json.dumps({
        'error_code': 1,
        'error_msg': 'An unknown error occurred',
    })
    mock_request.return_value.status_code = 200

    assert_raises(GraphAPI.FacebookError, graph.get, 'me')

    # Test legacy errors without an error code
    mock_request.return_value.content = json.dumps({
        'error_msg': 'The action you\'re trying to publish is invalid'
    })
    mock_request.return_value.status_code = 200

    assert_raises(GraphAPI.FacebookError, graph.get, 'me')


@with_setup(mock, unmock)
def test_post():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps({
        'id': 1
    })
    mock_request.return_value.status_code = 200

    graph.post(
        path='me/feed',
        message='He\'s a complicated man. And the only one that understands him is his woman'
    )

    mock_request.assert_called_with(
        'POST',
        'https://graph.facebook.com/me/feed',
        files={},
        verify=True,
        timeout=None,
        data={
            'message': 'He\'s a complicated man. And the only one that understands him is his woman',
            'access_token': '<access token>'
        }
    )


@with_setup(mock, unmock)
def test_post_with_files():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = 'true'
    mock_request.return_value.status_code = 200

    graph.post(
        path='me/photos',
        source=open('tests/fixtures/parrot.jpg')
    )


@with_setup(mock, unmock)
def test_forbidden_post():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = 'false'
    mock_request.return_value.status_code = 200

    assert_raises(GraphAPI.FacebookError, graph.post, 'me')


@with_setup(mock, unmock)
def test_delete():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = 'true'
    mock_request.return_value.status_code = 200

    graph.delete('1')

    mock_request.assert_called_with(
        'DELETE',
        'https://graph.facebook.com/1',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'access_token': '<access token>'
        }
    )


@with_setup(mock, unmock)
def test_forbidden_delete():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = 'false'
    mock_request.return_value.status_code = 200

    assert_raises(GraphAPI.FacebookError, graph.delete, 'me')


@with_setup(mock, unmock)
def test_search():
    graph = GraphAPI('<access token>')

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
    mock_request.return_value.status_code = 200

    graph.search(
        term='shaft quotes',
        type='post'
    )

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/search',
        allow_redirects=True,
        verify=True,
        timeout=None,
        params={
            'q': 'shaft quotes',
            'type': 'post',
            'access_token': '<access token>'
        }
    )


@with_setup(mock, unmock)
def test_invalid_search():
    graph = GraphAPI('<access token>')

    assert_raises(ValueError, graph.search, 'shaft', 'movies')


@with_setup(mock, unmock)
def test_batch():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps([
        {
            'code': 200,
            'headers': [
                {'name': 'Content-Type', 'value': 'text/javascript; charset=UTF-8'}
            ],
            'body': '{"foo": "bar"}'
        }
    ])
    mock_request.return_value.status_code = 200

    requests = [
        {'method': 'GET', 'relative_url': 'me/friends'},
        {'method': 'GET', 'relative_url': 'me/photos'},
        {'method': 'POST', 'relative_url': 'me/feed', 'body': {'message': 'Hi me.'}}
    ]

    batch = graph.batch(
        requests=requests
    )

    for item in batch:
        pass

    mock_request.assert_called_with(
        'POST',
        'https://graph.facebook.com/',
        files={},
        verify=True,
        timeout=None,
        data={
            'batch': json.dumps([
                {'method': 'GET', 'relative_url': 'me/friends'},
                {'method': 'GET', 'relative_url': 'me/photos'},
                {'method': 'POST', 'relative_url': 'me/feed', 'body': 'message=Hi+me.'}
            ]),
            'access_token': '<access token>'
        }
    )


@with_setup(mock, unmock)
def test_batch_with_empty_responses():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps([
        None,
        {
            'code': 200,
            'headers': [
                {'name': 'Content-Type', 'value': 'text/javascript; charset=UTF-8'}
            ],
            'body': '{"foo": "bar"}'
        }
    ])
    mock_request.return_value.status_code = 200

    requests = [
        {'method': 'GET', 'relative_url': 'me/friends'},
        {'method': 'GET', 'relative_url': 'me/photos'}
    ]

    batch = graph.batch(
        requests=requests
    )

    assert list(batch) == [None, {'foo': 'bar'}]


@with_setup(mock, unmock)
def test_batch_with_errors():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps([
        {
            'code': 200,
            'headers': [
                {'name': 'Content-Type', 'value': 'text/javascript; charset=UTF-8'}
            ],
            'body': '{"foo": "bar"}'
        },
        {
            'code': 500,
            'headers': [
                {'name': 'Content-Type', 'value': 'text/javascript; charset=UTF-8'}
            ],
            'body': '{"error_code": 1, "error_msg": "An unknown error occurred"}'
        }
    ])
    mock_request.return_value.status_code = 200

    requests = [
        {'method': 'GET', 'relative_url': 'me/friends'},
        {'method': 'GET', 'relative_url': 'me'}
    ]

    batch = graph.batch(requests)

    responses = list(batch)

    assert isinstance(responses[0], dict)
    assert isinstance(responses[1], Exception)


@with_setup(mock, unmock)
def test_batch_error_references_request():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps([
        {
            'code': 500,
            'headers': [
                {'name': 'Content-Type', 'value': 'text/javascript; charset=UTF-8'}
            ],
            'body': '{"error_code": 1, "error_msg": "An unknown error occurred"}'
        }
    ])
    mock_request.return_value.status_code = 200

    requests = [
        {'method': 'GET', 'relative_url': 'me'}
    ]

    batch = graph.batch(requests)

    responses = list(batch)

    assert_equal(responses[0].request, requests[0])


@with_setup(mock, unmock)
def test_batch_over_50_requests():
    graph = GraphAPI('<access_token')

    def side_effect_batch_size(*args, **kwargs):
        batch_size = len(json.loads(kwargs['data']['batch']))
        if batch_size > 50:
            return MagicMock(content='{"error":{"message":"Too many requests in batch message. Maximum batch size is 50","type":"GraphBatchException"}}',
                             status_code=200)
        else:
            return MagicMock(content=json.dumps([
                {
                    'code': 200,
                    'headers': [
                        {'name': 'Content-Type', 'value': 'text/javascript; charset=UTF-8'}
                    ],
                    'body': '{"foo": "bar"}'
                } for i in range(batch_size)
            ]), status_code=200)

    mock_request.side_effect = side_effect_batch_size

    requests = [dict(method="GET", relative_url="me?fields=username") for i in range(60)]

    batch = graph.batch(
        requests=requests
    )

    responses = list(batch)

    assert len(responses) == 60


@with_setup(mock, unmock)
def test_oauth_error():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps({
        'error': {
            'message': 'An active access token must be used to query information about the current user.',
            'type': 'OAuthException',
            'code': 2500
        }
    })
    mock_request.return_value.status_code = 200

    assert_raises(GraphAPI.OAuthError, graph.get, 'me')


@with_setup(mock, unmock)
def test_error_message_on_500_response():
    graph = GraphAPI('<access token>')

    message = 'Ad Sets may not be added to deleted Campaigns.'
    mock_request.return_value.status_code = 500
    mock_request.return_value.content = json.dumps({
        'error': {
            'code': 1487634,
            'type': 'Exception',
            'is_transient': False,
            'message': message,
        }
    })
    try:
        graph.get('act_xxxx/adcampaigns')
    except GraphAPI.FacebookError as exc:
        eq_(exc.message, message)
    try:
        graph.post('act_xxxx/adcampaigns')
    except GraphAPI.FacebookError as exc:
        eq_(exc.message, message)


@with_setup(mock, unmock)
def test_query_transport_error():
    graph = GraphAPI('<access token>')

    mock_request.side_effect = ConnectionError('Max retries exceeded with url: /')

    assert_raises(GraphAPI.HTTPError, graph.get, 'me')


@with_setup(mock, unmock)
def test_if_raises_error_on_facebook_500():
    graph = GraphAPI('<access token>')

    mock_request.return_value.status_code = 500
    mock_request.return_value.content = ''

    assert_raises(GraphAPI.FacebookError, graph.get, 'me')


@with_setup(mock, unmock)
def test_retry():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps({
        'error': {
            'code': 1,
            'message': 'An unknown error occurred'
        }
    })
    mock_request.return_value.status_code = 200

    assert_raises(GraphAPI.FacebookError, graph.get, 'me', retry=3)
    assert_equal(len(mock_request.call_args_list), 4)


@with_setup(mock, unmock)
def test_get_unicode_url():
    graph = GraphAPI('<access token>')

    mock_request.return_value.content = json.dumps({})
    mock_request.return_value.status_code = 200

    response = graph.get('https://www.facebook.com/christophernewportuniversity‎')

    assert_true(mock_request.called)
    assert_equal({}, response)


@with_setup(mock, unmock)
def test_timeouts():
    graph = GraphAPI('<access token>', timeout=1)

    mock_request.return_value.content = json.dumps({})
    mock_request.return_value.status_code = 200

    graph.get('me')

    mock_request.assert_called_with(
        'GET',
        'https://graph.facebook.com/me',
        allow_redirects=True,
        verify=True,
        timeout=1,
        params={
            'access_token': '<access token>'
        }
    )
