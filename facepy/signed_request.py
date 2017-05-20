import base64
import hashlib
import hmac
import time

try:
    import simplejson as json
except ImportError:
    import json  # flake8: noqa

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs


from datetime import datetime

from facepy.exceptions import *


class SignedRequest(object):
    """
    Facebook uses "signed requests" to communicate with applications on the Facebook platform. See `Facebook's
    documentation on authentication <https://developers.facebook.com/docs/authentication/signed_request/>`_
    for more information.
    """

    user = None
    """A ``SignedRequest.User`` instance describing the user that generated the signed request."""

    data = None
    """A string describing the contents of the ``app_data`` query string parameter."""

    page = None
    """A ``SignedRequest.Page`` instance describing the Facebook page that the signed request was generated from."""

    raw = None
    """A string describing the signed request in its original format."""

    def __init__(self, signed_request=None, application_secret_key=None, application_id=None, api_version=None):
        """
        Initialize a signed request.

        :param signed_request: A string describing a signed request.
        :param application_secret_key: A string describing a Facebook application's secret key.
        """
        self.signed_request = signed_request
        self.application_secret_key = application_secret_key
        self.application_id = application_id
        self.api_version = api_version

        self.raw = self.parse(signed_request, application_secret_key)

        self.data = self.raw.get('app_data', None)

        self.page = self.Page(
            id=self.raw['page'].get('id'),
            is_liked=self.raw['page'].get('liked'),
            is_admin=self.raw['page'].get('admin')
        ) if 'page' in self.raw else None

        if 'user' not in self.raw:
            self.fetch_user_data_and_token()

        self.user = self.User(
            id=self.raw.get('user_id'),
            locale=self.raw['user'].get('locale', None),
            country=self.raw['user'].get('country', None),
            age=range(
                self.raw['user']['age']['min'],
                self.raw['user']['age']['max'] + 1 if 'max' in self.raw['user']['age'] else 100
            ) if 'age' in self.raw['user'] else None,
            oauth_token=self.User.OAuthToken(
                token=self.raw['oauth_token'],
                issued_at=datetime.fromtimestamp(self.raw['issued_at']),
                expires_at=datetime.fromtimestamp(self.raw['expires']) if self.raw['expires'] > 0 else None
            ) if 'oauth_token' in self.raw else None,
        )

    def fetch_user_data_and_token(self):
        from . import GraphAPI, get_application_access_token

        app_token = get_application_access_token(self.application_id, self.application_secret_key, api_version=self.api_version)
        graph = GraphAPI(app_token, version=self.api_version)

        qs = graph.get('oauth/access_token', code=self.raw['code'], redirect_uri='', client_id=self.application_id, client_secret=self.application_secret_key)
        self.raw['oauth_token'] = qs['access_token']
        self.raw['expires'] = time.time() + qs['expires_in']
        self.raw['user'] = graph.get(self.raw['user_id'])

    def parse(cls, signed_request, application_secret_key):
        """Parse a signed request, returning a dictionary describing its payload."""
        def decode(encoded):
            padding = '=' * (len(encoded) % 4)
            return base64.urlsafe_b64decode(encoded + padding)

        try:
            encoded_signature, encoded_payload = (str(string) for string in signed_request.split('.', 2))
            signature = decode(encoded_signature)
            signed_request_data = json.loads(decode(encoded_payload).decode('utf-8'))
        except (TypeError, ValueError):
            raise SignedRequestError("Signed request had a corrupt payload")

        if signed_request_data.get('algorithm', '').upper() != 'HMAC-SHA256':
            raise SignedRequestError("Signed request is using an unknown algorithm")

        expected_signature = hmac.new(application_secret_key.encode('utf-8'), msg=encoded_payload.encode('utf-8'),
                                      digestmod=hashlib.sha256).digest()
        if signature != expected_signature:
            raise SignedRequestError("Signed request signature mismatch")

        return signed_request_data

    parse = classmethod(parse)

    def generate(self):
        """Generate a signed request from this instance."""
        payload = {
            'algorithm': 'HMAC-SHA256'
        }

        if self.data:
            payload['app_data'] = self.data

        if self.page:
            payload['page'] = {}

            if self.page.id:
                payload['page']['id'] = self.page.id

            if self.page.is_liked:
                payload['page']['liked'] = self.page.is_liked

            if self.page.is_admin:
                payload['page']['admin'] = self.page.is_admin

        if self.user:
            payload['user'] = {}

            if self.user.country:
                payload['user']['country'] = self.user.country

            if self.user.locale:
                payload['user']['locale'] = self.user.locale

            if self.user.age:
                payload['user']['age'] = {
                    'min': self.user.age[0],
                    'max': self.user.age[-1]
                }

            if self.user.oauth_token:

                if self.user.oauth_token.token:
                    payload['oauth_token'] = self.user.oauth_token.token

                if self.user.oauth_token.expires_at is None:
                    payload['expires_in'] = 0
                else:
                    payload['expires_in'] = int(time.mktime(self.user.oauth_token.expires_at.timetuple()))

                if self.user.oauth_token.issued_at:
                    payload['issued_at'] = int(time.mktime(self.user.oauth_token.issued_at.timetuple()))

        if self.user.id:
            payload['user_id'] = self.user.id

        encoded_payload = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(',', ':')).encode('utf-8')
        )

        encoded_signature = base64.urlsafe_b64encode(hmac.new(
            self.application_secret_key.encode('utf-8'),
            encoded_payload,
            hashlib.sha256
        ).digest())

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

        @property
        def url(self):
            return 'http://facebook.com/%s' % self.id

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

        oauth_token = None
        """A ``SignedRequest.User.OAuthToken`` instance describing an OAuth access token."""

        def __init__(self, id, age=None, locale=None, country=None, oauth_token=None):
            self.id = id
            self.locale = locale
            self.country = country
            self.age = age
            self.oauth_token = oauth_token

        @property
        def profile_url(self):
            """A string describing the URL to the user's Facebook profile."""
            return 'http://facebook.com/%s' % self.id

        @property
        def has_authorized_application(self):
            """A boolean describing whether the user has authorized the application."""
            return bool(self.oauth_token)

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

    # Proxy exceptions for ease of use and backwards compatibility.
    Error = SignedRequestError
