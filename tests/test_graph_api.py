"""Tests for facepy.GraphAPI."""

import json
import random

from facepy import GraphAPI
import requests

# Permanent access token for a test user of the Facepy Test Application (application id 160327664029652)
TEST_ACCESS_TOKEN = '160327664029652|71c2bc094b012a6f7f37ece4.0-100002387854815|gmGJg6Sc2nBzssDrCXL_w49bDO8'

def test_get():
    graph = GraphAPI(TEST_ACCESS_TOKEN)
    
    assert graph.get('me').__class__ is dict

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
