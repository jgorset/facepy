from setuptools import setup

setup(
    name = 'facepy',
    version = '0.6',
    description = 'Facepy makes it absurdly easy to interact with Facebook APIs',
    author = 'Johannes Gorset',
    author_email = 'jgorset@gmail.com',
    url = 'http://github.com/jgorset/facepy',
    packages = ['facepy'],
    install_requires = ['requests==0.8.3']
)
