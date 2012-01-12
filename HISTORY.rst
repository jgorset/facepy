History
-------

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
