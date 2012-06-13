Facepy
======

.. image:: https://secure.travis-ci.org/jgorset/facepy.png?branch=master

Facepy makes it really easy to interact with Facebook's Graph API.

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

Contribute
----------

* Fork `the repository <http://github.com/jgorset/facepy>`_.
* Do your thing (preferably on a feature branch).
* Write a test that demonstrates that the bug was fixed or the feature works as expected.
* Send a pull request and bug me until I merge it!

I love you
----------

Johannes Gorset made this. You should `tweet me <http://twitter.com/jgorset>`_ if you can't get it
to work. In fact, you should tweet me anyway.
