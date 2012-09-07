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

    # Make a FQL query
    graph.fql('SELECT name FROM user WHERE uid = me()')

    # Make a FQL multiquery
    graph.fql({
        'rsvp_status': 'SELECT uid, rsvp_status FROM event_member WHERE eid=12345678',
        'details': 'SELECT name, url, pic FROM profile WHERE id IN (SELECT uid FROM #rsvp_status)'
    }

.. autoclass:: facepy.GraphAPI
    :members: get, post, delete, search, batch, fql

.. admonition:: See also

    `Facebook's documentation on the Graph API <http://developers.facebook.com/docs/reference/api/>`_
