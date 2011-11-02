"""Tests for facepy.GraphAPI. You can run these with py.test (http://pytest.org/latest/)."""

import json
import random

from facepy import GraphAPI
from facepy import SignedRequest

import requests

# Permanent access token for a test user of the Facepy Test Application (application id 160327664029652)
TEST_ACCESS_TOKEN = '160327664029652|71c2bc094b012a6f7f37ece4.0-100002387854815|gmGJg6Sc2nBzssDrCXL_w49bDO8'

TEST_SIGNED_REQUEST = '7MF856LgfXmXf0PPe4BOWq20FVVZQLAebjlWAh2e64k.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImV4' \
                      'cGlyZXMiOjAsImlzc3VlZF9hdCI6MTMxMzQxNDQ1MCwib2F1dGhfdG9rZW4iOiIxNjAzMjc2NjQwMjk2NTJ8' \
                      'NzFjMmJjMDk0YjAxMmE2ZjdmMzdlY2U0LjEtMTAwMDAyMzg3ODU0ODE1fElET0RNWXpNc3JqbklPLWsxbVVy' \
                      'Qlk4LWpDayIsInVzZXIiOnsiY291bnRyeSI6Im5vIiwibG9jYWxlIjoiZW5fVVMiLCJhZ2UiOnsibWluIjoy' \
                      'MX19LCJ1c2VyX2lkIjoiMTAwMDAyMzg3ODU0ODE1In0'
                      
TEST_APP_SECRET = '102d4e42d228d59c7ae4ebd874ef7757'

def test_get():
    graph = GraphAPI(TEST_ACCESS_TOKEN)

    assert isinstance(graph.get('me'), dict)
    assert isinstance(graph.get('me/picture'), str)

def test_paged_get():
    graph = GraphAPI(TEST_ACCESS_TOKEN)

    posts = graph.get('Facebook/posts', until=1314742370, limit=6, page=True)

    for (i, post) in enumerate(posts):
        # require three pages of results
        if i >= 21:
            return

    assert False, 'only first page of results returned'

def test_post():

    graph = GraphAPI(TEST_ACCESS_TOKEN)

    # Generate a random message (Facebook rejects duplicate messages within a short time frame)
    message = ''.join(random.sample('a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(), 10))

    response = graph.post(
        path = 'me/feed',
        message = message
    )

    post = graph.get(response['id'])

    assert post['message'] == message

def test_delete():
    graph = GraphAPI(TEST_ACCESS_TOKEN)
    
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

    assert results.__class__ is list
