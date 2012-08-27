.. _development:

Development
===========

.. _get the code:

Get the code
------------

Please see the :ref:`source-code-checkouts` section of the :ref:`installation` page
for details on how to obtain Facepy's source code.

.. _contributing:

Contributing
------------

There are a number of ways to get involved with Facepy:

* **Report bugs.** If you think you've found a bug in Facepy, please let me know by
  creating a ticket on the `issue tracker`_.

* **Submit patches or new features.** Create a fork and send me a pull request on `Github`_!

Please note that, although difficult, facepy tries to be as PEP8 compliant as
possible. Thus, before contributing, please try to see if you have PEP8
warnings in your source by running::

    $ make pep8

Tests
-----

Facepy has an exhaustive test suite that runs under Python 2.6, Python 2.7 and PyPy::

    $ make test

To generate a test coverage report::

    $ make report

.. note::

  To run the tests, you will need to install the `tox`_, `nose`_ and `mock`_ libraries.
  To generate the coverage report, you will also need the `nose-cov`_ plugin.

Releases
--------

Major
^^^^^

Major releases update the first number, e.g. going from 0.9 to 1.0, and indicate that the
software has reached some very large milestone.

Minor
^^^^^

Minor releases, such as moving from 1.0 to 1.1, typically mean that one or more new, large
features has been added.

Bugfix
^^^^^^

The third and final part of version numbers, such as the ‘3’ in 1.0.3, generally indicate a
release containing one or more bugfixes, although minor feature modifications may (rarely) occur.

This third number is sometimes omitted for the first major or minor release in a series, e.g. 1.2 or 2.0,
and in these cases it can be considered an implicit zero (e.g. 2.0.0).

Support of older releases
-------------------------

Major and minor releases do not mark the end of the previous line or lines of development:

* The two most recent minor release branches will continue to receive critical bugfixes. For example,
  if 1.1 were the latest minor release, it and 1.0 would get bugfixes, but not 0.9 or earlier; and once
  1.2 came out, this window would then only extend back to 1.1.

* Depending on the nature of bugs found and the difficulty in backporting them, older release lines
  may also continue to get bugfixes – but there’s no longer a guarantee of any kind. Thus, if a bug
  were found in 1.1 that affected 0.9 and could be easily applied, a new 0.9.x version might be released.

.. _nose: http://readthedocs.org/docs/nose/en/latest/
.. _tox: http://tox.testrun.org/
.. _nose-cov: http://pypi.python.org/pypi/nose-cov/
.. _issue tracker: https://github.com/jgorset/facepy/issues
.. _Github: http://github.com
.. _PEP-8: http://www.python.org/dev/peps/pep-0008/
.. _mock: http://www.voidspace.org.uk/python/mock/
