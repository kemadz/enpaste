#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from enpaste import __version__


with open('README.md') as f:
    long_description = f.read()

setup(
    name="enpaste",
    version=__version__,
    license='MIT',
    description="A command-line tool using Evernote as a pastebin service",
    author='kemadz',
    author_email='kemadz@gmail.com',
    url='https://github.com/kemadz/enpaste',
    packages=['enpaste'],
    package_data={
        'enpaste': ['README.md', 'LICENSE']
    },
    install_requires=[
        'evernote'
    ],
    entry_points="""
    [console_scripts]
    enpaste = enpaste:main
    """,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    long_description=long_description,
    # tests_require=['nose', 'mock'],
    test_suite='nose.collector',
)
