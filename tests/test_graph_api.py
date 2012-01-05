"""Tests for the ``graph_api`` module."""

import random

from facepy import GraphAPI

TEST_APP_ID = '160327664029652'
TEST_APP_SECRET = '102d4e42d228d59c7ae4ebd874ef7757'
TEST_USER = None

def setup_module(module):
    setattr(module, 'TEST_USER', FacebookUser.create())

def teardown_module(module):
    if TEST_USER:
        TEST_USER.delete()

class FacebookUser(object):

    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token
        self.graph = GraphAPI(self.access_token)

    def delete(self):
        application_graph = GraphAPI('%s|%s' % (TEST_APP_ID, TEST_APP_SECRET))
        application_graph.delete("%s/" % self.user_id)

    @classmethod
    def create(cls):
        application_graph = GraphAPI('%s|%s' % (TEST_APP_ID, TEST_APP_SECRET))

        user = application_graph.post("%s/accounts/test-users" % TEST_APP_ID,
            installed='true',
            permissions='publish_stream,read_stream',
        )

        return cls(user['id'], user['access_token'])

def test_get():
    graph = TEST_USER.graph

    assert isinstance(graph.get('me'), dict)
    assert isinstance(graph.get('me/picture'), str)

def test_paged_get():
    graph = TEST_USER.graph

    posts = graph.get('facebook/posts', page=True)

    for index, post in enumerate(posts):
        if index > 3:
            return

    assert False, 'only first page of results returned'

def test_post():
    graph = TEST_USER.graph

    # Generate a random message (Facebook rejects duplicate messages within a short time frame)
    message = ''.join(random.sample('a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(), 10))

    response = graph.post(
        path = 'me/feed',
        message = message
    )

    post = graph.get(response['id'])

    assert post['message'] == message

def test_delete():
    graph = TEST_USER.graph

    # Generate a random message (Facebook rejects duplicate messages within a short time frame)
    message = ''.join(random.sample('a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(), 10))

    response = graph.post(
        path = 'me/feed',
        message = message
    )

    assert graph.delete(response['id']) is True

def test_search():
    graph = GraphAPI()

    results = graph.search(
        term = 'the meaning of life',
        type = 'post'
    )

    assert isinstance(results['data'], list)
