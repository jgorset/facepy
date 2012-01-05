"""Tests for the ``signed_request`` module."""

TEST_ACCESS_TOKEN = '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'

TEST_SIGNED_REQUEST = u'mnrG8Wc9CH_rh-GCqq97GFAPOh6AY7cMO8IYVKb6Pa4.eyJhbGdvcml0aG0iOi' \
                      'JITUFDLVNIQTI1NiIsImV4cGlyZXMiOjAsImlzc3VlZF9hdCI6MTMwNjE3OTkw' \
                      'NCwib2F1dGhfdG9rZW4iOiIxODEyNTk3MTE5MjUyNzB8MTU3MGE1NTNhZDY2MD' \
                      'U3MDVkMWI3YTVmLjEtNDk5NzI5MTI5fDhYcU1SaENXREt0cEctaV96UmtIQkRT' \
                      'c3FxayIsInVzZXIiOnsiY291bnRyeSI6Im5vIiwibG9jYWxlIjoiZW5fVVMiLC' \
                      'JhZ2UiOnsibWluIjoyMX19LCJ1c2VyX2lkIjoiNDk5NzI5MTI5In0'

TEST_FACEBOOK_APPLICATION_SECRET_KEY = '214e4cb484c28c35f18a70a3d735999b'

def test_parse_signed_request():
    from facepy import SignedRequest
    from datetime import datetime

    signed_request = SignedRequest.parse(TEST_SIGNED_REQUEST, TEST_FACEBOOK_APPLICATION_SECRET_KEY)

    assert signed_request.user.id == '499729129'
    assert signed_request.oauth_token.token == TEST_ACCESS_TOKEN
    assert signed_request.oauth_token.expires_at == None
    assert signed_request.oauth_token.issued_at == datetime(2011, 5, 23, 21, 45, 4)

def test_generate_signed_request():
    from facepy import SignedRequest
    from datetime import datetime

    parsed_signed_request = SignedRequest.parse(TEST_SIGNED_REQUEST, TEST_FACEBOOK_APPLICATION_SECRET_KEY)

    assert parsed_signed_request.oauth_token.token == '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'
    assert parsed_signed_request.oauth_token.expires_at == None
    assert parsed_signed_request.oauth_token.issued_at == datetime(2011, 5, 23, 21, 45, 4)
    assert parsed_signed_request.user.locale == 'en_US'
    assert parsed_signed_request.user.country == 'no'
    assert parsed_signed_request.user.age == range(21, 100)
    assert parsed_signed_request.user.id == '499729129'

    reverse_engineered_signed_request = parsed_signed_request.generate(TEST_FACEBOOK_APPLICATION_SECRET_KEY)

    assert reverse_engineered_signed_request == '_BI1k2IFKMlIqbUdtr85034LlIZxMu7iS1xF-K8pYkE=.' \
                                                'eyJ1c2VyX2lkIjoiNDk5NzI5MTI5IiwiYWxnb3JpdGhtI' \
                                                'joiSE1BQy1TSEEyNTYiLCJleHBpcmVzIjowLCJvYXV0aF' \
                                                '90b2tlbiI6IjE4MTI1OTcxMTkyNTI3MHwxNTcwYTU1M2F' \
                                                'kNjYwNTcwNWQxYjdhNWYuMS00OTk3MjkxMjl8OFhxTVJo' \
                                                'Q1dES3RwRy1pX3pSa0hCRFNzcXFrIiwidXNlciI6eyJsb' \
                                                '2NhbGUiOiJlbl9VUyIsImNvdW50cnkiOiJubyIsImFnZS' \
                                                'I6eyJtYXgiOjk5LCJtaW4iOjIxfX0sImlzc3VlZF9hdCI' \
                                                '6MTMwNjE3OTkwNH0='

    parsed_reverse_engineered_signed_request = SignedRequest.parse(
        signed_request = reverse_engineered_signed_request,
        application_secret_key = TEST_FACEBOOK_APPLICATION_SECRET_KEY
    )

    assert parsed_reverse_engineered_signed_request.oauth_token.token == '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'
    assert parsed_reverse_engineered_signed_request.oauth_token.expires_at == None
    assert parsed_reverse_engineered_signed_request.oauth_token.has_expired == False
    assert parsed_reverse_engineered_signed_request.oauth_token.issued_at == datetime(2011, 5, 23, 21, 45, 4)
    assert parsed_reverse_engineered_signed_request.user.locale == 'en_US'
    assert parsed_reverse_engineered_signed_request.user.country == 'no'
    assert parsed_reverse_engineered_signed_request.user.age == range(21, 100)
    assert parsed_reverse_engineered_signed_request.user.id == '499729129'
    assert parsed_reverse_engineered_signed_request.user.has_authorized_application == True
