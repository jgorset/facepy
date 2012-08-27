.. _test-users:

Test users
==========

You may manage test users using the ``User`` class of the ``test`` module::

    from facepy.test import User

    user = User.create(application_id, application_access_token,
        name = 'John Doe',
        permissions = ['read_stream', 'publish_stream']
    )

.. autoclass:: facepy.test.User
    :members: create, delete

.. admonition:: See also

    `Facebook's documentation on test users <http://developers.facebook.com/docs/test_users>`_
