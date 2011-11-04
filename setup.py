from setuptools import setup

setup(
    name = 'facepy',
    version = '0.4.2',
    description = "Facepy is a client for Facebook APIs.",
    author = "Johannes Gorset",
    author_email = "jgorset@gmail.com",
    url = "http://github.com/jgorset/facepy",
    packages = ['facepy'],
    install_requires = ['requests']
)
