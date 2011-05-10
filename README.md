# Facepy

## About

Facepy is an API client for Facebook's Graph API that doesn't suck.

## Usage

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
    
    # Delete an item from the Graph API.
    graph.delete('481213268764')
    
    # Search the Graph API for posts describing the meaning of life.
    graph.search(
        term = 'the meaning of life',
        type = 'post'
    )
    
## Documentation

See [Facebook's Graph API documentation](http://developers.facebook.com/docs/reference/api/).
    
## Installation

    $ pip install git+git://github.com/jgorset/facepy

## Dependencies

* [requests](https://github.com/kennethreitz/requests/)
