try:
    import simplejson as json
except ImportError:
    import json  # flake8: noqa
import requests
import hashlib
import hmac

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from decimal import Decimal

import six

from facepy.exceptions import *


class GraphAPI(object):
    def __init__(self, oauth_token=False, url='https://graph.facebook.com', verify_ssl_certificate=True, appsecret=False, timeout=None):
        """
        Initialize GraphAPI with an OAuth access token.

        :param oauth_token: A string describing an OAuth access token.
        """
        self.oauth_token = oauth_token
        self.session = requests.session()
        self.url = url.strip('/')
        self.verify_ssl_certificate = verify_ssl_certificate
        self.appsecret = appsecret
        self.timeout = timeout

    @classmethod
    def for_application(self, id, secret_key):
        """
        Initialize GraphAPI with an OAuth access token for an application.

        :param id: An integer describing a Facebook application.
        :param secret_key: A String describing the Facebook application's secret key.
        """
        from facepy.utils import get_application_access_token

        return GraphAPI(get_application_access_token(id, secret_key))

    def get(self, path='', page=False, retry=3, **options):
        """
        Get an item from the Graph API.

        :param path: A string describing the path to the item.
        :param page: A boolean describing whether to return a generator that
                     iterates over each page of results.
        :param retry: An integer describing how many times the request may be retried.
        :param options: Graph API parameters such as 'limit', 'offset' or 'since'.

        Floating-point numbers will be returned as :class:`decimal.Decimal`
        instances.

        See `Facebook's Graph API documentation <http://developers.facebook.com/docs/reference/api/>`_
        for an exhaustive list of parameters.
        """
        response = self._query(
            method='GET',
            path=path,
            data=options,
            page=page,
            retry=retry
        )

        if response is False:
            raise FacebookError('Could not get "%s".' % path)

        return response

    def post(self, path='', retry=0, **data):
        """
        Post an item to the Graph API.

        :param path: A string describing the path to the item.
        :param retry: An integer describing how many times the request may be retried.
        :param data: Graph API parameters such as 'message' or 'source'.

        See `Facebook's Graph API documentation <http://developers.facebook.com/docs/reference/api/>`_
        for an exhaustive list of options.
        """
        response = self._query(
            method='POST',
            path=path,
            data=data,
            retry=retry
        )

        if response is False:
            raise FacebookError('Could not post to "%s"' % path)

        return response

    def delete(self, path, retry=3):
        """
        Delete an item in the Graph API.

        :param path: A string describing the path to the item.
        :param retry: An integer describing how many times the request may be retried.
        """
        response = self._query(
            method='DELETE',
            path=path,
            retry=retry
        )

        if response is False:
            raise FacebookError('Could not delete "%s"' % path)

        return response

    def search(self, term, type, page=False, retry=3, **options):
        """
        Search for an item in the Graph API.

        :param term: A string describing the search term.
        :param type: A string describing the type of items to search for.
        :param page: A boolean describing whether to return a generator that
                     iterates over each page of results.
        :param retry: An integer describing how many times the request may be retried.
        :param options: Graph API parameters, such as 'center' and 'distance'.

        Supported types are ``post``, ``user``, ``page``, ``event``, ``group``, ``place`` and ``checkin``.

        See `Facebook's Graph API documentation <http://developers.facebook.com/docs/reference/api/>`_
        for an exhaustive list of options.
        """
        SUPPORTED_TYPES = ['post', 'user', 'page', 'event', 'group', 'place', 'checkin']

        if type not in SUPPORTED_TYPES:
            raise ValueError('Unsupported type "%s". Supported types are %s' % (type, ', '.join(SUPPORTED_TYPES)))

        options = dict({
            'q': term,
            'type': type,
        }, **options)

        response = self._query('GET', 'search', options, page, retry)

        return response

    def batch(self, requests):
        """
        Make a batch request.

        :param requests: A list of dictionaries with keys 'method', 'relative_url' and optionally 'body'.

        Yields a list of responses and/or exceptions.
        """

        for request in requests:
            if 'body' in request:
                request['body'] = urlencode(request['body'])

        def _grouper(complete_list, n=1):
            """
            Batches a list into constant size chunks.

            :param complete_list: A input list (not a generator).
            :param n: The size of the chunk.

            Adapted from <http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python>
            """

            for i in range(0, len(complete_list), n):
                yield complete_list[i:i + n]

        responses = []

        # Maximum batch size for Facebook is 50 so split up requests
        # https://developers.facebook.com/docs/graph-api/making-multiple-requests/#limits
        for group in _grouper(requests, 50):
            responses += self.post(
                batch=json.dumps(group)
            )

        for response, request in zip(responses, requests):

            # Facilitate for empty Graph API responses.
            #
            # https://github.com/jgorset/facepy/pull/30
            if not response:
                yield None
                continue

            try:
                yield self._parse(response['body'])
            except FacepyError as exception:
                exception.request = request
                yield exception

    def fql(self, query, retry=3):
        """
        Use FQL to powerfully extract data from Facebook.

        :param query: A FQL query or FQL multiquery ({'query_name': "query",...})
        :param retry: An integer describing how many times the request may be retried.

        See `Facebook's FQL documentation <http://developers.facebook.com/docs/reference/fql/>`_
        for an exhaustive list of details.
        """
        return self._query(
            method='GET',
            path='fql?%s' % urlencode({'q': query}),
            retry=retry
        )

    def _query(self, method, path, data=None, page=False, retry=0):
        """
        Fetch an object from the Graph API and parse the output, returning a tuple where the first item
        is the object yielded by the Graph API and the second is the URL for the next page of results, or
        ``None`` if results have been exhausted.

        :param method: A string describing the HTTP method.
        :param path: A string describing the object in the Graph API.
        :param data: A dictionary of HTTP GET parameters (for GET requests) or POST data (for POST requests).
        :param page: A boolean describing whether to return an iterator that iterates over each page of results.
        :param retry: An integer describing how many times the request may be retried.
        """

        if(data):
            data = dict(
                 (k.replace('_sqbro_', '['), v) for k, v in data.items())
            data = dict(
                 (k.replace('_sqbrc_', ']'), v) for k, v in data.items())
            data = dict(
                 (k.replace('__', ':'), v) for k, v in data.items())
        data = data or {}

        def load(method, url, data):
            for key in data:
                value = data[key]

                if isinstance(value, (list, dict, set)):
                    data[key] = json.dumps(value)

            try:
                if method in ['GET', 'DELETE']:
                    response = self.session.request(method, url, params=data, allow_redirects=True,
                     verify=self.verify_ssl_certificate, timeout=self.timeout)

                if method in ['POST', 'PUT']:
                    files = {}

                    for key in data:
                        if hasattr(data[key], 'read'):
                            files[key] = data[key]

                    for key in files:
                        data.pop(key)

                    response = self.session.request(method, url, data=data, files=files,
                        verify=self.verify_ssl_certificate, timeout=self.timeout)
            except requests.RequestException as exception:
                raise HTTPError(exception)

            result = self._parse(response.content)

            try:
                next_url = result['paging']['next']
            except (KeyError, TypeError):
                next_url = None

            return result, next_url

        def paginate(method, url, data):
            while url:
                result, url = load(method, url, data)

                # Reset pagination parameters.
                for key in ['offset', 'until', 'since']:
                    if key in data:
                        del data[key]

                yield result

        # Convert option lists to comma-separated values.
        for key in data:
            if isinstance(data[key], (list, set, tuple)) and all([isinstance(item, six.string_types) for item in data[key]]):
                data[key] = ','.join(data[key])

        # Support absolute paths too
        if not path.startswith('/'):
            if six.PY2:
                path = '/' + six.text_type(path.decode('utf-8'))
            else:
                path = '/' + path

        url = '%s%s' % (self.url, path)

        if self.oauth_token:
            data['access_token'] = self.oauth_token

        if self.appsecret and self.oauth_token:
            data['appsecret_proof'] = self._generate_appsecret_proof()

        try:
            if page:
                return paginate(method, url, data)
            else:
                return load(method, url, data)[0]
        except FacepyError:
            if retry:
                return self._query(method, path, data, page, retry - 1)
            else:
                raise

    def _parse(self, data):
        """
        Parse the response from Facebook's Graph API.

        :param data: A string describing the Graph API's response.
        """
        # tests seems to pass a str, while real usage bytes which should be expected
        if type(data) == type(bytes()):
            data = data.decode('utf-8')
        try:
            data = json.loads(data, parse_float=Decimal)
        except ValueError:
            return data

        # Facebook's Graph API sometimes responds with 'true' or 'false'. Facebook offers no documentation
        # as to the prerequisites for this type of response, though it seems that it responds with 'true'
        # when objects are successfully deleted and 'false' upon attempting to delete or access an item that
        # one does not have access to.
        #
        # For example, the API would respond with 'false' upon attempting to query a feed item without having
        # the 'read_stream' extended permission. If you were to query the entire feed, however, it would respond
        # with an empty list instead.
        #
        # Genius.
        #
        # We'll handle this discrepancy as gracefully as we can by implementing logic to deal with this behavior
        # in the high-level access functions (get, post, delete etc.).
        if type(data) is dict:
            if 'error' in data:
                error = data['error']

                if error.get('type') == "OAuthException":
                    exception = OAuthError
                else:
                    exception = FacebookError

                raise exception(
                    error.get('message'),
                    error.get('code', None)
                )

            # Facebook occasionally reports errors in its legacy error format.
            if 'error_msg' in data:
                raise FacebookError(
                    data.get('error_msg'),
                    data.get('error_code', None)
                )

        return data

    def _generate_appsecret_proof(self):
        """
        Returns a SHA256 of the oauth_token signed by appsecret.
        https://developers.facebook.com/docs/graph-api/securing-requests/
        """
        if six.PY2:
            key = self.appsecret
            message = self.oauth_token
        else:
            key = bytes(self.appsecret, 'utf-8')
            message = bytes(self.oauth_token, 'utf-8')

        return hmac.new(key, message, hashlib.sha256).hexdigest()

    # Proxy exceptions for ease of use and backwards compatibility.
    FacebookError, OAuthError, HTTPError = FacebookError, OAuthError, HTTPError
