from facepy.exceptions import FacepyError

try:
    import simplejson as json
except ImportError:
    import json

from datetime import datetime

import base64
import hashlib
import hmac
import time

class SignedRequest(object):
    """
    Facebook uses 'signed requests' to communicate with applications on the Facebook platform. See Facebook's
    documentation on authentication at https://developers.facebook.com/docs/authentication/signed_request/
    for the nitty-gritty of signed requests.

    Properties:
    user -- A User instance describing the user that generated the signed request.
    data -- A string describing the contents of the 'app_data' query string parameter.
    page -- A Page instance describing the page that the signed request was generated from.
    oauth_token -- An OAuthToken instance describing an OAuth access token.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['user', 'issued_at', 'expires_at', 'data', 'page', 'oauth_token']:
                setattr(self, key, value)
            else:
                raise TypeError('SignedRequest got an unexpected argument \'%s\'' % key)

    def parse(cls, signed_request, application_secret_key):
        try:
            encoded_signature, encoded_payload = (str(string) for string in signed_request.split('.', 2))
        except IndexError:
            raise cls.Error("Signed request malformed")

        def decode(string):
            return base64.urlsafe_b64decode(string + "=" * ((4 - len(string) % 4) % 4))

        signature = decode(encoded_signature)
        payload = decode(encoded_payload)

        psr = json.loads(payload)

        if not psr['algorithm'] == 'HMAC-SHA256':
            raise cls.Error("Signed request is using an unknown algorithm")

        expected_signature = hmac.new(application_secret_key, msg=encoded_payload, digestmod=hashlib.sha256).digest()
        if not signature == expected_signature:
            raise cls.Error("Signed request signature mismatch")

        return cls(

            # Populate user data
            user = cls.User(
                id = psr.get('user_id'),
                locale = psr['user'].get('locale', None),
                country = psr['user'].get('country', None),
                age = range(
                    psr['user']['age']['min'],
                    psr['user']['age']['max'] + 1 if 'max' in psr['user']['age'] else 100
                )
            ),

            # Populate page data
            page = cls.Page(
                id = psr['page']['id'],
                is_liked = psr['page']['liked'],
                is_admin = psr['page']['admin']
            ) if 'page' in psr else None,

            # Populate oauth token data
            oauth_token = cls.OAuthToken(
                token = psr['oauth_token'],
                issued_at = datetime.fromtimestamp(psr['issued_at']),
                expires_at = datetime.fromtimestamp(psr['expires']) if psr['expires'] > 0 else None
            ) if 'oauth_token' in psr else None,

            # Populate miscellaneous data
            data = psr.get('app_data', None)
        )

    parse = classmethod(parse)

    def generate(self, application_secret_key):

        payload = {
            'algorithm': 'HMAC-SHA256'
        }

        if self.data:
            payload['app_data'] = self.data

        if self.oauth_token:
            payload['oauth_token'] = self.oauth_token.token
            payload['expires'] = int(time.mktime(self.oauth_token.expires_at.timetuple())) if self.oauth_token.expires_at else 0
            payload['issued_at'] = int(time.mktime(self.oauth_token.issued_at.timetuple()))

        if self.page:
            payload['page'] = {
                'id': self.page.id,
                'liked': self.page.is_liked,
                'admin': self.page.is_admin
            }

        if self.user:
            payload['user'] = {
                'country': self.user.country,
                'locale': self.user.locale,
                'age': {
                    'min': self.user.age[0],
                    'max': self.user.age[-1]
                }
            }

        if self.user.id:
            payload['user_id'] = self.user.id

        encoded_payload = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(',', ':'))
        )

        encoded_signature = base64.urlsafe_b64encode(hmac.new(application_secret_key, encoded_payload, hashlib.sha256).digest())

        return '%(signature)s.%(payload)s' % {
            'signature': encoded_signature,
            'payload': encoded_payload
        }

    class Page(object):
        """
        A page represents a Page on Facebook.

        Properties:
        id -- An integer describing the page's Facebook ID.
        is_liked -- A boolean describing whether or not the user likes the page.
        is_admin -- A bolean describing whether or nor the user is an administrator of the page.
        url -- A string describing the URL to the page.
        """

        def __init__(self, id, is_liked, is_admin):
            self.id, self.is_liked, self.is_admin = id, is_liked, is_admin

        def _get_url(self):
            return 'http://facebook.com/%s' % self.id

        url = property(_get_url)

    class User(object):
        """
        A user represents a user on Facebook.

        Properties:
        id -- An integer describing the user's Facebook ID.
        url -- A string describing the URL to the user's profile.
        locale -- A string describing the user's locale.
        country -- A string describing the user's country.
        age -- A range describing the user's age.
        """

        def __init__(self, id, locale, country, age):
            self.id, self.locale, self.country, self.age = id, locale, country, age

        def _get_profile_url(self):
            return 'http://facebook.com/%s' % self.id

        profile_url = property(_get_profile_url)
        
        def _get_authorization_status(self):
            return True if self.id else False
            
        has_authorized_application = property(_get_authorization_status)

    class OAuthToken(object):
        """
        An OAuth token represents an access token that may be used to query
        Facebook's Graph API on behalf of the user that issued it.

        Properties:
        token -- A string describing the access token.
        issued_at -- A datetime instance describing when the signed request was issued.
        expires_at -- A datetime instance describing when the OAuth token will expire, or 'None' if it doesn't.
        """

        def __init__(self, token, issued_at, expires_at):
            self.token, self.issued_at, self.expires_at = token, issued_at, expires_at

        def _has_expired(self):
            if self.expires_at is None:
                return False
            else:
                return self.expires_at < datetime.now()

        has_expired = property(_has_expired)

    class Error(FacepyError):
        """Exception raised for invalid signed_request processing."""
        pass
