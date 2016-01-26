# Change Log
All notable changes to this project will be documented in this file.

## Unreleased

## 1.0.8 - 2016-01-26
### Fixed
- Fixed an issue where `get_application_access_token` using Graph API versions 2.3+ would
  return JSON instead of a query string, resulting in an `AttributeError` to be thrown.

## 1.0.7 - 2015-09-08
### Fixed
- Fixed an issue where `get_extended_access_token` using Graph API versions 2.3+ would
  return JSON instead of a query string, resulting in an `AttributeError` to be thrown.
- `FacebookError` instances now contain additional data about the error.

## 1.0.6 - 2015-01-07
### Fixed
- Fixed an issue where pagination of nested resources would break.

## 1.0.5 - 2015-01-05
### Added
- You may now specify the API version to use with `GraphAPI`.

## 1.0.4 - 2014-09-28
### Added
- Facepy now proxies the error message from Facebook for 5XX responses.
- Facepy now raises `FacebookError` on any response in the 5XX range.

## 1.0.3 - 2014-06-17
### Added
- `FacebookError`, `HTTPError`, `OAuthError` and `SignedRequestError` are now available
from the `facepy` module for convenience.
- `GraphAPI` now raises `FacebookError` upon receiving HTTP 500 from Facebook.

## 1.0.2 - 2014-06-10
### Added
- `GraphAPI` now accepts an argument `timeout`, which can be either `None` or an
integer describing how many seconds to wait for a response.

## 1.0.1 - 2014-05-22
### Fixed
- Fixed an issue where six would cause an `ImportError` unless already
installed. It is now a direct dependency.

## 1.0.0 - 2014-05-22
### Added
- `GraphAPI` now supports securing Graph API requests with application secret proofs.
- `GraphAPI#post` now supports user-generated images.

### Fixed
- The last bit of the tuple returned from `get_extended_access_token` is now `None`
if the access token won't expire.
- `GraphAPI#batch` can now handle more than 50 requests at a time.
- Fixed a bug that caused unicode URLs to fail.

## 0.9.0 - 2014-02-12
### Added
- Changed `GraphAPI` methods to return `decimal.Decimal` instances for floating-point
numbers instead of `float`, which can cause precision losses not acceptable for
financial operations.
- Nested dictionaries, lists and sets are now automatically encoded as JSON.
- You may now elect to not verify Facebook's SSL certificate.
- You may now substitute colons with underscores in keys such as `fb:explicitly_shared`.
- Facepy is now compatible with Python 3.

### Fixed
- Fixed a bug that caused parsing signed requests to fail when the `user` key
is not present.

## 0.8.4 - 2012-11-13
### Fixed
- Fixed a bug that caused a KeyError for signed requests that were missing
some keys for its "page" attribute.

## 0.8.3 - 2012-10-04
### Added
- You may now extend access tokens with `get_extended_access_token`.

### Fixed
- Fixed a bug that caused batch requests with a body to fail.
- Fixed a bug that caused paths that started with a slash to fail.
- Fixed a bug that caused exception messages to be omitted.

## 0.8.2 - 2012-07-03
### Added
- Facepy exceptions may now be pickled.

## 0.8.1 - 2012-07-02
### Fixed
- Fixed a bug that caused pagination to stop prematurely.

## 0.8.0 - 2012-06-22
### Added
- You may now query application access tokens with `get_application_access_token`.
- `SignedRequest.parse` now returns a dictionary describing the payload of the signed request
instead of a `SignedRequest` instance.
- `SignedRequest.__init__` now accepts arguments `signed_request` and `application_secret_key`
and no longer facilitates for constructing arbitrary signed requests.
- `SignedRequest#generate` no longer requires the provision of `application_secret_key`.
- `GraphAPI` now supports retries for `get`, `post`, `delete`, `search` and `fql`.
- `GraphAPI#get` is now more intelligent about pagination and should no longer query Facebook for another page
of results if the current page has less elements than `limit`.

### Removed
- `SignedRequest#oauth_token` and `SignedRequest.OAuthToken` have been removed (deprecated since v0.6).

### Fixed
- Fixed a bug that caused some exceptions to be returned rather than raised.

## 0.7.0 - 2012-06-13
### Added
- You may now access the original data of the signed request from `SignedRequest#raw`.
- You may now issue FQL queries with `GraphAPI#fql`.
- `FacebookError` exceptions yielded from `GraphAPI#batch` now include the request that
produced the error.

### Fixed
- Fixed a bug that caused `GraphAPI#batch` to crash upon receiving legacy errors from Facebook.

## 0.6.9 - 2012-05-27
### Added
- Facepy will now raise `OAuthError` for authorization-related errors.
- Facepy will now reuse the connection to Facebook.

## 0.6.8 - 2012-04-25
### Fixed
- Fixed a bug that caused a KeyError upon parsing errors without an error code.

## 0.6.7 - 2012-04-23
### Added
- Facepy now raises `GraphAPI.HTTPError` for requests whose transport failed,
and `GraphAPI.FacebookError` for requests that produced an error in Facebook's API.

### Fixed
- Fixed a bug that caused some errors to be ignored.
- Fixed a bug that caused an error for empty batch responses.

## 0.6.6 - 2012-03-28
### Added
- Facepy now supports batch requests.

## 0.6.5 - 2012-03-09
### Added
- Updated requests.

## 0.6.4 - 2012-01-16
### Fixed
- Fixed a bug that caused `SignedRequest.User#has_authorized_application` to be incorrect for
signed requests with an user id, but no OAuth Token.
- Fixed a bug that caused queries that returned 3xx status codes to yield a blank string

## 0.6.3 - 2012-01-12
### Fixed
- Fixed a bug that caused installation to fail in some circumstances.

## 0.6.2 - 2012-01-10
### Fixed
- Fixed a bug that caused a KeyError upon parsing a signed request that didn't include the user's age.

## 0.6.1 - 2012-01-06
### Fixed
- Fixed a bug that caused a NameError upon providing a list of strings as a Graph API parameter.

## 0.6.0 - 2012-01-05
### Added
- Search results may now be paged.
- `facepy.VERSION` is now `facepy.__version__`

## 0.5.1 - 2011-12-03
### Added
- It is now considerably easier to create signed requests programmatically.

## 0.5.0 - 2011-11-07
### Added
- Facepy now returns the complete API response instead of just its "data" attribute.

## 0.4.2 - 2011-11-03
### Added
- Facepy is now compatible with Python 2.4.

### Fixed
- Fixed a bug that caused a KeyError if the user's locale or country is missing from the signed request.

## 0.4.1 - 2011-11-02
### Fixed
- Fixed a bug that caused a TypeError upon parsing signed requests in unicode.

## 0.4.0 - 2011-11-02
### Added
- Added support for parsing and reverse-engineering signed requests.
- Added support for file-like objects in POST and PUT.

## 0.3.1 - 2011-09-17
### Fixed
- Fixed a bug that prevented the 'page' argument to GraphAPI#get from working
correctly.

## 0.3.0 - 2011-09-16
### Added
- GraphAPI#get now has a new argument 'page', which returns a generator
that iterates over each page of results.

## 0.2.3 - 2011-08-15
### Added
- The GraphAPI class may now be initialized by signed request.

## 0.2.2 - 2011-05-26
### Fixed
- Fix a bug that caused non-JSON data (e.g. pictures) to raise a ValueError.

## 0.2.1 - 2011-05-10
### Fixed
- Fix a bug that caused a TypeError if the 'path' argument is an integer.

## 0.2.0 - 2011-05-10
### Added
- Exceptions have been moved.
