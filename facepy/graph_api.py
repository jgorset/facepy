try:
    import simplejson as json
except ImportError:
    import json  # flake8: noqa
import requests
import hashlib
import hmac
import logging

try:
    import urllib.parse as urlparse
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
    import urlparse
from decimal import Decimal

import six

from facepy.exceptions import *


class GraphAPI(object):
    def __init__(self, oauth_token=False, url='https://graph.facebook.com', verify_ssl_certificate=True, appsecret=False, timeout=None, version=None):
        """
        Initialize GraphAPI with an OAuth access token.

        :param oauth_token: A string describing an OAuth access token.
        :param version: A string with version ex. '2.2'.
        """
        self.oauth_token = oauth_token
        self.session = requests.session()
        self.url = url.strip('/')
        self.verify_ssl_certificate = verify_ssl_certificate
        self.appsecret = appsecret
        self.timeout = timeout
        self.version = version

    @classmethod
    def for_application(self, id, secret_key, api_version=None):
        """
        Initialize GraphAPI with an OAuth access token for an application.

        :param id: An integer describing a Facebook application.
        :param secret_key: A String describing the Facebook application's secret key.
        """
        from facepy.utils import get_application_access_token

        access_token = get_application_access_token(id, secret_key, api_version=api_version)
        return GraphAPI(access_token, version=api_version)

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
                    response = self.session.request(
                        method, url, params=data, allow_redirects=True,
                        verify=self.verify_ssl_certificate, timeout=self.timeout
                    )

                if method in ['POST', 'PUT']:
                    files = {}

                    for key in data:
                        if hasattr(data[key], 'read'):
                            files[key] = data[key]

                    for key in files:
                        data.pop(key)

                    response = self.session.request(
                        method, url, data=data, files=files,
                        verify=self.verify_ssl_certificate, timeout=self.timeout
                    )

                if 500 <= response.status_code < 600:
                    # Facebook 5XX errors usually come with helpful messages
                    # as a JSON object describing the problem with the request.
                    # If this is the case, an error will be raised and we just
                    # need to re-raise it. This is most likely to happen
                    # with the Ads API.
                    # This will raise an exception if a JSON-like error object
                    # comes in the response.
                    self._parse(response.content)
                    # If Facebook does not provide any JSON-formatted error
                    # but just a plain-text, useless error, we'll just inform
                    # about a Facebook Internal errror occurred.
                    raise FacebookError(
                        'Internal Facebook error occurred',
                        response.status_code
                    )

            except requests.RequestException as exception:
                raise HTTPError(exception)

            result = self._parse(response.content)
            if isinstance(result, dict):
                result['headers'] = response.headers

            try:
                next_url = result['paging']['next']
            except (KeyError, TypeError):
                next_url = None

            return result, next_url

        def load_with_retry(method, url, data):
            remaining_retries = retry
            while True:
                try:
                    return load(method, url, data)
                except FacepyError as e:
                    logging.warn("Exception on %s: %s, retries remaining: %s" % (
                        url,
                        e,
                        remaining_retries,
                    ))
                    if remaining_retries > 0:
                        remaining_retries -= 1
                    else:
                        raise

        def paginate(method, url, data):
            while url:
                result, url = load_with_retry(method, url, data)

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

        url = self._get_url(path)

        if self.oauth_token:
            data['access_token'] = self.oauth_token

        if self.appsecret and self.oauth_token:
            data['appsecret_proof'] = self._generate_appsecret_proof()

        if page:
            return paginate(method, url, data)
        else:
            return load_with_retry(method, url, data)[0]

    def _get_url(self, path):
        # When Facebook returns nested resources (like comments for a post), it
        # prepends 'https://graph.facebook.com' by itself and so we must take
        # care not to prepend it again.
        if urlparse.urlparse(path).netloc == '':
            url = self.url
        else:
            url = ''

        if self.version:
            url = '%s/v%s%s' % (url, self.version, path)
        else:
            url = '%s%s' % (url, path)

        return url

    def _get_error_params(self, error_obj):
        error_params = {}
        error_fields = ['message', 'code', 'error_subcode', 'error_user_msg',
                        'is_transient', 'error_data', 'error_user_title',
                        'fbtrace_id']

        if 'error' in error_obj:
            error_obj = error_obj['error']

        for field in error_fields:
            error_params[field] = error_obj.get(field)
        return error_params

    def _parse(self, data):
        """
        Parse the response from Facebook's Graph API.

        :param data: A string describing the Graph API's response.
        """
        if type(data) == type(bytes()):
            try:
                data = data.decode('utf-8')
            except UnicodeDecodeError:
                return data

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

                raise exception(**self._get_error_params(data))

            # Facebook occasionally reports errors in its legacy error format.
            if 'error_msg' in data:
                raise FacebookError(**self._get_error_params(data))

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
