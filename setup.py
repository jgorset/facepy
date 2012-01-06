from setuptools import setup

setup(
    name = 'facepy',
    version = '0.6',
    description = 'Facepy makes it absurdly easy to interact with Facebook APIs',
    author = 'Johannes Gorset',
    author_email = 'jgorset@gmail.com',
    url = 'http://github.com/jgorset/facepy',
    packages = ['facepy'],
    install_requires = ['requests==0.8.3'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)
