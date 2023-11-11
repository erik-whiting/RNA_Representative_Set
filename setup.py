#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name = 'RNARepresentativeSet',
    version = '1.0',
    description = 'Tool for working with representative RNAs',
    long_description = LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    license = 'MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Science/Research',
        ],
    python_requires = '>=3.9',
    install_requires = ['bs4', 'requests'],
    packages=['RNARepresentativeSet']
)
