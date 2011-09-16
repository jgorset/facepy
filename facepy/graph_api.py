import requests

from exceptions import *
from signed_request import parse_signed_request

try:
    import simplejson as json
except ImportError:
    import json

class GraphAPI(object):

    def __init__(self, oauth_token=None, signed_request=None, app_secret=None):
        """Initialize GraphAPI with an oauth_token, signed request or neither.

        If signed_request is given along with app_secret, oauth_token will be
        extracted automatically from the signed_request.

        Arguments:
        oauth_token -- OAuth 2.0 token
        signed_request -- raw signed_request taken from POST (optional)
        app_secret -- Application's app_secret required to parse signed_request (optional)
        """

        if not oauth_token and signed_request and app_secret:
            sr = parse_signed_request(signed_request, app_secret)
            self.oauth_token = sr.get("oauth_token", None)
        else:
            self.oauth_token = oauth_token

    def get(self, path='', page=False, **options):
        """
        Get an item from the Graph API.

        Arguments:
        path -- A string describing the path to the item.
        page -- A boolean describing whether to return a generator that iterates over each page of results.
        **options -- Graph API parameters such as 'limit', 'offset' or 'since' (see http://developers.facebook.com/docs/reference/api/).
        """

        response = self._query('GET', path, options, page)

        if response is False:
            raise self.Error('Could not get "%s".' % path)

        return response

    def post(self, path='', **data):
        """
        Post an item to the Graph API.

        Arguments:
        path -- A string describing the path to the item.
        **options -- Graph API publishing parameters (see http://developers.facebook.com/docs/reference/api/#publishing).
        """

        response = self._query('POST', path, data)

        if response is False:
            raise self.Error('Could not post to "%s"' % path)

        return response

    def delete(self, path):
        """
        Delete an item in the Graph API.

        Arguments:
        path -- A string describing the path to the item.
        """

        response = self._query('DELETE', path)

        if response is False:
            raise self.Error('Could not delete "%s"' % path)

        return response

    def search(self, term, type, **options):
        """
        Search for an item in the Graph API.

        Arguments:
        term -- A string describing the search term.
        type -- A string describing the type of items to search for *.
        **options -- Additional Graph API parameters, such as 'center' and 'distance' (see http://developers.facebook.com/docs/reference/api/).

        Supported types are 'post', 'user', 'page', 'event', 'group', 'place' and 'checkin'.
        """

        SUPPORTED_TYPES = ['post', 'user', 'page', 'event', 'group', 'place', 'checkin']
        if type not in SUPPORTED_TYPES:
            raise ValueError('Unsupported type "%s". Supported types are %s' % (type, ', '.join(SUPPORTED_TYPES)))

        options = dict({
            'q': term,
            'type': type,
        }, **options)

        response = self._query('GET', 'search', options)

        return response

    def _load_url(self, method, url, data):
        """
        Fetch an object from the Graph API and parse the output.

        Arguments:
        method -- A string describing the HTTP method.
        url -- A string describing the URL.
        data -- A dictionary of HTTP GET parameters (for GET requests) or POST data (for POST requests).

        Returns a pair (obj, next_url) where obj is the object returned from the graph API (parsed 
        into a python object) and next_url is the URL for more results or None if this is the last
        page of results.
        """

        if method in ['GET', 'DELETE']:
            response = requests.request(method, url, params=data)
        else:
            response = requests.request(method, url, data=data)

        result = self._parse(response.content)

        try:
            obj = result['data']
        except (KeyError, TypeError):
            obj = result

        try:
            next_url = result['paging']['next']
        except (KeyError, TypeError):
            next_url = None

        return obj, next_url

    def _query(self, method, path, data={}, page=False):
        """
        Low-level access to Facebook's Graph API.

        Arguments:
        method -- A string describing the HTTP method.
        path -- A string describing the path.
        data -- A dictionary of HTTP GET parameters (for GET requests) or POST data (for POST requests).
        """

        # Convert option lists to comma-separated values; Facebook chokes on array-like constructs
        # in the query string (like [...]?ids=['johannes.gorset', 'atle.mo']).
        for key, value in data.items():
            if type(value) is list and all([type(item) in (str, unicode) for item in value]):
                data[key] = ','.join(value)

        url = 'https://graph.facebook.com/%s' % path
        if self.oauth_token:
            data.update({'access_token': self.oauth_token })
        
        if page:
            def make_generator(url, data):
                while url is not None:
                    objs, url = self._load_url(method, url, data)
                    data = {}
                    for obj in objs:
                        yield objs
            return make_generator(url, data)
        else:
            obj, next_url = self._load_url(method, url, data)
            return obj

    def _parse(self, data):
        """
        Parse the response from Facebook's Graph API.

        Arguments:
        data -- A string describing the Graph API's response.
        """

        try:
            data = json.loads(data)
        except ValueError as e:
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
                raise self.Error(data['error']['message'])

        return data

    class Error(FacepyError):
        pass
