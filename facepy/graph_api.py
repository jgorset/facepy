try:
    import simplejson as json
except ImportError:
    import json  # flake8: noqa
import requests

from urllib import urlencode

from facepy.exceptions import *


class GraphAPI(object):
    def __init__(self, oauth_token=False, url='https://graph.facebook.com'):
        """
        Initialize GraphAPI with an OAuth access token.

        :param oauth_token: A string describing an OAuth access token.
        """
        self.oauth_token = oauth_token
        self.session = requests.session()
        self.url = url.strip('/')

    def get(self, path='', page=False, retry=3, **options):
        """
        Get an item from the Graph API.

        :param path: A string describing the path to the item.
        :param page: A boolean describing whether to return a generator that
                     iterates over each page of results.
        :param retry: An integer describing how many times the request may be retried.
        :param options: Graph API parameters such as 'limit', 'offset' or 'since'.

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

        responses = self.post(
            batch=json.dumps(requests)
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
        data = data or {}

        def load(method, url, data):
            try:
                if method in ['GET', 'DELETE']:
                    response = self.session.request(method, url, params=data, allow_redirects=True)

                if method in ['POST', 'PUT']:
                    files = {}

                    for key in data:
                        if hasattr(data[key], 'read'):
                            files[key] = data[key]

                    for key in files:
                        data.pop(key)

                    response = self.session.request(method, url, data=data, files=files)
            except requests.RequestException as exception:
                raise HTTPError(exception.message)

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
            if isinstance(data[key], (list, set, tuple)) and all([isinstance(item, basestring) for item in data[key]]):
                data[key] = ','.join(data[key])

        # Support absolute paths too
        if not path.startswith('/'):
            path = '/' + str(path)

        url = '%s%s' % (self.url, path)

        if self.oauth_token:
            data['access_token'] = self.oauth_token

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
        try:
            data = json.loads(data)
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

    # Proxy exceptions for ease of use and backwards compatibility.
    FacebookError, OAuthError, HTTPError = FacebookError, OAuthError, HTTPError
