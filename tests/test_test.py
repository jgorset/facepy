"""Tests for the ``test`` module."""

from mock import patch
from nose.tools import *

from facepy.test import *

@patch('facepy.GraphAPI.post')
def test_create_user(post):
    """Test creating a new test user."""
    response = {
        'id': '<id>',
        'access_token': '<access token>',
        'login_url': '<login url>',
        'email': '<email>',
        'password': '<password>'
    }

    post.return_value = response   

    user = User.create('<application id>', '<access token>',
        permissions = ['read_stream'],
        locale = 'en_US',
        name = 'John Doe',
        installed = True
    )

    post.assert_called_with('<application id>/accounts/test-users',
        permissions = ['read_stream'],
        locale = 'en_US',
        name = 'John Doe',
        installed = True
    )

    assert_equal(user.id, response['id'])
    assert_equal(user.access_token, response['access_token'])
    assert_equal(user.login_url, response['login_url'])
    assert_equal(user.email, response['email'])
    assert_equal(user.password, response['password'])

@patch('facepy.GraphAPI.delete')
def test_delete_user(delete):
    """Test deleting a test user."""
    user = User(
        id = '<id>',
        access_token = '<access token>',
        login_url = '<login url>',
        email = '<email>',
        password = '<password'
    )

    user.delete()

    delete.assert_called_with('<id>')
