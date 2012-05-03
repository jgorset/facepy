test:
	DJANGO_SETTINGS_MODULE=tests.project.settings nosetests

release:
	python setup.py sdist register upload
