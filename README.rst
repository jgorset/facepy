Facepy
======

About
-----

Facepy makes it absurdly easy to interact with Facebook APIs.

Usage
-----

::

    from facepy import GraphAPI

    # Initialize the Graph API with a valid access token (optional,
    # but will allow you to do all sorts of fun stuff).
    graph = GraphAPI(oauth_access_token)

    # Get my latest posts
    graph.get('me/posts')

    # Post a photo of a parrot
    graph.post(
        path = 'me/photos',
        source = open('parrot.jpg')
    )

Facepy can do more than reading your latest posts and posting photographs of parrots, but you'll have to
`read the documentation <http://readthedocs.org/docs/facepy>`_ to find out how.

Installation
------------

::

    $ pip install facepy
