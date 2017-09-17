.. _graph-api:

Graph API
=========

You may interact with Facebook's Graph API using the ``GraphAPI`` class::

    from facepy import GraphAPI

    graph = GraphAPI(access_token)

    # Get my latest posts
    graph.get('me/posts')

    # Post a photo of a parrot
    graph.post(
        path = 'me/photos',
        source = open('parrot.jpg')
    )



.. autoclass:: facepy.GraphAPI
    :members: get, post, delete, search, batch

.. admonition:: See also

    `Facebook's documentation on the Graph API <http://developers.facebook.com/docs/reference/api/>`_
