from .exceptions import FacepyError

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
    Facebook uses 'signed requests' to communicate with applications on the Facebook platform. See `Facebook's
    documentation on authentication <https://developers.facebook.com/docs/authentication/signed_request/>`_
    for more information.
    """

    user = None
    """A ``SignedRequest.User`` instance describing the user that generated the signed request."""

    data = None
    """A string describing the contents of the ``app_data`` query string parameter."""

    page = None
    """A ``SignedRequest.Page`` instance describing the Facebook page that the signed request was generated from."""

    oauth_token = None
    """A ``SignedRequest.OAuthToken`` instance describing an OAuth access token."""

    def __init__(self, user, data=None, page=None, oauth_token=None):
        """Initialize an instance from arbitrary data."""
        self.user, self.data, self.page, self.oauth_token = user, data, page, oauth_token

    def parse(cls, signed_request, application_secret_key):
        """Initialize an instance from a signed request."""
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
                ) if 'age' in psr['user'] else None
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
        """Generate a signed request from this instance."""
        payload = {
            'algorithm': 'HMAC-SHA256'
        }

        if self.data is not None:
            payload['app_data'] = self.data

        if self.oauth_token is not None:
            payload['oauth_token'] = self.oauth_token.token

        if self.oauth_token.expires_at is not None:
            payload['expires'] = int(time.mktime(self.oauth_token.expires_at.timetuple()))
        else:
            payload['expires'] = 0

        if self.oauth_token.issued_at is not None:
            payload['issued_at'] = int(time.mktime(self.oauth_token.issued_at.timetuple()))

        if self.page is not None:
            payload['page'] = {}

            if self.page.id is not None:
                payload['page']['id'] = self.page.id

            if self.page.is_liked is not None:
                payload['page']['liked'] = self.page.is_liked

            if self.page.is_admin is not None:
                payload['page']['admin'] = self.page.is_admin

        if self.user is not None:
            payload['user'] = {}

            if self.user.country is not None:
                payload['user']['country'] = self.user.country

            if self.user.locale is not None:
                payload['user']['locale'] = self.user.locale

            if self.user.age is not None:
                payload['user']['age'] = {
                    'min': self.user.age[0],
                    'max': self.user.age[-1]
                }

        if self.user.id is not None:
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
        A ``Page`` instance represents a Facebook page.
        """

        id = None
        """An integer describing the page's Facebook ID."""

        is_liked = None
        """A boolean describing whether or not the user likes the page."""

        is_admin = None
        """A bolean describing whether or nor the user is an administrator of the page."""

        url = None
        """A string describing the URL to the page."""

        def __init__(self, id, is_liked=False, is_admin=False):
            self.id, self.is_liked, self.is_admin = id, is_liked, is_admin

        def _get_url(self):
            return 'http://facebook.com/%s' % self.id

        url = property(_get_url)

    class User(object):
        """
        A ``User`` instance represents a Facebook user.
        """

        id = None
        """An integer describing the user's Facebook ID."""

        age = None
        """A range describing the user's age."""

        locale = None
        """A string describing the user's locale."""

        country = None
        """A string describing the user's country."""

        def __init__(self, id, age=None, locale=None, country=None):
            self.id, self.locale, self.country, self.age = id, locale, country, age

        @property
        def profile_url(self):
            """A string describing the URL to the user's Facebook profile."""
            return 'http://facebook.com/%s' % self.id

        @property
        def has_authorized_application(self):
            """A boolean describing whether the user has authorized the application."""
            return True if self.id else False

    class OAuthToken(object):
        """
        An OAuth token represents an access token that may be used to query
        Facebook's Graph API on behalf of the user that issued it.
        """

        token = None
        """A string describing the access token."""

        issued_at = None
        """A ``datetime`` instance describing when the access token was issued."""

        expires_at = None
        """A ``datetime`` instance describing when the access token will expire, or ``None`` if it won't."""

        def __init__(self, token, issued_at, expires_at):
            self.token, self.issued_at, self.expires_at = token, issued_at, expires_at

        @property
        def has_expired(self):
            """A boolean describing whether the access token has expired."""
            if self.expires_at is None:
                return False
            else:
                return self.expires_at < datetime.now()

    class Error(FacepyError):
        """Exception raised for invalid signed_request processing."""
