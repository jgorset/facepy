"""Tests for the ``signed_request`` module."""


from datetime import datetime, timedelta
from nose.tools import *

from facepy import SignedRequest


TEST_ACCESS_TOKEN = '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'

TEST_SIGNED_REQUEST = u'' \
    'mnrG8Wc9CH_rh-GCqq97GFAPOh6AY7cMO8IYVKb6Pa4.eyJhbGdvcml0aG0iOi' \
    'JITUFDLVNIQTI1NiIsImV4cGlyZXMiOjAsImlzc3VlZF9hdCI6MTMwNjE3OTkw' \
    'NCwib2F1dGhfdG9rZW4iOiIxODEyNTk3MTE5MjUyNzB8MTU3MGE1NTNhZDY2MD' \
    'U3MDVkMWI3YTVmLjEtNDk5NzI5MTI5fDhYcU1SaENXREt0cEctaV96UmtIQkRT' \
    'c3FxayIsInVzZXIiOnsiY291bnRyeSI6Im5vIiwibG9jYWxlIjoiZW5fVVMiLC' \
    'JhZ2UiOnsibWluIjoyMX19LCJ1c2VyX2lkIjoiNDk5NzI5MTI5In0'

TEST_SIGNED_REQUEST__UNKNOWN_ALGORITHM = u'' \
    'HjPZBDNttKrX_DBxH-fD78wmqP5O7eDcvjE9ToayKb0=.eyJ1c2VyX2lkIjoiN' \
    'Dk5NzI5MTI5IiwiYWxnb3JpdGhtIjoiVU5LTk9XTl9BTEdPUklUSE0iLCJleHB' \
    'pcmVzIjowLCJvYXV0aF90b2tlbiI6IjE4MTI1OTcxMTkyNTI3MHwxNTcwYTU1M' \
    '2FkNjYwNTcwNWQxYjdhNWYuMS00OTk3MjkxMjl8OFhxTVJoQ1dES3RwRy1pX3p' \
    'Sa0hCRFNzcXFrIiwidXNlciI6eyJsb2NhbGUiOiJlbl9VUyIsImNvdW50cnkiO' \
    'iJubyIsImFnZSI6eyJtYXgiOjk5LCJtaW4iOjIxfX0sImlzc3VlZF9hdCI6MTM' \
    'wNjE3OTkwNH0='

TEST_FACEBOOK_APPLICATION_SECRET_KEY = '214e4cb484c28c35f18a70a3d735999b'


def test_parse_signed_request():
    signed_request = SignedRequest.parse(
        signed_request=TEST_SIGNED_REQUEST,
        application_secret_key=TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    assert signed_request == {
        'user_id': '499729129',
        'algorithm': 'HMAC-SHA256',
        'expires': 0,
        'oauth_token': '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk',
        'user': {
            'locale': 'en_US',
            'country': 'no',
            'age': {'min': 21}
        },
        'issued_at': 1306179904
    }


def test_parse_invalid_signed_request():
    assert_raises(
        SignedRequest.Error,
        SignedRequest,
        signed_request="<invalid signed request>",
        application_secret_key=TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )


def test_initialize_signed_request():
    signed_request = SignedRequest(
        signed_request=TEST_SIGNED_REQUEST,
        application_secret_key=TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    assert signed_request.user.id == '499729129'
    assert signed_request.user.oauth_token.token == TEST_ACCESS_TOKEN
    assert signed_request.user.oauth_token.expires_at is None

    assert signed_request.raw == {
        'user_id': '499729129',
        'algorithm': 'HMAC-SHA256',
        'expires': 0,
        'oauth_token': '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk',
        'user': {
            'locale': 'en_US',
            'country': 'no',
            'age': {'min': 21}
        },
        'issued_at': 1306179904
    }


def test_signed_request_page_url():
    page = SignedRequest.Page(id=1)

    assert page.url == 'http://facebook.com/1'


def test_signed_request_user_profile_url():
    user = SignedRequest.User(id=1)

    assert user.profile_url == 'http://facebook.com/1'


def test_signed_request_user_has_authorized_application():
    oauth_token = SignedRequest.User.OAuthToken(
        token='<token>',
        issued_at=datetime.now(),
        expires_at=None
    )

    user = SignedRequest.User(id=1, oauth_token=oauth_token)

    assert user.has_authorized_application is True

    user = SignedRequest.User(id=1, oauth_token=None)

    assert user.has_authorized_application is False


def test_signed_request_user_oauth_token_has_expired():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    oauth_token = SignedRequest.User.OAuthToken(
        token='<token>',
        issued_at=yesterday,
        expires_at=None,
    )

    assert oauth_token.has_expired is False

    oauth_token = SignedRequest.User.OAuthToken(
        token='<token>',
        issued_at=yesterday,
        expires_at=tomorrow
    )

    assert oauth_token.has_expired is False

    oauth_token = SignedRequest.User.OAuthToken(
        token='<token>',
        issued_at=yesterday,
        expires_at=yesterday
    )

    assert oauth_token.has_expired is True


def test_generate_signed_request():
    signed_request = SignedRequest(
        signed_request=TEST_SIGNED_REQUEST,
        application_secret_key=TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    signed_request = signed_request.generate()


def test_parse_signed_request_unknown_algorithm():
    assert_raises(
        SignedRequest.Error,
        SignedRequest.parse,
        signed_request=TEST_SIGNED_REQUEST__UNKNOWN_ALGORITHM,
        application_secret_key=TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )


def test_parse_signed_request_incorrect_signature():
    encoded_signature, _ = (str(string) for string in TEST_SIGNED_REQUEST__UNKNOWN_ALGORITHM.split('.', 2))
    _, encoded_payload = (str(string) for string in TEST_SIGNED_REQUEST.split('.', 2))

    assert_raises(
        SignedRequest.Error,
        SignedRequest.parse,
        signed_request=u"%s.%s" % (encoded_signature, encoded_payload),
        application_secret_key=TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )
