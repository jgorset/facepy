from datetime import datetime, timedelta

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

from facepy.graph_api import GraphAPI


def get_extended_access_token(access_token, application_id, application_secret_key, api_version=None):
    """
    Get an extended OAuth access token.

    :param access_token: A string describing an OAuth access token.
    :param application_id: An integer describing the Facebook application's ID.
    :param application_secret_key: A string describing the Facebook application's secret key.

    Returns a tuple with a string describing the extended access token and a datetime instance
    describing when it expires.
    """
    graph = GraphAPI(version=api_version)

    response = graph.get(
        path='oauth/access_token',
        client_id=application_id,
        client_secret=application_secret_key,
        grant_type='fb_exchange_token',
        fb_exchange_token=access_token
    )

    try:
        components = parse_qs(response)
    except AttributeError:  # api_version >= 2.3 returns a dict
        return response['access_token'], None

    token = components['access_token'][0]

    try:
        expires_at = datetime.now() + timedelta(seconds=int(components['expires'][0]))
    except KeyError:  # there is no expiration
        expires_at = None

    return token, expires_at


def get_application_access_token(application_id, application_secret_key, api_version=None):
    """
    Get an OAuth access token for the given application.

    :param application_id: An integer describing a Facebook application's ID.
    :param application_secret_key: A string describing a Facebook application's secret key.
    """
    graph = GraphAPI(version=api_version)

    response = graph.get(
        path='oauth/access_token',
        client_id=application_id,
        client_secret=application_secret_key,
        grant_type='client_credentials'
    )

    try:
        data = parse_qs(response)

        try:
            return data['access_token'][0]
        except KeyError:
            raise GraphAPI.FacebookError('No access token given')
    except AttributeError:  # api_version >= 2.3 returns a dict
        return response['access_token'], None
