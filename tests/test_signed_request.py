"""Tests for the ``signed_request`` module."""

from datetime import datetime

from facepy import SignedRequest

TEST_ACCESS_TOKEN = '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'

TEST_SIGNED_REQUEST = u'mnrG8Wc9CH_rh-GCqq97GFAPOh6AY7cMO8IYVKb6Pa4.eyJhbGdvcml0aG0iOi' \
                      'JITUFDLVNIQTI1NiIsImV4cGlyZXMiOjAsImlzc3VlZF9hdCI6MTMwNjE3OTkw' \
                      'NCwib2F1dGhfdG9rZW4iOiIxODEyNTk3MTE5MjUyNzB8MTU3MGE1NTNhZDY2MD' \
                      'U3MDVkMWI3YTVmLjEtNDk5NzI5MTI5fDhYcU1SaENXREt0cEctaV96UmtIQkRT' \
                      'c3FxayIsInVzZXIiOnsiY291bnRyeSI6Im5vIiwibG9jYWxlIjoiZW5fVVMiLC' \
                      'JhZ2UiOnsibWluIjoyMX19LCJ1c2VyX2lkIjoiNDk5NzI5MTI5In0'

TEST_FACEBOOK_APPLICATION_SECRET_KEY = '214e4cb484c28c35f18a70a3d735999b'

def test_parse_signed_request():
    signed_request = SignedRequest.parse(
        signed_request = TEST_SIGNED_REQUEST,
        application_secret_key = TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    assert signed_request == {
        'user_id': '499729129',
        'algorithm': 'HMAC-SHA256',
        'expires': 0,
        'oauth_token': '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk',
        'user': {
            'locale': 'en_US',
            'country': 'no',
            'age': { 'min': 21 }
        },
        'issued_at': 1306179904
    }

def test_initialize_signed_request():
    signed_request = SignedRequest(
        signed_request = TEST_SIGNED_REQUEST,
        application_secret_key = TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    assert signed_request.user.id == '499729129'
    assert signed_request.user.oauth_token.token == TEST_ACCESS_TOKEN
    assert signed_request.user.oauth_token.expires_at == None

    assert signed_request.raw == {
        'user_id': '499729129',
        'algorithm': 'HMAC-SHA256',
        'expires': 0,
        'oauth_token': '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk',
        'user': {
            'locale': 'en_US',
            'country': 'no',
            'age': { 'min': 21 }
        },
        'issued_at': 1306179904
    }

def test_generate_signed_request():
    signed_request = SignedRequest(
        signed_request = TEST_SIGNED_REQUEST,
        application_secret_key = TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    signed_request = signed_request.generate(TEST_FACEBOOK_APPLICATION_SECRET_KEY)
