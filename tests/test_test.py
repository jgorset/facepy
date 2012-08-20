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

    manager = TestUserManager('<application id>', '<access token>')

    user = manager.create_user()

    assert_equal(user.id, response['id'])
    assert_equal(user.access_token, response['access_token'])
    assert_equal(user.login_url, response['login_url'])
    assert_equal(user.email, response['email'])
    assert_equal(user.password, response['password'])

@patch('facepy.GraphAPI.delete')
def test_delete_user(delete):
    """Test deleting a test user."""
    manager = TestUserManager('<application id>', '<access token>')

    user = FacebookTestUser(
        id = '<id>',
        access_token = '<access token>',
        login_url = '<login url>',
        email = '<email>',
        password = '<password'
    )

    manager.delete_user(user)

    delete.assert_called_with('<id>')
