from urlparse import parse_qs

from .graph_api import GraphAPI

def get_application_access_token(application_id, application_secret_key):
    """
    Query Facebook for an OAuth access token for the given application.

    :param application_id: An integer describing a Facebook application's ID.
    :param application_secret_key: A string describing a Facebook application's secret key.
    """
    graph = GraphAPI()

    response = graph.get(
        path = 'oauth/access_token',
        client_id = application_id,
        client_secret = application_secret_key,
        grant_type = 'client_credentials'
    )

    data = parse_qs(response)

    try:
        return data['access_token'][0]
    except KeyError:
        raise GraphAPI.FacebookError('No access token given')
