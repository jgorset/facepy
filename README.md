# Facepy

## About

Facepy is an API client for Facebook's Graph API that doesn't suck.

## Usage

### Graph API

    from facepy import GraphAPI

    # Initialize the Graph API with a valid access token (optional,
    # but will allow you to do all sorts of fun stuff).
    graph = GraphAPI(oauth_access_token)

    # Get an object from the Graph API.
    graph.get('johannes.gorset')

    # Get a list of objects from the Graph API.
    graph.get('johannes.gorset/friends')

    # Post an item to the Graph API.
    graph.post(
        path = 'johannes.gorset/feed',
        message = 'Why, hello.'
    )

    # Upload an image to the Graph API.
    graph.post(
        path = 'johannes.gorset/photos',
        source = open('parrot.jpg'),
    )

    # Delete an item from the Graph API.
    graph.delete('481213268764')

    # Search the Graph API for posts describing the meaning of life.
    graph.search(
        term = 'the meaning of life',
        type = 'post'
    )

### Signed requests

    from facepy import SignedRequest

    # Parse a signed request
    signed_request = SignedRequest.parse(signed_request, facebook_application_secret_key)

    # Print the Facebook ID of the user that issued the signed request
    print signed_request.user.id
    
    # Print the OAuth token contained within the signed request
    print signed_request.oauth_token.token
    
    # Print whether or not the OAuth token has expired
    print signed_request.oauth_token.has_expired

    # Reverse-engineer the signed request
    signed_request.generate(facebook_application_secret_key)

## Documentation

See [Facebook's Graph API documentation](http://developers.facebook.com/docs/reference/api/) and the docstrings.

## Installation

    $ pip install facepy

## Dependencies

* [requests](https://github.com/kennethreitz/requests/)
