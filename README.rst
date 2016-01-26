.. image::  https://raw.githubusercontent.com/jgorset/facepy/master/docs/banner.png

.. image:: https://img.shields.io/travis/jgorset/facepy.svg
.. image:: https://img.shields.io/github/license/jgorset/facepy.svg
.. image:: https://img.shields.io/pypi/v/facepy.svg

Usage
-----

.. code:: python

    from facepy import GraphAPI

    # Initialize the Graph API with a valid access token (optional,
    # but will allow you to do all sorts of fun stuff).
    graph = GraphAPI(oauth_access_token)

    # Get my latest posts
    graph.get('me/posts')

    # Post a photo of a parrot
    graph.post(
        path = 'me/photos',
        source = open('parrot.jpg', 'rb')
    )

Facepy can do more than reading your latest posts and posting photographs of parrots, but you'll have to
`read the documentation <http://facepy.rtfd.org>`_ to find out how.

Please note that Facepy does *not* do authentication with Facebook; it only consumes its API. To get an
access token to consume the API on behalf of a user, use a suitable OAuth library for your platform (if you're
using Django, for example, you might use `Fandjango <https://github.com/jgorset/fandjango>`_).

Installation
------------

.. code:: bash

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

I love Hyper
------------

I work at `Hyper <https://github.com/hyperoslo>`_ with a bunch of awesome folks
who are every bit as passionate about building things as I am. If you're using
Facepy, we probably want to hire you.
