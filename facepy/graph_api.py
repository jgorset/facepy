import requests

from exceptions import *

try:
    import json
except ImportError:
    import simplejson as json

class GraphAPI(object):
    
    def __init__(self, oauth_token=None):
        self.oauth_token = oauth_token
        
    def get(self, path='', **options):
        """
        Get an item from the Graph API.
        
        Arguments:
        path -- A string describing the path to the item.
        **options -- Graph API parameters such as 'limit', 'offset' or 'since' (see http://developers.facebook.com/docs/reference/api/).
        """
        
        response = self._query('GET', path, options)
        
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
        
        
    def _query(self, method, path, data={}):
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
            if type(value) is list and all([type(item) is str for item in value]):
                data[key] = ','.join(value)
        
        if self.oauth_token:
            data.update({'access_token': self.oauth_token })
        
        response = requests.request(method, 'https://graph.facebook.com/%s' % path, data=data)

        return self._parse(response.content)
        
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
        if type(data) is bool:
            return data
        
        if type(data) is dict:
            
            if 'error' in data:
                raise self.Error(data['error']['message'])
                
            # If the response contains a 'data' key, strip everything else (it serves no purpose)
            if 'data' in data:
                data = data['data']
        
            return data

    class Error(FacepyError):
        pass
