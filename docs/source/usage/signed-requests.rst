.. _signed-requests:

Signed requests
===============

You may parse `signed requests <http://developers.facebook.com/docs/authentication/signed_request/>`_ using the
``SignedRequest`` class::

    from facepy import SignedRequest
    
    # Parse a signed request into a Python dict
    signed_request_data = SignedRequest.parse(signed_request, facebook_application_secret_key)

    # Get a SignedRequest object
    signed_request = SignedRequest(signed_request, facebook_application_secret_key)
    
    # Print the Facebook ID of the user that generated the signed request
    print signed_request.user.id
    
    # Print the OAuth access token for the user that generated the signed request
    print signed_request.oauth_token.token
    
    # Reverse-engineer the signed request
    signed_request.generate(facebook_application_secret_key)

.. autoclass:: facepy.SignedRequest
    :members: parse, user, data, page, oauth_token, generate, User, Page, OAuthToken

.. admonition:: See also

    `Facebook's documentation on signed requests <http://developers.facebook.com/docs/authentication/signed_request/>`_
