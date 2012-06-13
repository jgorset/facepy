test:
	nosetests

release:
	python setup.py sdist register upload
