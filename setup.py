from distutils.core import setup

setup(
  name = 'facepy',
  version = '0.2.2',
  description = "Facepy is an API client for Facebook's Graph API that doesn't suck.",
  author = "Johannes Gorset",
  author_email = "jgorset@gmail.com",
  url = "http://github.com/jgorset/facepy",
  packages = ['facepy'],
  requires = ['requests']
)
