import os

from setuptools import setup
from codecs import open

readme = open('README.rst').read()
history = open('CHANGELOG.md').read()

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'facepy', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

setup(
    name='facepy',
    version=about['__version__'],
    description="Facepy makes it really easy to use Facebook's Graph API",
    long_description=readme + '\n\n' + history,
    author='Johannes Gorset',
    author_email='jgorset@gmail.com',
    url='http://github.com/jgorset/facepy',
    packages=['facepy'],
    install_requires=[
        'requests >= 0.8',
        'six >= 1.6',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False,
)
