"""Tests for facepy.GraphAPI."""

import json
import random

from facepy import GraphAPI
import requests

# Permanent access token for a test user of the Facepy Test Application (application id 160327664029652)
TEST_ACCESS_TOKEN = '160327664029652|71c2bc094b012a6f7f37ece4.0-100002387854815|gmGJg6Sc2nBzssDrCXL_w49bDO8'

TEST_SIGNED_REQUEST = ""
TEST_APP_SECRET = ""

def test_signed_request():
    graph = GraphAPI(signed_request=TEST_SIGNED_REQUEST, app_secret=TEST_APP_SECRET)

    assert isinstance(graph.get("me"), dict)
    print "test_signed_request() passed."

def test_get():
    graph = GraphAPI(TEST_ACCESS_TOKEN)
    
    assert isinstance(graph.get('me'), dict)
    assert isinstance(graph.get('me/picture'), str)
    print "test_get() passed."


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
    print "test_post() passed."
    
def test_delete():
    graph = GraphAPI(TEST_ACCESS_TOKEN)
    
    # Generate a random message (Facebook rejects duplicate messages within a short time frame)
    message = ''.join(random.sample('a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(), 10))
    
    response = graph.post(
        path = 'me/feed',
        message = message
    )
    
    assert graph.delete(response['id']) is True
    print "test_delete() passed."

def test_search():
    graph = GraphAPI()
    
    results = graph.search(
        term = 'the meaning of life',
        type = 'post'
    )

    assert results.__class__ is list
    print "test_search() passed."

if __name__ == "__main__":
    #test_signed_request()
    test_post()
    test_get()
    test_search()
    test_delete()

