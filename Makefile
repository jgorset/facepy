test:
	nosetests --with-color

release:
	python setup.py sdist register upload
