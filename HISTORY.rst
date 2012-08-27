History
-------

0.8.2
+++++

* Facepy exceptions may now be pickled.

0.8.1
+++++

* Fixed a bug that caused pagination to stop prematurely.

0.8.0
+++++

* You may now query application access tokens with ``get_application_access_token``.
* ``SignedRequest.parse`` now returns a dictionary describing the payload of the signed request
  instead of a ``SignedRequest`` instance.
* ``SignedRequest.__init__`` now accepts arguments ``signed_request`` and ``application_secret_key`` and no longer
  facilitates for constructing arbitrary signed requests.
* ``SignedRequest#generate`` no longer requires the provision of ``application_secret_key``.
* ``SignedRequest#oauth_token`` and ``SignedRequest.OAuthToken`` have been removed (deprecated since v0.6).
* Fixed a bug that caused some exceptions to be returned rather than raised.
* ``GraphAPI`` now supports retries for ``get``, ``post``, ``delete``, ``search`` and ``fql``.
* ``GraphAPI#get`` is now more intelligent about pagination and should no longer query Facebook for another page
  of results if the current page has less elements than ``limit``.

Note: This release is backwards-incompatible.

0.7.0
+++++

* You may now access the original data of the signed request from ``SignedRequest#raw``.
* You may now issue FQL queries with ``GraphAPI#fql``.
* Fixed a bug that caused ``GraphAPI#batch`` to crash upon receiving legacy errors from Facebook.
* ``FacebookError`` exceptions yielded from ``GraphAPI#batch`` now include the request that
  produced the error.

0.6.9
+++++

* Facepy will now raise ``OAuthError`` for authorization-related errors.
* Facepy will now reuse the connection to Facebook.

0.6.8
+++++

* Fixed a bug that caused a KeyError upon parsing errors without an error code.

0.6.7
+++++

* Fixed a bug that caused some errors to be ignored.
* Facepy now raises ``GraphAPI.HTTPError`` for requests whose transport failed,
  and ``GraphAPI.FacebookError`` for requests that produced an error in Facebook's API.
* Fixed a bug that caused an error for empty batch responses.

0.6.6
+++++

* Facepy now supports batch requests.

0.6.5
+++++

* Updated requests.

0.6.4
+++++

* Fixed a bug that caused SignedRequest.User#has_authorized_application to be incorrect for
  signed requests with an user id, but no OAuth Token.
* Fixed a bug that caused queries that returned 3xx status codes to yield a blank string

0.6.3
+++++

* Fixed a bug that caused installation to fail in some circumstances.

0.6.2
+++++

* Fixed a bug that caused a KeyError upon parsing a signed request that didn't include the user's age.

0.6.1
++++++

* Fixed a bug that caused a NameError upon providing a list of strings as a Graph API parameter.

0.6.0
+++++

* Search results may now be paged.
* 'facepy.VERSION' is now 'facepy.__version__'

0.5.1
+++++

* It is now considerably easier to create signed requests programmatically.

0.5.0
+++++

* Facepy now returns the complete API response instead of just its "data" attribute.

Note: This release is backwards-incompatible.

0.4.2
+++++

* Facepy is now compatible with Python 2.4.
* Fixed a bug that caused a KeyError if the user's locale or country is missing from the signed request.

0.4.1
+++++

* Fixed a bug that caused a TypeError upon parsing signed requests in unicode.

0.4.0
+++++

* Added support for parsing and reverse-engineering signed requests.
* Added support for file-like objects in POST and PUT.

0.3.1
+++++

* Fixed a bug that prevented the 'page' argument to GraphAPI#get from working
  correctly.

0.3.0
+++++

* GraphAPI#get now has a new argument 'page', which returns a generator
  that iterates over each page of results.

0.2.3
+++++

* The GraphAPI class may now be initialized by signed request.

0.2.2
+++++

* Fix a bug that caused non-JSON data (e.g. pictures) to raise a ValueError.

0.2.1
+++++

* Fix a bug that caused a TypeError if the 'path' argument is an integer.

0.2.0
+++++

* Exceptions have been moved.
