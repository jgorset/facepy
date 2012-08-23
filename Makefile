test:
	tox

report:
	nosetests --with-cov --cov-config tests/coveragerc --cov-report term-missing

release:
	python setup.py sdist register upload

documentation:
	cd docs; make html

pep8:
	@echo "Running PEP8 checks"
# flake 8 --ignore and --exclude is broken so we have to also use grep :(
	@flake8=$(flake8 --ignore=E501,W404 . --exclude=docs | \
		grep -v 'W404' | \
		grep -v '^./docs')
# We run pep8 on its own because flake8 embeds an old version of pep8
	@pep8 --ignore=E501 --exclude=docs .
