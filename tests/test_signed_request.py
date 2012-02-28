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

def test_construct_signed_request():
    assert SignedRequest(
        user = SignedRequest.User(
            id = 1,
            age = range(0, 100),
            locale = 'en_US',
            country = 'US',
            oauth_token = SignedRequest.User.OAuthToken(
                token = 'AAAAAAITEghMBAFjv7aoQrdnxDkYyNwpwGXSZBvoWH57Q0f...',
                issued_at = datetime.now(),
                expires_at = None
            )
        )
    )

def test_parse_signed_request():
    signed_request = SignedRequest.parse(
        signed_request = TEST_SIGNED_REQUEST,
        application_secret_key = TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    assert signed_request.user.id == '499729129'
    assert signed_request.user.oauth_token.token == TEST_ACCESS_TOKEN
    assert signed_request.user.oauth_token.expires_at == None
    assert signed_request.user.oauth_token.issued_at

def test_generate_signed_request():
    signed_request = SignedRequest.parse(
        signed_request = TEST_SIGNED_REQUEST,
        application_secret_key = TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    assert signed_request.user.oauth_token.token == '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'
    assert signed_request.user.oauth_token.expires_at == None
    assert signed_request.user.oauth_token.issued_at
    assert signed_request.user.locale == 'en_US'
    assert signed_request.user.country == 'no'
    assert signed_request.user.age == range(21, 100)
    assert signed_request.user.id == '499729129'

    signed_request = signed_request.generate(TEST_FACEBOOK_APPLICATION_SECRET_KEY)

    assert signed_request == '_BI1k2IFKMlIqbUdtr85034LlIZxMu7iS1xF-K8pYkE=.' \
                             'eyJ1c2VyX2lkIjoiNDk5NzI5MTI5IiwiYWxnb3JpdGhtI' \
                             'joiSE1BQy1TSEEyNTYiLCJleHBpcmVzIjowLCJvYXV0aF' \
                             '90b2tlbiI6IjE4MTI1OTcxMTkyNTI3MHwxNTcwYTU1M2F' \
                             'kNjYwNTcwNWQxYjdhNWYuMS00OTk3MjkxMjl8OFhxTVJo' \
                             'Q1dES3RwRy1pX3pSa0hCRFNzcXFrIiwidXNlciI6eyJsb' \
                             '2NhbGUiOiJlbl9VUyIsImNvdW50cnkiOiJubyIsImFnZS' \
                             'I6eyJtYXgiOjk5LCJtaW4iOjIxfX0sImlzc3VlZF9hdCI' \
                             '6MTMwNjE3OTkwNH0='

    signed_request = SignedRequest.parse(
        signed_request = signed_request,
        application_secret_key = TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    assert signed_request.user.oauth_token.token == '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'
    assert signed_request.user.oauth_token.expires_at == None
    assert signed_request.user.oauth_token.has_expired == False
    assert signed_request.user.oauth_token.issued_at
    assert signed_request.user.locale == 'en_US'
    assert signed_request.user.country == 'no'
    assert signed_request.user.age == range(21, 100)
    assert signed_request.user.id == '499729129'
    assert signed_request.user.has_authorized_application == True
