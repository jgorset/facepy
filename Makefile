test:
	tox

report:
	nosetests --with-cov --cov-config tests/coveragerc --cov-report term-missing

release:
	python setup.py sdist register upload

documentation:
		cd docs; make html
