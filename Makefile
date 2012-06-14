test:
	nosetests

coverage:
	nosetests --with-cov --cov-config tests/coveragerc --cov-report term-missing

release:
	python setup.py sdist register upload
