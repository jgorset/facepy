"""
    Tests signed_request.py - you can run these with py.test (http://pytest.org/latest/).
"""
TEST_ACCESS_TOKEN = '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'

TEST_SIGNED_REQUEST = 'mnrG8Wc9CH_rh-GCqq97GFAPOh6AY7cMO8IYVKb6Pa4.eyJhbGdvcml0aG0iOi' \
                      'JITUFDLVNIQTI1NiIsImV4cGlyZXMiOjAsImlzc3VlZF9hdCI6MTMwNjE3OTkw' \
                      'NCwib2F1dGhfdG9rZW4iOiIxODEyNTk3MTE5MjUyNzB8MTU3MGE1NTNhZDY2MD' \
                      'U3MDVkMWI3YTVmLjEtNDk5NzI5MTI5fDhYcU1SaENXREt0cEctaV96UmtIQkRT' \
                      'c3FxayIsInVzZXIiOnsiY291bnRyeSI6Im5vIiwibG9jYWxlIjoiZW5fVVMiLC' \
                      'JhZ2UiOnsibWluIjoyMX19LCJ1c2VyX2lkIjoiNDk5NzI5MTI5In0'

TEST_FACEBOOK_APPLICATION_SECRET_KEY = '214e4cb484c28c35f18a70a3d735999b'

def test_parse_signed_request():
    from facepy.signed_request import parse_signed_request
    data = parse_signed_request(TEST_SIGNED_REQUEST, TEST_FACEBOOK_APPLICATION_SECRET_KEY)

    assert data['user_id'] == '499729129'
    assert data['algorithm'] == 'HMAC-SHA256'
    assert data['expires'] == 0
    assert data['oauth_token'] == '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'
    assert data['issued_at'] == 1306179904


def test_create_signed_request():
    from facepy.signed_request import parse_signed_request
    from facepy.signed_request import create_signed_request
    from datetime import datetime, timedelta
    import time

    # test sending only user_id
    signed_request_user_1 = create_signed_request(TEST_FACEBOOK_APPLICATION_SECRET_KEY, user_id=1, issued_at=1254459601)
    assert signed_request_user_1 == 'Y0ZEAYY9tGklJimbbSGy2dgpYz9qZyVJp18zrI9xQY0=.eyJpc3N1ZWRfYXQiOiAxMjU0NDU5NjAxLCAidXNlcl9pZCI6IDEsICJhbGdvcml0aG0iOiAiSE1BQy1TSEEyNTYifQ=='

    data_user_1 = parse_signed_request(signed_request_user_1, TEST_FACEBOOK_APPLICATION_SECRET_KEY)
    assert sorted(data_user_1.keys()) == sorted([u'user_id', u'algorithm', u'issued_at'])
    assert data_user_1['user_id'] == 1
    assert data_user_1['algorithm'] == 'HMAC-SHA256'

    # test not sending a user_id which will default to user_id 1
    signed_request_user_2 = create_signed_request(TEST_FACEBOOK_APPLICATION_SECRET_KEY, issued_at=1254459601)
    assert signed_request_user_1 == signed_request_user_2

    # test sending each available named argument
    today = datetime.now()
    tomorrow = today + timedelta(hours=1)

    signed_request_user_3 = create_signed_request(
       app_secret = TEST_FACEBOOK_APPLICATION_SECRET_KEY,
       user_id = 999,
       issued_at = 1254459600,
       expires = tomorrow,
       oauth_token = '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk',
       app_data = {},
       page = {
           'id': '1',
           'liked': True
       }
   )

    data_user_3 = parse_signed_request(signed_request_user_3, TEST_FACEBOOK_APPLICATION_SECRET_KEY)
    assert sorted(data_user_3.keys()) == sorted([u'user_id', u'algorithm', u'issued_at', u'expires', u'oauth_token', u'app_data', u'page'])
    assert data_user_3['user_id'] == 999
    assert data_user_3['algorithm'] == 'HMAC-SHA256'
    assert data_user_3['issued_at'] == 1254459600
    assert data_user_3['expires'] == int(time.mktime(tomorrow.timetuple()))
    assert data_user_3['oauth_token'] == '181259711925270|1570a553ad6605705d1b7a5f.1-499729129|8XqMRhCWDKtpG-i_zRkHBDSsqqk'
    assert data_user_3['app_data'] == {}
    assert data_user_3['page'] == {
       'id': '1',
       'liked': True
    }