"""Tests for the ``graph_api`` module."""

import random

from facepy import GraphAPI

TEST_APPLICATION_ID = '160327664029652'
TEST_APPLICATION_SECRET = '102d4e42d228d59c7ae4ebd874ef7757'

def setup_module(module):
    """
    Create a Facebook test user.
    """
    global TEST_USER_ID
    global TEST_USER_ACCESS_TOKEN

    graph = GraphAPI('%s|%s' % (TEST_APPLICATION_ID, TEST_APPLICATION_SECRET))

    user = graph.post('%s/accounts/test-users' % TEST_APPLICATION_ID,
        installed = 'true',
        permissions = 'publish_stream, read_stream'
    )

    TEST_USER_ID = user['id']
    TEST_USER_ACCESS_TOKEN = user['access_token']

def teardown_module(module):
    """
    Delete the Facebook test user.
    """
    GraphAPI('%s|%s' % (TEST_APPLICATION_ID, TEST_APPLICATION_SECRET)).delete(
        path = TEST_USER_ID
    )

def test_get():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    # Test a simple get
    assert graph.get('me')

    # Test a get that specifies fields
    assert len(graph.get('me', fields=['id', 'first_name', 'last_name'])) == 3

    # Test a paged get
    pages = graph.get('facebook/posts', page=True)

    for index, page in enumerate(pages):
        if index == 3:
            break

    assert index == 3

def test_post():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    message = ''.join(random.sample('a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(), 10))

    response = graph.post(
        path = 'me/feed',
        message = message
    )

    post = graph.get(response['id'])

    assert post['message'] == message

def test_delete():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    response = graph.post(
        path = 'me/feed',
        message = ''.join(random.sample('a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(), 10))
    )

    assert graph.delete(
        path = response['id']
    )

def test_search():
    graph = GraphAPI(TEST_USER_ACCESS_TOKEN)

    # Test a simple search
    assert graph.search(
        term = 'the meaning of life',
        type = 'post'
    )

    # Test a paged search
    pages = graph.get('facebook/posts', page=True)

    for index, page in enumerate(pages):
        if index == 3:
            break

    assert index == 3
