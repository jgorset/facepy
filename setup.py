from setuptools import setup

setup(
  name = 'facepy',
  version = '0.2.3',
  description = "Facepy is an API client for Facebook's Graph API that doesn't suck.",
  author = "Johannes Gorset",
  author_email = "jgorset@gmail.com",
  url = "http://github.com/jgorset/facepy",
  packages = ['facepy'],
  install_requires = ['requests<=0.4']
)
