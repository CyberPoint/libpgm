# run python setup.py install to install
# run python setup.py sdist to generate a tarball

from distutils.core import setup

setup(

    name = 'libpgm',
    version = '1.3',
    author = 'CyberPoint International, LLC',
    author_email = 'mraugas@cyberpointllc.com',
    url = 'http://www.cyberpointllc.com',
    description = 'A library for creating and using probabilistic graphical models',
    long_description = 'This library provides tools for modeling large systems with Bayesian networks. Using these tools allows for efficient statistical analysis on large data sets.',
    packages = ['libpgm', 'libpgm.CPDtypes', 'utils']
)
